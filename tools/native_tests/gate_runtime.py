"""Observe admitted native predicates; never certify interaction responses.

Only explicit read protocols are accepted. Arbitrary calls, unknown locals,
unbounded iteration and writes cannot be evaluated here.
"""
import operator
import itertools
import dis
import json
import hashlib
import random
from enum import IntEnum
from contextlib import contextmanager
try:
    from .gate_catalogue import UNRESOLVED
except ImportError:
    from gate_catalogue import UNRESOLVED


def native_predicate(expression, roots, predicates):
    kind=expression.get('kind')
    if kind=='enum':
        clock_member=getattr(roots.get('time'),expression['type'],None)
        if (isinstance(clock_member,IntEnum) and type(clock_member).__module__==expression['module']
                and type(clock_member).__qualname__==expression['qualname']):
            member=type(clock_member).__members__.get(expression['name'],UNRESOLVED)
            if member is not UNRESOLVED and int(member)==expression['value']:return member
        return UNRESOLVED
    if kind=='literal':return expression['value']
    if kind=='constant':return {'Ellipsis':Ellipsis,'int':int,'float':float,'str':str,'bool':bool}.get(expression['name'],UNRESOLVED)
    if kind=='path':
        parts=expression['parts']
        value=roots.get(parts[0],UNRESOLVED)
        for field in parts[1:]:
            if field.startswith('_') or value is UNRESOLVED:return UNRESOLVED
            value=getattr(value,field,UNRESOLVED)
        return value
    if kind=='reference':
        for catalogue in roots.values():
            if (type(catalogue).__module__==expression['module']
                    and getattr(catalogue,'ref',None)==expression['ref']):return catalogue
            value=getattr(catalogue,expression['ref'],UNRESOLVED)
            if type(value).__module__==expression['module']:return value
        return UNRESOLVED
    if kind=='attribute':
        owner=native_predicate(expression['owner'],roots,predicates)
        field=expression['name']
        if owner is UNRESOLVED or field.startswith('_'):return UNRESOLVED
        # Only existing stored attributes here; computed properties require
        # their separately admitted native protocol.
        data=getattr(owner,'__dict__',{})
        return data.get(field,UNRESOLVED)
    if kind=='sequence':
        values=[native_predicate(x,roots,predicates) for x in expression['items']]
        return UNRESOLVED if any(x is UNRESOLVED for x in values) else tuple(values)
    if kind=='call':
        function=expression['function']
        if (function.get('kind')=='attribute' and function.get('name')=='random'
                and function.get('owner',{}).get('kind')=='call'
                and function['owner'].get('function')=={'kind':'callable','name':'random.Random'}
                and not expression['args'] and not expression['keywords']):
            owner=native_predicate(function['owner'],roots,predicates)
            return owner.random() if type(owner) is random.Random else UNRESOLVED
        if function.get('kind')!='callable':return UNRESOLVED
        callback=predicates.get(function['name'])
        if callback is None:return UNRESOLVED
        values=[native_predicate(x,roots,predicates) for x in expression['args']]
        if any(x is UNRESOLVED for x in values):return UNRESOLVED
        names=expression['keywords']
        count=len(values)-len(names)
        if callback is random.Random and (names or len(values)!=1 or type(values[0]) not in (int,float,str,bytes)):
            return UNRESOLVED
        if callback is len and (len(values)!=1 or not isinstance(values[0],(tuple,list,dict,set,frozenset,str,bytes))):return UNRESOLVED
        return callback(*values[:count],**dict(zip(names,values[count:])))
    if kind=='unary':
        value=native_predicate(expression['operand'],roots,predicates)
        if value is UNRESOLVED:return UNRESOLVED
        if expression['operator']=='UNARY_NOT':return not value
        if expression['operator']=='UNARY_NEGATIVE' and type(value) in (int,float):return -value
        return UNRESOLVED
    if kind=='operation':
        left=native_predicate(expression['left'],roots,predicates)
        right=native_predicate(expression['right'],roots,predicates)
        if left is UNRESOLVED or right is UNRESOLVED:return UNRESOLVED
        op=expression['operator']
        if op=='is':return left is right
        if op=='is not':return left is not right
        scalar=lambda value:type(value) in (str,int,float,bool,type(None))
        functions={'==':operator.eq,'!=':operator.ne,'<':operator.lt,'<=':operator.le,
                   '>':operator.gt,'>=':operator.ge,'+':operator.add,'-':operator.sub}
        numeric_left=int(left) if isinstance(left,IntEnum) else left
        numeric_right=int(right) if isinstance(right,IntEnum) else right
        arithmetic={'*':operator.mul,'/':operator.truediv,'//':operator.floordiv,'%':operator.mod}
        if op in arithmetic and type(numeric_left) in (int,float) and type(numeric_right) in (int,float):
            # Numeric operands only: never invoke overloaded entity operators.
            # Invalid arithmetic remains unknown, rather than blocking the probe.
            try:
                result=arithmetic[op](numeric_left,numeric_right)
            except (ArithmeticError,ValueError):
                return UNRESOLVED
            import math
            return result if type(result) is int or math.isfinite(result) else UNRESOLVED
        if op in functions and scalar(numeric_left) and scalar(numeric_right):return functions[op](numeric_left,numeric_right)
        if op in ('<','>') and type(right) is str:
            method=getattr(type(left),'__lt__' if op=='<' else '__gt__',None)
            code=getattr(method,'__code__',None)
            if (code is not None and getattr(method,'__module__','').startswith('saga.')
                    and code.co_names==('memo',)
                    and all(instruction.opname in ('RESUME','CACHE','NOP','LOAD_FAST','LOAD_ATTR','CONTAINS_OP','RETURN_VALUE')
                        for instruction in dis.get_instructions(code))):
                return method(left,right)
        if op in ('in','not in'):
            if type(left).__module__.startswith('saga.') and getattr(type(left),'__eq__',None) is object.__eq__:
                for container in (tuple,list,set,frozenset):
                    if isinstance(right,container):
                        # Identity comparison is the native object's equality
                        # protocol; builtin iteration avoids subclass hooks.
                        result=any(left is item for item in container.__iter__(right))
                        return not result if op=='not in' else result
            method=getattr(type(right),'__contains__',None)
            code=getattr(method,'__code__',None)
            if (code is not None and getattr(method,'__module__','').startswith('saga.')
                    and code.co_names==('getattr',) and 'where' in code.co_consts
                    and all(instruction.opname in ('RESUME','CACHE','NOP','LOAD_GLOBAL','LOAD_FAST','LOAD_CONST',
                        'PRECALL','CALL','IS_OP','RETURN_VALUE') for instruction in dis.get_instructions(code))):
                result=method(right,left)
                return not result if op=='not in' else result
            if (code is not None and getattr(method,'__module__','').startswith('saga.')
                    and set(code.co_names)=={'isinstance','Moveable','where','pool'}
                    and method.__globals__.get('isinstance',__import__('builtins').isinstance) is __import__('builtins').isinstance
                    and isinstance(getattr(right,'pool',None),(tuple,list,set,frozenset))
                    and all(instruction.opname in ('RESUME','CACHE','NOP','LOAD_GLOBAL','LOAD_FAST','LOAD_CONST',
                        'LOAD_ATTR','PRECALL','CALL','POP_JUMP_IF_FALSE','POP_JUMP_FORWARD_IF_FALSE',
                        'STORE_FAST','CONTAINS_OP','RETURN_VALUE') for instruction in dis.get_instructions(code))):
                result=method(right,left)
                return not result if op=='not in' else result
        if op in ('in','not in') and scalar(left) and type(right) in (tuple,list,set,frozenset):
            if not all(scalar(value) for value in right):return UNRESOLVED
            result=left in right
            return not result if op=='not in' else result
        if op=='subscript' and type(left) in (tuple,list,str) and type(right) is int:
            return left[right] if -len(left)<=right<len(left) else UNRESOLVED
    return UNRESOLVED


