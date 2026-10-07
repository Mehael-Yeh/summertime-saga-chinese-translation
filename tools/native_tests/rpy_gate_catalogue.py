"""Crawl RPY with the game's parser; record dependencies without execution."""
import ast
import hashlib
import types
from pathlib import Path


def stored_fields(node):
    try:fields=dict(object.__getattribute__(node,'__dict__'))
    except AttributeError:fields={}
    for cls in type(node).__mro__:
        for key,descriptor in vars(cls).items():
            native_field=(type(node).__module__.startswith('renpy.')
                and key in {'filename','linenumber','name','block','entries','condition','items',
                    'label','target','expression','arguments','code','store','varname','line','screen'}
                and isinstance(descriptor,types.GetSetDescriptorType))
            if (isinstance(descriptor,types.MemberDescriptorType) or native_field) and key not in fields:
                try:fields[key]=descriptor.__get__(node,type(node))
                except AttributeError:pass
    if type(node).__module__.startswith('renpy.ast'):
        # Ren'Py Object may virtualize its storage descriptors. These are
        # fixed AST data fields, never an arbitrary source-defined property.
        for key in ('filename','linenumber','name','block','entries','condition','items',
                'label','target','expression','arguments','code','store','varname','line','screen'):
            if key not in fields:
                try:fields[key]=object.__getattribute__(node,key)
                except AttributeError:pass
    return fields


def python_facts(source):
    try:tree=ast.parse(source)
    except (SyntaxError,TypeError) as error:
        return {'unresolved':[{'reason':'python_syntax','message':str(error)}]}
    reads=set();writes=set();calls=[];conditions=[]
    for node in ast.walk(tree):
        if isinstance(node,(ast.Attribute,ast.Name,ast.Subscript)):
            path=ast.unparse(node)
            if isinstance(node.ctx,ast.Load):reads.add(path)
            elif isinstance(node.ctx,(ast.Store,ast.Del)):writes.add(path)
        if isinstance(node,ast.Call):
            calls.append({'function':ast.unparse(node.func),'expression':ast.unparse(node),
                'line':node.lineno})
        if isinstance(node,(ast.If,ast.IfExp,ast.While,ast.Assert)):
            conditions.append({'expression':ast.unparse(node.test),'line':node.lineno})
    guarded=[]
    def descend(body,guards):
        for statement in body:
            if isinstance(statement,ast.If):
                expr=ast.unparse(statement.test)
                descend(statement.body,guards+[{'expression':expr,'truth':True}])
                descend(statement.orelse,guards+[{'expression':expr,'truth':False}])
            elif isinstance(statement,(ast.For,ast.AsyncFor,ast.While,ast.Try,ast.With,ast.AsyncWith)):
                guarded.append({'line':statement.lineno,'statement':ast.unparse(statement),
                    'guards':guards,'requires_native_control':True})
            else:
                guarded.append({'line':statement.lineno,'statement':ast.unparse(statement),'guards':guards})
    descend(tree.body,[])
    return {'reads':sorted(reads),'writes':sorted(writes),'calls':calls,
        'conditions':conditions,'guarded_statements':guarded,'unresolved':[]}


