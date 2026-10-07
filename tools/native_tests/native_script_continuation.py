"""Run native script state transitions without presenting dialogue or scenes.

Native Python, branching, calls and returns remain native. Menus require an
explicit enabled input; unknown screen/custom statements never return success.
"""
import time
import json
import ast
import sys
from contextlib import contextmanager


class ScriptBlocked(BaseException):
    def __init__(self, reason, details):
        self.reason,self.details=reason,details


def expand_menu_plans(plan, receipts):
    """Derive separate inputs only from a native menu's enabled payloads.

    The caller must reconstruct an isolated world before every resulting
    plan. An interrupted script's partially changed world must not be reused.
    """
    for receipt in reversed(receipts):
        if receipt.get('reason')!='native_menu_input_required':continue
        details=receipt['details']
        key=details['source']
        if key in plan:return []
        return [dict(plan,**{key:row['value']}) for row in details['available']]
    # A screen may have a native preference-controlled alternative. Derive
    # Scalar parameter candidates from actual preceding script conditions;
    # never manufacture a screen's return value to bypass that screen.
    parameters=plan.get('__parameters__',{})
    result=[]
    for receipt in receipts:
        if receipt.get('status')!='native_script_blocked':continue
        for statement in receipt.get('statements',()):
            domains=statement.get('stored_scalar_candidates')
            if domains is None:domains={path:[not value] for path,value in statement.get('stored_boolean_parameters',{}).items()}
            for path,values in domains.items():
                if path in parameters:continue
                for value in values:
                    changed=dict(parameters,**{path:value})
                    candidate=dict(plan,__parameters__=changed)
                    if candidate not in result:result.append(candidate)
    return result


def plan_identity(plan):
    return json.dumps(plan,sort_keys=True,separators=(',',':'))


def parameter_owner(api,path):
    parts=path.split('.')
    if len(parts)<2 or any(not part.isidentifier() or part.startswith('_') for part in parts):
        raise ValueError('Unsupported script parameter path')
    owner=api.store
    for part in parts[:-1]:owner=getattr(owner,part)
    if owner is getattr(getattr(api.store,'saga',None),'time',None):
        raise ValueError('Native clock requires a separate temporal scenario')
    data=getattr(owner,'__dict__',{})
    if parts[-1] not in data or type(data[parts[-1]]) not in (str,int,float,bool,type(None)):
        raise ValueError('Script parameter is not a stored scalar')
    return data,parts[-1]


def apply_script_parameters(api,parameters):
    changes=[]
    for path,value in parameters.items():
        data,field=parameter_owner(api,path)
        if type(value) not in (str,int,float,bool,type(None)) or (data[field] is not None and type(value) is not type(data[field])):
            raise ValueError('Script parameter type mismatch')
        changes.append((data,field,value))
    for data,field,value in changes:data[field]=value


def replace_persistent_aliases(namespaces,original,replacement):
    """Redirect imported native aliases to the disposable persistent object."""
    bindings=[]
    seen=set()
    for namespace in namespaces:
        if id(namespace) in seen:continue
        seen.add(id(namespace))
        for key,value in tuple(namespace.items()):
            if value is original:
                bindings.append((namespace,key,value))
                namespace[key]=replacement
    return bindings


def restore_persistent_aliases(bindings):
    for namespace,key,value in reversed(bindings):namespace[key]=value


def stored_boolean_parameters(api,expressions):
    result={}
    for expression in expressions:
        try:tree=ast.parse(expression,mode='eval')
        except (SyntaxError,TypeError):continue
        for node in ast.walk(tree):
            if not isinstance(node,ast.Attribute):continue
            parts=[]
            current=node
            while isinstance(current,ast.Attribute):parts.insert(0,current.attr);current=current.value
            if not isinstance(current,ast.Name):continue
            path='.'.join([current.id]+parts)
            try:
                data,field=parameter_owner(api,path)
                if type(data[field]) is bool:result[path]=data[field]
            except (ValueError,AttributeError):pass
    return result


def script_parameter_candidates(api,expressions):
    """Finite scalar domains from native If literals, without evaluating code."""
    result={path:[not value] for path,value in stored_boolean_parameters(api,expressions).items()}
    for expression in expressions:
        try:tree=ast.parse(expression,mode='eval')
        except (SyntaxError,TypeError):continue
        for node in ast.walk(tree):
            if not isinstance(node,ast.Compare):continue
            operands=[node.left]+node.comparators
            for left,right in zip(operands,operands[1:]):
                for field_node,literal_node in ((left,right),(right,left)):
                    if not isinstance(field_node,ast.Attribute):continue
                    try:
                        value=ast.literal_eval(literal_node)
                        path=ast.unparse(field_node)
                        data,field=parameter_owner(api,path)
                    except (ValueError,TypeError,SyntaxError,AttributeError):continue
                    original=data[field]
                    if type(value) not in (str,int,float,bool,type(None)) or (original is not None and type(original) is not type(value)):continue
                    domain=[value]
                    if type(value) in (int,float):domain.extend((value-1,value+1))
                    for candidate in domain:
                        if type(candidate) is type(original) and candidate==original:continue
                        if candidate not in result.setdefault(path,[]):result[path].append(candidate)
    return result