def observe_chain(branch, roots, predicates):
    """Observe reached predicates only; a blocked predecessor stays blocked."""
    if branch.get('prior_effects'):
        return {'status':'unresolved','reason':'requires_native_prior_effects'}
    try:
        for index,row in enumerate(branch.get('prerequisites',())):
            value=native_predicate(row['expression'],roots,predicates)
            if value is UNRESOLVED:return {'status':'unresolved','reason':'predecessor','index':index}
            if bool(value)!=row['truth']:return {'status':'predecessor_blocked','index':index}
        value=native_predicate(branch['expression'],roots,predicates)
        if value is UNRESOLVED:return {'status':'unresolved','reason':'predicate'}
        return {'status':'native_predicate_observed','truth':bool(value),
                'native_response_validated':False}
    except Exception as error:
        return {'status':'native_predicate_error','type':type(error).__name__,'message':str(error)}


@contextmanager
def parameter_fields(witness, roots, retain=False):
    """Apply solved stored parameters transactionally, including failures."""
    restored=[]
    try:
        for path,value in witness.get('changes',{}).items():
            parts=path.split('.')
            if len(parts)<3 or parts[0]=='time' or any(field.startswith('_') for field in parts):
                raise ValueError('unsupported_native_write_path')
            owner=roots.get(parts[0])
            for field in parts[1:-1]:owner=getattr(owner,field,None)
            data=getattr(owner,'__dict__',{})
            if parts[-1] not in data or type(data[parts[-1]]) not in (str,int,float,bool,type(None)):
                raise ValueError('not_a_stored_scalar')
            if type(value) not in (str,int,float,bool,type(None)):
                raise ValueError('not_a_scalar_parameter')
            restored.append((data,parts[-1],data[parts[-1]]))
            data[parts[-1]]=value
        yield
    finally:
        if not retain:
            for data,field,value in reversed(restored):data[field]=value


