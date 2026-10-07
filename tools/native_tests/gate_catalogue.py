"""Read native gate branches, without executing callbacks or assuming success.

Branches are individual control-flow edges, not one large conjunction. A
temporal witness is a test scenario; it must never be merged into save state.
"""
import dis
import functools
import hashlib
import json
import types
import builtins
import random
from enum import IntEnum
try:
    from .native_branch_trace import code_identity
except ImportError:
    from native_branch_trace import code_identity


UNKNOWN = {'kind': 'unknown'}
UNRESOLVED = object()


def unwrap_callback(callback, runtime_positional=()):
    """Read both functools and the engine's bound callback protocol."""
    supplied = {}
    positional = list(runtime_positional)
    visited = set()
    while id(callback) not in visited:
        visited.add(id(callback))
        if isinstance(callback,type):break
        if isinstance(callback, functools.partial) or (
                not hasattr(callback, '__code__') and callable(getattr(callback, 'func',None))
                and isinstance(getattr(callback,'args',None),(tuple,list)) and hasattr(callback, 'keywords')):
            function = callback.func
            # Outer bindings override inner bindings, just as a nested partial.
            current = dict(callback.keywords or {})
            positional = list(callback.args)+positional
            current.update(supplied)
            supplied = current
            callback = function
        elif hasattr(callback, '__wrapped__'):
            callback = callback.__wrapped__
        else:
            break
    code=getattr(callback,'__code__',None)
    if isinstance(code,types.CodeType):
        bound=dict(zip(code.co_varnames[:code.co_argcount],positional))
        bound.update(supplied)
        supplied=bound
    return callback, supplied


def literal(value):
    if isinstance(value,IntEnum):
        return {'kind':'enum','module':type(value).__module__,'type':type(value).__name__,
            'qualname':type(value).__qualname__,'name':value.name,'value':int(value)}
    if value is Ellipsis:return {'kind':'constant','name':'Ellipsis'}
    if isinstance(value,type) and value in (int,float,str,bool):
        return {'kind':'constant','name':value.__name__}
    if value is None or isinstance(value, (str, bool, int, float)):
        return {'kind': 'literal', 'value': value}
    if isinstance(value, (tuple, list, set, frozenset)):
        return {'kind': 'sequence', 'items': [literal(x) for x in value]}
    ref = getattr(value, 'ref', None)
    if isinstance(ref, str):
        return {'kind': 'reference', 'module': type(value).__module__, 'ref': ref}
    return UNKNOWN


def concrete_event_defaults(callback, requirements, clock=None):
    """Choose explicit event inputs from native declared defaults.

    These are deliberately dispatched test parameters, not observations of
    player inputs. A missing required argument without a default stays unknown.
    """
    function,supplied=unwrap_callback(callback)
    code=getattr(function,'__code__',None)
    event=dict(requirements)
    provenance={key:'registered_literal' for key in event}
    if code is None:return event,provenance,sorted(getattr(callback,'_req',()))
    defaults=function.__defaults__ or ()
    declared=dict(zip(code.co_varnames[code.co_argcount-len(defaults):code.co_argcount],defaults))
    declared.update(function.__kwdefaults__ or {})
    declared.update(supplied)
    missing=[]
    for key in sorted(getattr(callback,'_req',())):
        if key in event:continue
        if key not in declared:missing.append(key);continue
        value=declared[key]
        if value is None and clock is not None and isinstance(getattr(clock,key,None),IntEnum):
            event[key]=getattr(clock,key)
            provenance[key]='explicit_test_input_from_native_clock'
            continue
        if literal(value)['kind']=='unknown':missing.append(key);continue
        event[key]=value
        provenance[key]='explicit_test_input_from_native_default'
    return event,provenance,missing


def admitted_read_protocol(function):
    """Admit the engine's inspected eligibility protocol, not arbitrary calls."""
    if function in (builtins.getattr,builtins.len,random.Random):return True
    function,_=unwrap_callback(function)
    code=getattr(function,'__code__',None)
    if not isinstance(code,types.CodeType) or getattr(function,'__module__','')!='saga.logic.util' or code.co_name!='req':return False
    names={'Ellipsis','float','seen','time','now','__class__','int','str','plan',
           'isinstance','Container','where','zone','type','set','range','tuple',
           'TypeError','iter','next','extend'}
    forbidden={'STORE_ATTR','STORE_SUBSCR','DELETE_ATTR','DELETE_SUBSCR','STORE_GLOBAL','STORE_DEREF'}
    return set(code.co_names)<=names and not any(op.opname in forbidden for op in dis.get_instructions(code))