class ScriptContinuation:
    presentation={'Say','Show','Hide','Scene','With'}
    native={'Label','Python','EarlyPython','If','While','Menu','Call','Return','Jump','Pass',
            'Translate','TranslateSay','EndTranslate','TranslateBlock','TranslateEarlyBlock','Default'}

    def __init__(self, renpy, inputs=None, statement_limit=10000, seconds=5):
        self.renpy=renpy
        self.inputs=dict(inputs or {})
        self.statement_limit,self.seconds=statement_limit,seconds
        self.records=[]

    def key(self, node):
        return str(node.filename)+':'+str(node.linenumber)

    def execute(self, original, node, owner_kind=None):
        if len(self.records)>=self.statement_limit or time.monotonic()-self.started>self.seconds:
            raise ScriptBlocked('native_script_budget',{'statements':len(self.records)})
        kind=type(node).__name__
        self.current=node
        row={'kind':kind,'source':self.key(node)}
        self.records.append(row)
        if kind=='If':
            row['native_conditions']=[str(expression) for expression,block in node.entries]
            row['stored_boolean_parameters']=stored_boolean_parameters(self.renpy,row['native_conditions'])
            row['stored_scalar_candidates']=script_parameter_candidates(self.renpy,row['native_conditions'])
        # TranslateSay executes its native translation lookup and seen-state
        # bookkeeping, then calls Say.execute. Only that presentation layer
        # is omitted; skipping TranslateSay would discard native state work.
        if kind in self.presentation or owner_kind=='Say':
            row['scope']='presentation_omitted_not_ui_acceptance'
            self.renpy.ast.next_node(node.next)
            return
        if kind=='UserStatement':
            line=getattr(node,'line','').strip()
            if line=='pause' or line.startswith('pause '):
                row['scope']='presentation_pause_omitted'
                self.renpy.ast.next_node(node.next)
                return
            raise ScriptBlocked('native_statement_requires_adapter',{'source':self.key(node),'line':line})
        if kind not in self.native:
            raise ScriptBlocked('native_node_requires_adapter',row)
        try:
            if kind=='If':
                original_eval=self.renpy.python.py_eval
                original_next=self.renpy.ast.next_node
                control_targets=[]
                row['native_evaluated_conditions']=[]
                def observed_eval(expression,*args,**kwargs):
                    direct=sys._getframe(1).f_code is getattr(original,'__code__',None)
                    value=original_eval(expression,*args,**kwargs)
                    if direct and str(expression) in row['native_conditions']:
                        record={'expression':str(expression)}
                        if type(value) in (str,int,float,bool,type(None)):
                            record.update(value=value,truth=bool(value))
                        else:
                            # Do not invoke a custom __bool__ a second time.
                            record.update(truth=None,unresolved_truth_type=type(value).__module__+'.'+type(value).__qualname__)
                        row['native_evaluated_conditions'].append(record)
                    return value
                def observed_next(target):
                    if sys._getframe(1).f_code is getattr(original,'__code__',None):control_targets.append(target)
                    return original_next(target)
                self.renpy.python.py_eval=observed_eval
                self.renpy.ast.next_node=observed_next
                try:
                    result=original(node)
                    evaluations=row['native_evaluated_conditions']
                    chosen=[index for index,(expr,block) in enumerate(node.entries)
                        if block and len(control_targets)==2 and control_targets[-1] is block[0]]
                    selected=chosen[0] if len(chosen)==1 and len(evaluations)==chosen[0]+1 else None
                    if selected is not None or len(control_targets)==1 and len(evaluations)==len(node.entries):
                        for index,record in enumerate(evaluations):
                            record['truth']=index==selected
                            record['native_truth_source']='native_control_transfer'
                            record.pop('unresolved_truth_type',None)
                    return result
                finally:
                    self.renpy.python.py_eval=original_eval
                    self.renpy.ast.next_node=original_next
            return original(node)
        except Exception as error:
            if type(error).__module__.startswith('renpy.') and type(error).__name__ in (
                    'CallException','JumpException','JumpOutException','ReturnException','RestartException'):
                raise
            raise ScriptBlocked('native_script_execution_error',dict(row,
                type=type(error).__name__,message=str(error)))

    def menu(self, choices, *args, **kwargs):
        node=self.current
        key=self.key(node)
        enabled=[(caption,value) for caption,condition,value in choices
            if value is not None and bool(self.renpy.python.py_eval(condition))]
        available=[{'caption':caption,'value':value} for caption,value in enabled]
        if key in self.inputs:
            selected=[value for caption,value in enabled if value==self.inputs[key]]
            if len(selected)!=1:raise ScriptBlocked('native_menu_input_not_enabled',{'source':key,'available':available})
            value=selected[0]
        elif len(enabled)==1:
            value=enabled[0][1]
        else:
            raise ScriptBlocked('native_menu_input_required',{'source':key,'available':available})
        self.records[-1]['native_menu_input']=value
        return value

    @contextmanager
    def adapters(self):
        api=self.renpy
        patched=[]
        seen=set()
        try:
            for cls in vars(api.ast).values():
                if not isinstance(cls,type) or not issubclass(cls,api.ast.Node) or 'execute' not in vars(cls) or id(cls) in seen:continue
                seen.add(id(cls))
                original=cls.execute
                def execute(node, original=original, owner_kind=cls.__name__):return self.execute(original,node,owner_kind)
                patched.append((cls,'execute',original))
                cls.execute=execute
            patched.append((api.exports,'menu',api.exports.menu))
            api.exports.menu=self.menu
            yield
        finally:
            for owner,name,value in reversed(patched):setattr(owner,name,value)

    def run(self, label, args=(), kwargs=None):
        self.started=time.monotonic()
        self.records=[]
        try:
            with self.adapters():
                result=self.renpy.call_in_new_context(label,*args,**dict(kwargs or {}))
            return {'status':'native_script_returned','value':result,'statements':list(self.records)}
        except ScriptBlocked as blocked:
            return {'status':'native_script_blocked','reason':blocked.reason,
                'details':blocked.details,'statements':list(self.records)}