def native_statement_graph(blocks):
    rows=[];labels={};module_labels={};unknown=[];seen=set();screens={}
    def visit(block,owner,guards):
        for node in block:
            if id(node) in seen:continue
            seen.add(id(node))
            fields=stored_fields(node);kind=type(node).__name__
            source=str(fields.get('filename',''))
            line=fields.get('linenumber')
            if kind=='Label':owner=str(fields['name'])
            row={'id':str(len(rows)),'file':source,'line':line,'node':kind,
                'label':owner,'guards':list(guards),'status':'source_inventory_only'}
            rows.append(row)
            if source.endswith('.rpym'):row['requires_native_module_namespace']=True
            if kind=='Label':
                if source.endswith('.rpym'):
                    module_labels.setdefault(source,{}).setdefault(owner,[]).append(row['id'])
                else:labels.setdefault(owner,[]).append(row['id'])
            if kind=='If':
                previous=[]
                for expr,child in fields['entries']:
                    condition=str(expr)
                    row.setdefault('conditions',[]).append(condition)
                    visit(child,owner,guards+previous+[{'expression':condition,'truth':True}])
                    previous=previous+[{'expression':condition,'truth':False}]
            elif kind=='Menu':
                row['choices']=[]
                for caption,expr,child in fields['items']:
                    row['choices'].append({'caption':caption,'condition':str(expr),'has_block':child is not None})
                    if child is not None:
                        visit(child,owner,guards+[{'expression':str(expr),'truth':True,
                            'menu_input':caption,'menu_file':source,'menu_line':line}])
            elif kind=='While':
                row['conditions']=[str(fields.get('condition'))]
                row['requires_native_iteration']=True
                visit(fields.get('block',()),owner,guards+[{'expression':str(fields.get('condition')),
                    'truth':True,'requires_native_iteration':True}])
            elif kind in ('Call','Jump'):
                row['target']=str(fields.get('label') if kind=='Call' else fields.get('target'))
                row['dynamic_target']=bool(fields.get('expression'))
                arguments=fields.get('arguments')
                raw_args=getattr(arguments,'arguments',None) if arguments is not None else None
                row['arguments']=[{'name':name,'expression':str(expr)} for name,expr in raw_args] if raw_args is not None else None
                if arguments is not None and raw_args is None:row['unresolved_arguments']=True
            elif kind=='Return':
                expression=fields.get('expression')
                row['expression']=str(expression) if expression is not None else None
                if expression:row['python']=python_facts(str(expression))
            elif kind in ('Python','EarlyPython'):
                row['python']=python_facts(getattr(fields.get('code'),'source',None))
                row['requires_native_execution']=True
            elif kind in ('Default','Define'):
                row['store']=str(fields.get('store',''))
                row['variable']=str(fields.get('varname',''))
                row['python']=python_facts(getattr(fields.get('code'),'source',None))
            elif kind=='UserStatement':
                row['statement']=str(fields.get('line',''))
                row['requires_native_statement_protocol']=True
            elif kind=='Screen':
                row['screen']=str(getattr(fields.get('screen'),'name',''))
                screens[(row['screen'],row['id'])]=types.SimpleNamespace(function=fields['screen'])
                row['screen_declaration']=row['id']
            elif 'block' in fields and isinstance(fields['block'],(list,tuple)):
                visit(fields['block'],owner,guards)
            # Capture native syntax child protocols, including translate and
            # init blocks. No execute/eval is invoked during this crawl.
            elif kind not in ('Say','Show','Hide','Scene','With','Pause','Pass','Image',
                    'Transform','TranslateString','TranslatePython','EndTranslate',
                    'TranslateSay','Testcase','RPY','ShowLayer','Style'):
                unknown.append({'row':row['id'],'reason':'unclassified_statement','fields':sorted(fields)})
    for block in blocks:visit(block,None,[])
    edges=[];producers={};consumers={}
    for row in rows:
        if 'target' in row:
            module_candidates=[]
            if row['file'] in module_labels:
                module_candidates=module_labels[row['file']].get(row['target'],[])
            else:
                for filename,declared in module_labels.items():
                    prefix=Path(filename).stem+'.'
                    if row['target'].startswith(prefix):module_candidates.extend(declared.get(row['target'][len(prefix):],[]))
            edges.append({'source':row['id'],'target_label':row['target'],
                'target_rows':labels.get(row['target'],[]) if not row['dynamic_target'] else [],
                'module_target_candidates':module_candidates if not row['dynamic_target'] else [],
                'module_binding_unverified':bool(module_candidates) or row.get('requires_native_module_namespace',False),
                'dynamic':row['dynamic_target']})
        facts=row.get('python',{})
        for path in facts.get('writes',()):producers.setdefault(path,[]).append(row['id'])
        for expr in row.get('conditions',()):
            facts_expr=python_facts(expr)
            for path in facts_expr.get('reads',()):consumers.setdefault(path,[]).append(row['id'])
        for choice in row.get('choices',()):
            for path in python_facts(choice['condition']).get('reads',()):consumers.setdefault(path,[]).append(row['id'])
        for path in facts.get('reads',()):consumers.setdefault(path,[]).append(row['id'])
    try:from .screen_catalogue import screen_inventory
    except ImportError:from screen_catalogue import screen_inventory
    return {'statements':rows,'labels':labels,'module_labels':module_labels,'call_edges':edges,'screen_syntax':screen_inventory(screens),
        'field_dependencies':{path:{'producers':producers.get(path,[]),'consumers':consumers.get(path,[])}
            for path in sorted(producers.keys()|consumers.keys())},
        'unresolved':unknown,'all_gates_passed':False,
        'scope':'RPY syntax and lexical prerequisite dependencies; call guards, dynamic dispatch and native effects require solving/execution'}


def crawl_sources(roots,parser):
    blocks=[];files=[];errors=[];seen=set()
    for root in roots:
        for path in sorted(path for path in Path(root).rglob('*') if path.suffix in ('.rpy','.rpym') and path.is_file()):
            if path.resolve() in seen:continue
            seen.add(path.resolve())
            raw=path.read_bytes()
            entry={'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'script_module':path.suffix=='.rpym'}
            try:
                nodes=parser(str(path),raw.decode('utf-8-sig'))
                if nodes is None:raise ValueError('Native parser did not return a syntax tree')
                blocks.append(nodes);entry['parsed']=True
            except Exception as error:
                entry['parsed']=False
                errors.append({'path':str(path),'type':type(error).__name__,'message':str(error)})
            files.append(entry)
    graph=native_statement_graph(blocks)
    return {'roots':[str(root) for root in roots],'files':files,'parse_errors':errors,
        'graph':graph,'validation_mode':'gate_only','route_endpoint_validation_required':False,
        'all_gates_passed':False,
        'scope':'Direct RPY parsing only; no script, Python, screen or callback execution'}