def admitted_expression_read(function):
    return (function.get('kind')=='attribute' and function.get('name')=='random'
        and function.get('owner',{}).get('kind')=='call'
        and function['owner'].get('function')=={'kind':'callable','name':'random.Random'})


def branch_inventory(callback, catalogues, clock, event_bindings=None, observer_context=UNRESOLVED, clock_bindings=()):
    """Bounded symbolic stack. Unsupported operations stay explicitly unknown."""
    required_event_fields=getattr(callback,'_req',())
    # Native annotate records the positional parameter count as an integer;
    # Event.next tests its truth value before supplying one observer ctx.
    needs_context=bool(getattr(callback,'_ctx',False))
    callback, supplied = unwrap_callback(callback,(observer_context,) if needs_context else ())
    if not isinstance(getattr(callback,'__code__',None),types.CodeType):
        return {'supported': False, 'branches': [], 'unsupported': ['non_python_callback']}
    defaults = callback.__defaults__ or ()
    bound = dict(zip(callback.__code__.co_varnames[callback.__code__.co_argcount-len(defaults):callback.__code__.co_argcount], defaults))
    bound.update(callback.__kwdefaults__ or {})
    bound.update(supplied)
    bound.update(event_bindings or {})
    for name in required_event_fields:
        if name not in supplied and name not in (event_bindings or {}):bound[name]=UNRESOLVED
    bound.update(zip(callback.__code__.co_freevars,
                     (cell.cell_contents for cell in (callback.__closure__ or ()))))
    results, writes, unsupported, instructions = [], [], set(), []

    def value_expression(value):
        if type(value) in (tuple,list,set,frozenset):
            return {'kind':'sequence','items':[value_expression(x) for x in value]}
        for key, catalogue in catalogues.items():
            if value is catalogue:
                return {'kind':'path', 'parts':[key]}
            ref = getattr(value, 'ref', None)
            if isinstance(ref, str) and getattr(catalogue, ref, None) is value:
                return {'kind':'path', 'parts':[key, ref]}
        if value is clock:
            return {'kind':'path', 'parts':['time']}
        if callable(value):
            return {'kind':'callable','name':(getattr(value,'__module__','') or '')+'.'+(getattr(value,'__name__','') or '')}
        return literal(value)

    def inspect(code, local):
        initial_local=dict(local)
        stack = []
        keywords = ()
        def pop():return stack.pop() if stack else UNKNOWN
        def global_value(name):
            value = callback.__globals__.get(name, getattr(builtins, name, UNRESOLVED))
            return value_expression(value)
        operations=list(dis.get_instructions(code))
        offsets={op.offset:index for index,op in enumerate(operations)}
        for op in operations:
            instructions.append({'code':code.co_name,'offset':op.offset,'operation':op.opname,
                'argument':op.argval if isinstance(op.argval,(str,int,float,bool,type(None))) else op.argrepr,
                'line':op.positions.lineno})
        pending=[(0,[],dict(local),(),[],frozenset(),[])]
        budget=4096
        while pending and budget:
            index,stack,local,keywords,prerequisites,visited,effects=pending.pop()
            if index>=len(operations):continue
            budget-=1
            op=operations[index]
            if op.offset in visited:
                unsupported.add('loop_requires_native_iteration')
                continue
            visited=visited|{op.offset}
            next_index=index+1
            name = op.opname
            if name in ('RESUME','CACHE','NOP','EXTENDED_ARG','PRECALL','PUSH_NULL','COPY_FREE_VARS'):
                pass
            elif name == 'LOAD_CONST':stack.append(literal(op.argval))
            elif name == 'LOAD_GLOBAL':stack.append(global_value(op.argval))
            elif name in ('LOAD_FAST','LOAD_DEREF','LOAD_FAST_CHECK'):
                stack.append(local.get(op.argval, {'kind':'local','name':op.argval}))
            elif name in ('LOAD_ATTR','LOAD_METHOD'):
                owner=pop()
                if owner.get('kind') == 'path':
                    stack.append({'kind':'path','parts':owner['parts']+[op.argval]})
                else:stack.append({'kind':'attribute','owner':owner,'name':op.argval})
            elif name in ('STORE_FAST','STORE_DEREF'):local[op.argval]=pop()
            elif name == 'KW_NAMES':keywords=code.co_consts[op.arg]
            elif name == 'CALL':
                args=[pop() for _ in range(op.arg)][::-1]
                function=pop()
                stack.append({'kind':'call','function':function,'args':args,'keywords':list(keywords)})
                function_name=function.get('name','')
                actual=next((value for value in callback.__globals__.values()
                    if callable(value) and (getattr(value,'__module__','') or '')+'.'+(getattr(value,'__name__','') or '')==function_name),None)
                if function_name=='builtins.getattr':actual=builtins.getattr
                if not admitted_read_protocol(actual) and not admitted_expression_read(function):
                    effects=effects+[{'offset':op.offset,'operation':'CALL','function':function}]
                keywords=()
            elif name == 'STORE_ATTR':
                owner,value=pop(),pop()
                writes.append({'module':callback.__module__,'code':code.co_name,
                    'code_identity_sha256':code_identity(code),'offset':op.offset,
                    'line':op.positions.lineno,'field':op.argval,'owner':owner,'value':value,
                    'prerequisites':list(prerequisites),'prior_effects':list(effects),
                    'projection_validated':False})
                effects=effects+[{'offset':op.offset,'operation':name}]
            elif name == 'SWAP':
                if len(stack)>=op.arg:stack[-1],stack[-op.arg]=stack[-op.arg],stack[-1]
                else:stack.clear();unsupported.add(name)
            elif name in ('COMPARE_OP','CONTAINS_OP','IS_OP','BINARY_OP','BINARY_SUBSCR'):
                right,left=pop(),pop()
                operator = op.argrepr if name in ('COMPARE_OP','BINARY_OP') else (
                    ('not in' if op.arg else 'in') if name=='CONTAINS_OP' else
                    ('is not' if op.arg else 'is') if name=='IS_OP' else 'subscript')
                stack.append({'kind':'operation','operator':operator,'left':left,'right':right})
            elif name in ('UNARY_NOT','UNARY_NEGATIVE'):
                stack.append({'kind':'unary','operator':name,'operand':pop()})
            elif name.startswith('POP_JUMP') or name.startswith('JUMP_IF'):
                expression=pop()
                if name.endswith('IF_NONE') or name.endswith('IF_NOT_NONE'):
                    expression={'kind':'operation','operator':'is' if name.endswith('IF_NONE') else 'is not',
                                'left':expression,'right':literal(None)}
                    jump_truth=True
                else:jump_truth='TRUE' in name
                results.append({'code':code.co_name,'offset':op.offset,'line':op.positions.lineno,
                    'module':callback.__module__, 'code_identity_sha256':code_identity(code),
                    'bytecode_sha256':hashlib.sha256(code.co_code).hexdigest(),
                    'jump':name,'target':op.argval,'expression':expression,
                    'prerequisites':prerequisites,
                    'prior_effects':effects,
                    'temporal':contains_clock(expression), 'supported':not unresolved(expression)})
                jump_stack=list(stack)
                if name.startswith('JUMP_IF'):jump_stack.append(expression)
                pending.append((offsets[op.argval],jump_stack,dict(local),keywords,
                    prerequisites+[{'expression':expression,'truth':jump_truth}],visited,list(effects)))
                prerequisites=prerequisites+[{'expression':expression,'truth':not jump_truth}]
            elif name in ('BUILD_TUPLE','BUILD_LIST','BUILD_SET'):
                values=[pop() for _ in range(op.arg)][::-1]
                stack.append({'kind':'sequence','items':values})
            elif name == 'COPY':stack.append(stack[-op.arg] if len(stack)>=op.arg else UNKNOWN)
            elif name == 'POP_TOP':pop()
            elif name in ('RETURN_VALUE','RETURN_CONST'):
                continue
            elif name in ('JUMP_FORWARD','JUMP_BACKWARD','JUMP_BACKWARD_NO_INTERRUPT'):
                next_index=offsets[op.argval]
            else:
                # Calls, iterators and computed protocols cannot be guessed.
                unsupported.add(name)
                stack.clear()
                effects=effects+[{'offset':op.offset,'operation':name}]
            pending.append((next_index,stack,local,keywords,prerequisites,visited,effects))
        if pending:unsupported.add('control_flow_budget_exhausted')
        for child in code.co_consts:
            if isinstance(child,types.CodeType):inspect(child,dict(initial_local))
    local={name:value_expression(value) for name,value in bound.items()}
    for name in clock_bindings:
        if isinstance(bound.get(name),IntEnum) and isinstance(getattr(clock,name,None),type(bound[name])):
            local[name]={'kind':'path','parts':['time',name]}
    inspect(callback.__code__,local)
    return {'supported':not unsupported and all(x['supported'] for x in results),
            'branches':results,'writes':writes,'unsupported':sorted(unsupported),
            'instructions':instructions,
            'bytecode_sha256':hashlib.sha256(callback.__code__.co_code).hexdigest()}