def solve_parameter_prerequisites(branch, roots, predicates, target, max_candidates=1024):
    """Search stored parameters while evaluating admitted native read protocols.

    References and computed clock fields are fixed native facts, not missing
    scalar inputs. Unknown reads and preceding effects still fail closed.
    """
    try:
        from .gate_catalogue import walk
    except ImportError:
        from gate_catalogue import walk
    if branch.get('prior_effects'):
        return {'status':'unresolved','reason':'requires_native_prior_effects'}
    constraints=list(branch.get('prerequisites',()))+[{'expression':branch['expression'],'truth':bool(target)}]
    nodes=[node for row in constraints for node in walk(row['expression'])]
    paths={tuple(node['parts']) for node in nodes if node.get('kind')=='path'}
    # getattr(owner, literal_field, default) reads the same stored parameter.
    for node in nodes:
        if node.get('kind')!='call' or node.get('function',{}).get('name')!='builtins.getattr':continue
        args=node['args']
        if len(args)>=2 and args[0].get('kind')=='path' and args[1].get('kind')=='literal' and isinstance(args[1]['value'],str):
            paths.add(tuple(args[0]['parts'])+(args[1]['value'],))
    literals=[node['value'] for node in nodes if node.get('kind')=='literal'
        and type(node['value']) in (str,int,float,bool,type(None))]
    typed_nullable={}
    for node in nodes:
        if node.get('kind')!='operation':continue
        for left,right in ((node['left'],node['right']),(node['right'],node['left'])):
            if left.get('kind')=='path' and right.get('kind')=='literal':
                typed_nullable.setdefault(tuple(left['parts']),[]).append(right['value'])
    domains={}
    random_paths=set()
    for node in nodes:
        if node.get('kind')=='call' and node.get('function')=={'kind':'callable','name':'random.Random'}:
            random_paths.update(tuple(child['parts']) for arg in node.get('args',()) for child in walk(arg)
                if child.get('kind')=='path')
    for parts in sorted(paths):
        if len(parts)<3 or parts[0]=='time' or any(field.startswith('_') for field in parts):continue
        owner=roots.get(parts[0])
        for field in parts[1:-1]:owner=getattr(owner,field,None)
        data=getattr(owner,'__dict__',{})
        if parts[-1] not in data or type(data[parts[-1]]) not in (str,int,float,bool,type(None)):continue
        value=data[parts[-1]]
        candidates=[value]
        if type(value) is bool:candidates.append(not value)
        else:
            for literal in typed_nullable.get(parts,[]) if value is None else literals:
                if type(value) is not type(literal) and value is not None:continue
                candidates.append(literal)
                if type(literal) in (int,float):candidates.extend((literal-1,literal+1))
            if type(value) is int and parts in random_paths:
                # A pure local Random constructor exposes a controllable
                # numeric input even when no integer literal occurs nearby.
                # Bound it explicitly; failure is not proof of impossibility.
                candidates.extend(range(64))
        unique=[]
        for candidate in candidates:
            if not any(type(candidate) is type(known) and candidate==known for known in unique):unique.append(candidate)
        domains['.'.join(parts)]=unique
    paths=sorted(domains)
    tried=0
    unknown=False
    for values in itertools.product(*(domains[path] for path in paths)):
        if tried>=max_candidates:return {'status':'budget_exhausted','candidates':tried}
        tried+=1
        changes={path:value for path,value in zip(paths,values)
            if type(value) is not type(domains[path][0]) or value!=domains[path][0]}
        try:
            with parameter_fields({'changes':changes},roots):
                result=observe_chain(branch,roots,predicates)
                if result.get('status')=='native_predicate_observed' and result.get('truth') is bool(target):
                    return {'status':'parameter_witness','changes':changes,'candidates':tried,
                        'seeded_random_domain_limit':64 if random_paths else None,
                        'native_response_validated':False}
                unknown|=result.get('status') in ('unresolved','native_predicate_error')
        except Exception as error:
            return {'status':'unresolved','reason':'parameter_search_error','type':type(error).__name__,'message':str(error)}
    return {'status':'unresolved' if unknown else 'no_parameter_witness','candidates':tried,
        'scope':'Finite native-read parameter domain; not proof of impossibility'}