def walk(expression):
    if isinstance(expression,dict):
        yield expression
        for value in expression.values():yield from walk(value)
    elif isinstance(expression,list):
        for value in expression:yield from walk(value)


def contains_clock(expression):
    return any(x.get('kind')=='path' and x['parts'][0]=='time' for x in walk(expression))


def unresolved(expression):
    return any(x.get('kind') in ('unknown','local','attribute','call','callable') for x in walk(expression))


def temporal_scenarios(days, periods, start_day=1):
    """Separate witnesses for mutually exclusive weekdays and time periods."""
    if days <= 0 or periods <= 0:raise ValueError('Empty native clock domain')
    return tuple({'day':day,'period':period,'tick':day*periods+period}
                 for day in range(start_day,start_day+days) for period in range(periods))


def evaluate_expression(expression, facts):
    """Evaluate supplied scalar facts only; never invoke native game methods."""
    kind=expression.get('kind')
    if kind=='literal':return expression['value']
    if kind=='path':return facts.get('.'.join(expression['parts']),UNRESOLVED)
    if kind=='sequence':
        values=[evaluate_expression(x,facts) for x in expression['items']]
        return UNRESOLVED if any(x is UNRESOLVED for x in values) else values
    if kind=='unary':
        value=evaluate_expression(expression['operand'],facts)
        if value is UNRESOLVED:return UNRESOLVED
        if expression['operator']=='UNARY_NOT':return not value
        if expression['operator']=='UNARY_NEGATIVE' and type(value) in (int,float):return -value
    if kind=='operation':
        left=evaluate_expression(expression['left'],facts)
        right=evaluate_expression(expression['right'],facts)
        if left is UNRESOLVED or right is UNRESOLVED:return UNRESOLVED
        # No overloaded native comparisons/membership or arbitrary subscripts.
        scalar=lambda value: type(value) in (str,int,float,bool,type(None))
        op=expression['operator']
        if not scalar(left) or not scalar(right):return UNRESOLVED
        import operator
        operations={'==':operator.eq,'!=':operator.ne,'<':operator.lt,'<=':operator.le,
                    '>':operator.gt,'>=':operator.ge,'+':operator.add,'-':operator.sub}
        if op not in operations:return UNRESOLVED
        try:return operations[op](left,right)
        except (TypeError,ValueError):return UNRESOLVED
    return UNRESOLVED


def branch_witnesses(expression, scenarios):
    results={'true':[],'false':[],'unknown':[]}
    for identity,facts in scenarios:
        result=evaluate_expression(expression,facts)
        key='unknown' if result is UNRESOLVED else 'true' if bool(result) else 'false'
        results[key].append(identity)
    return results


def solve_prerequisites(branch, facts, target, max_candidates=1024):
    """Finite scalar constraint search, with explicit unknown/budget results.

    A witness satisfies the entire predecessor chain, not just the last test.
    This proposes test facts; it never writes them to a save or certifies a
    native response. Unsupported dynamic predicates remain unresolved.
    """
    import itertools
    constraints=list(branch.get('prerequisites',()))+[
        {'expression':branch['expression'],'truth':bool(target)}]
    if branch.get('prior_effects'):
        return {'status':'unresolved','reason':'requires_native_prior_effects'}
    if any(unresolved(row['expression']) for row in constraints):
        return {'status':'unresolved','reason':'dynamic_or_missing_binding'}
    paths={'.'.join(node['parts']) for row in constraints for node in walk(row['expression'])
           if node.get('kind')=='path'}
    if any(path not in facts for path in paths):
        return {'status':'unresolved','reason':'missing_fact',
                'paths':sorted(paths-facts.keys())}
    if any(type(facts[path]) not in (str,int,float,bool,type(None)) for path in paths):
        return {'status':'unresolved','reason':'non_scalar_native_fact'}
    # Time is supplied by a separate native clock scenario, never solved as
    # unrelated date/period fields. Durable domains use observed thresholds.
    variable_paths=sorted(path for path in paths if not path.startswith('time.'))
    domains={path:[facts[path]] for path in variable_paths}
    # A bare flag is itself a predicate. Without both Boolean values, a
    # false initial flag can never yield a candidate for the open branch.
    for path in variable_paths:
        if type(facts[path]) is bool:domains[path].append(not facts[path])
    for row in constraints:
        for node in walk(row['expression']):
            if node.get('kind')!='operation':continue
            left,right=node['left'],node['right']
            if left.get('kind')=='literal' and right.get('kind')=='path':left,right=right,left
            if left.get('kind')!='path' or right.get('kind')!='literal':continue
            path='.'.join(left['parts'])
            if path not in domains:continue
            value=right['value']
            candidates=[value]
            if type(value) in (int,float):candidates.extend((value-1,value+1))
            if type(value) is bool:candidates.append(not value)
            for candidate in candidates:
                if not any(type(candidate) is type(v) and candidate==v for v in domains[path]):
                    domains[path].append(candidate)
    tried=0
    unknown=False
    for values in itertools.product(*(domains[path] for path in variable_paths)):
        if tried>=max_candidates:
            return {'status':'budget_exhausted','candidates':tried}
        tried+=1
        scenario=dict(facts)
        scenario.update(zip(variable_paths,values))
        evaluations=[evaluate_expression(row['expression'],scenario) for row in constraints]
        if any(value is UNRESOLVED for value in evaluations):unknown=True;continue
        if all(bool(value)==row['truth'] for value,row in zip(evaluations,constraints)):
            return {'status':'scalar_witness','changes':{
                path:scenario[path] for path in variable_paths
                if type(scenario[path]) is not type(facts[path]) or scenario[path]!=facts[path]},
                'candidates':tried,'native_response_validated':False}
    return {'status':'unresolved' if unknown else 'no_scalar_witness',
            'candidates':tried,'scope':'Finite threshold domain, not proof of impossibility'}