def verify_scalar_witness(branch, witness, target, roots, predicates):
    """Test a proposed witness against actual native fields, then restore them."""
    try:
        with parameter_fields(witness, roots):
            observation=observe_chain(branch,roots,predicates)
            observation['witness_matches_native']=observation.get('truth') is bool(target) and observation['status']=='native_predicate_observed'
            observation['native_response_validated']=False
            return observation
    except ValueError as error:
        return {'status':'unresolved','reason':str(error)}


def execute_parameter_case(branch, witness, target, roots, predicates, invoke, tracer, observe, retain_parameters=False):
    """Set prerequisites, dispatch native code, and record actual consequences.

    The caller must provide a disposable native world. Parameter restoration
    alone cannot undo arbitrary callback effects. No navigation or dialogue
    replay occurs here. Unresolved script transfers remain incomplete.
    """
    # Sequential callers own one disposable world for the entire chain. Its
    # current inputs and native effects must survive into the next gate.
    with parameter_fields(witness, roots, retain=retain_parameters):
        admission=observe_chain(branch,roots,predicates)
        if admission.get('status')!='native_predicate_observed' or admission.get('truth') is not bool(target):
            return {'status':'prerequisite_not_satisfied','admission':admission,'native_response_validated':False}
        before=observe()
        tracer.begin()
        error=None
        try:
            invoke()
        except Exception as caught:
            error={'type':type(caught).__module__+'.'+type(caught).__name__,'message':str(caught)}
        finally:
            trace=tracer.finish()
        after=observe()
        reached=any(row.get('module')==branch.get('module')
            and row.get('code_identity_sha256')==branch.get('code_identity_sha256')
            and row.get('offset')==branch.get('offset')
            and row.get('condition_truth') is bool(target) for row in trace.get('observations',()))
        if branch.get('entry_only'):
            reached=any(row.get('module')==branch.get('module')
                and row.get('code_identity_sha256')==branch.get('code_identity_sha256')
                for row in trace.get('invocations',()))
        return {'status':'native_dispatch_observed' if reached and error is None else 'native_response_incomplete',
            'target_branch_observed':reached if not branch.get('entry_only') else None,
            'target_entry_observed':reached if branch.get('entry_only') else None,
            'parameters':dict(witness.get('changes',{})),
            'before':before,'after':after,'state_delta':state_delta(before,after),
            'native_branch_trace':trace,'error':error,
            'native_response_validated':False,
            'scope':'Executed native dispatch and state observations; script continuations and semantic postconditions require separate acceptance'}


def state_delta(before, after):
    """Record exact stored-fact differences without inferring story completion."""
    def digest(value):
        return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=True,
            separators=(',',':')).encode('ascii')).hexdigest()
    changes=[]
    def compare(left,right,path):
        if type(left) is type(right) and left==right:return
        if isinstance(left,dict) and isinstance(right,dict):
            for key in sorted(set(left)|set(right)):
                if key not in left or key not in right:
                    changes.append({'path':path+[key],'before_present':key in left,
                        'after_present':key in right,'before':left.get(key),'after':right.get(key)})
                else:compare(left[key],right[key],path+[key])
        else:changes.append({'path':path,'before':left,'after':right})
    compare(before,after,[])
    return {'before_sha256':digest(before),'after_sha256':digest(after),
        'changes':changes,'scope':'Observed stored facts only; unchanged or changed is not semantic acceptance'}