def render_inventory(report):
    lines=['# Native gate inventory','',
           'Extracted registrations and control-flow branches; not a passed-gate certificate.',
           'Temporal branches need separate scenarios. Unknown expressions require further parsing.',
           '', '| ID | Source | Registration | Branches | Temporal | Unknown branches |',
           '| --- | --- | --- | ---: | ---: | ---: |']
    for row in report['gates']:
        branches=row['analysis']['branches']
        def cell(value):return str(value).replace('|','\\|').replace('\n',' ')
        lines.append('| '+' | '.join(map(cell,(row['id'],row['source'],json.dumps(row['requirements'],ensure_ascii=False),
            len(branches),sum(x['temporal'] for x in branches),sum(not x['supported'] for x in branches))))+' |')
    lines.extend(['','## Branch prerequisites','',
        'Each row is a native branch edge. These edges are not required to be true simultaneously.',
        '', '| Gate | Code / line | Predicate | Jump | Temporal | Parsed |',
        '| --- | --- | --- | --- | --- | --- |'])
    for row in report['gates']:
        for branch in row['analysis']['branches']:
            lines.append('| '+' | '.join(map(cell,(row['id'],str(branch['code'])+' / '+str(branch['line']),
                format_expression(branch['expression']),branch['jump']+' -> '+str(branch['target']),
                branch['temporal'],branch['supported'])))+' |')
    lines.extend(['','## Script conditions','', '| File / line | Kind | Condition |',
                  '| --- | --- | --- |'])
    for row in report.get('script_conditions',()):
        lines.append('| '+' | '.join(map(cell,(str(row['file'])+':'+str(row['line']),row['kind'],row['expression'])))+' |')
    return '\n'.join(lines)+'\n'


def format_expression(expression):
    kind=expression.get('kind')
    if kind=='path':return '.'.join(expression['parts'])
    if kind=='literal':return repr(expression['value'])
    if kind=='local':return '<local '+expression['name']+'>'
    if kind=='reference':return expression['module']+'.'+expression['ref']
    if kind=='sequence':return '['+', '.join(format_expression(x) for x in expression['items'])+']'
    if kind=='attribute':return format_expression(expression['owner'])+'.'+expression['name']
    if kind=='callable':return expression['name']
    if kind=='call':return format_expression(expression['function'])+'('+', '.join(format_expression(x) for x in expression['args'])+')'
    if kind=='operation':return '('+format_expression(expression['left'])+' '+expression['operator']+' '+format_expression(expression['right'])+')'
    if kind=='unary':return expression['operator']+'('+format_expression(expression['operand'])+')'
    return '<unknown>'
