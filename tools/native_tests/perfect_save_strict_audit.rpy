# Read-only catalogue/condition audit in isolated official-game copies only.
init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-perfect-mod-tests')
init 1000 python:
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_strict_splash'
    import sys,types
    _strict=types.ModuleType('ssct_strict_probe')
    _strict.phase=0
    sys.modules[_strict.__name__]=_strict

    def _ssct_strict_run():
        import ast,json,os,re,collections
        import dis
        from saga import step,flow
        def reference(node):
            if isinstance(node,ast.Constant):return node.value
            if isinstance(node,ast.Attribute) and isinstance(node.value,ast.Attribute) and isinstance(node.value.value,ast.Name) and node.value.value.id=='saga':
                return getattr(getattr(saga,node.value.attr),node.attr)
            raise ValueError('Nonliteral query argument')
        def serial(value):return getattr(value,'ref',value)
        queries={}
        other=[]
        for statement in renpy.game.script.all_stmts:
            if not isinstance(statement,renpy.ast.Menu):continue
            for caption,condition,block in statement.items:
                if not condition or str(condition)=='True':continue
                try:expr=ast.parse(str(condition),mode='eval').body
                except SyntaxError:continue
                calls=[item for item in ast.walk(expr) if isinstance(item,ast.Call) and isinstance(item.func,ast.Attribute) and item.func.attr=='peek' and isinstance(item.func.value,ast.Attribute) and item.func.value.attr=='event' and isinstance(item.func.value.value,ast.Name) and item.func.value.value.id=='saga']
                if not calls:
                    other.append((str(statement.filename),statement.linenumber,str(caption),str(condition)))
                    continue
                for call in calls:
                    try:params={item.arg:reference(item.value) for item in call.keywords}
                    except (ValueError,AttributeError):
                        other.append((str(statement.filename),statement.linenumber,str(caption),str(condition)))
                        continue
                    if call.args or None in params:continue
                    key=tuple(sorted((name,serial(value)) for name,value in params.items()))
                    item=queries.setdefault(key,{'params':params,'sources':[],'available':[],'errors':[],'candidates':[]})
                    item['sources'].append((str(statement.filename),statement.linenumber,str(caption),str(condition)))
        # Match literal event-pool requirements independently of the Mod model.
        for node in step:
            for entry in getattr(node,'pool',()):
                requirements=dict(entry[1])
                for item in queries.values():
                    if not all(name in requirements and requirements[name]==value for name,value in item['params'].items()):continue
                    kind='finite' if re.match(r'^[a-z]+[0-9]+_',node.ref) else 'cycle' if '_baby_' in node.ref else 'repeat'
                    item['candidates'].append((node.ref,getattr(entry[0],'__name__',type(entry[0]).__name__),kind))
        original=saga.time.now
        model=_ssct_completion_model([route for route in flow if _ssct_perfect_stages(route,step)],tuple(step))
        removed={target for target,attached in model['listeners'].items() if not attached}
        edges={}
        native_steps={id(node):node for node in step}
        for node in step:
            destinations=set()
            for entry in getattr(node,'pool',()):
                callback=entry[0]
                if not hasattr(callback,'__code__'):continue
                defaults=callback.__defaults__ or ()
                code=callback.__code__
                bound=dict(zip(code.co_varnames[code.co_argcount-len(defaults):code.co_argcount],defaults))
                bound.update(dict(entry[1]))
                instructions=list(dis.get_instructions(callback))
                for index,op in enumerate(instructions):
                    if op.opname!='RETURN_VALUE':continue
                    result,unused=_ssct_completion_expression(instructions,index-1,callback.__globals__,bound)
                    for target in result if isinstance(result,tuple) else (result,):
                        if id(target) in native_steps:destinations.add(target.ref)
            edges[node.ref]=sorted(destinations)
        reachable=set()
        pending=[getattr(getattr(entity,'step',None),'ref',None) for entity in saga.event.crowd]
        while pending:
            ref=pending.pop()
            if not ref or ref in reachable:continue
            reachable.add(ref)
            pending.extend(edges.get(ref,()))
        direct={source:{'source':source,'available':[],'errors':[],'supported':False} for source in other}
        permitted=(ast.Expression,ast.BoolOp,ast.And,ast.Or,ast.UnaryOp,ast.Not,ast.Compare,ast.Lt,ast.LtE,ast.Gt,ast.GtE,ast.Eq,ast.NotEq,ast.In,ast.NotIn,ast.Is,ast.IsNot,ast.Attribute,ast.Name,ast.Load,ast.Constant,ast.Tuple)
        for source,row in direct.items():
            try:tree=ast.parse(source[3],mode='eval')
            except SyntaxError:continue
            row['supported']=all(isinstance(node,permitted) and (not isinstance(node,ast.Name) or node.id=='saga') for node in ast.walk(tree))
        listeners={}
        for context in tuple(saga.event.crowd):
            active=getattr(context,'step',context)
            for entry in getattr(active,'pool',()):
                key=active.ref+'.'+getattr(entry[0],'__name__',type(entry[0]).__name__)
                listeners[key]=repr(entry[1])
        for tick in range(28):
            saga.time.now=tick
            _ssct_perfect_schedule()
            for item in queries.values():
                try:
                    if saga.event.peek(**item['params']):item['available'].append(tick)
                except Exception as error:item['errors'].append((tick,type(error).__name__,str(error)))
            for source,row in direct.items():
                if not row['supported']:continue
                try:
                    if renpy.python.py_eval(source[3]):row['available'].append(tick)
                except Exception as error:row['errors'].append((tick,type(error).__name__,str(error)))
            saga.event.queue=renpy.revertable.RevertableList()
        saga.time.now=original
        _ssct_perfect_schedule()
        result={'version':config.version,'routes':ssct_perfect_generation['routes'],
                'completion':ssct_perfect_generation['completion_contract'],
                'place_program_retirements':ssct_perfect_generation.get('completed_enter_programs',[]),
                'queries':[],'other_menu_conditions':list(direct.values()),'active_event_pools':listeners}
        # Independent native data export for comparison with observed normal
        # endpoints. No completion-model inference decides these values.
        import importlib.util
        spec=importlib.util.spec_from_file_location('ssct_contract_guard',os.path.join(config.basedir,'ssct_replay_guard.py'))
        guard=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guard)
        result['native_postconditions']={kind+'.'+entity.ref:guard.stored_facts(entity,
            ignored=('when','where','plan'))
            for kind,catalogue in _ssct_completion_catalogues().items()
            if kind in ('cast','prop','flow','sets') for entity in catalogue}
        for key,item in queries.items():
            item['params']={name:serial(value) for name,value in item['params'].items()}
            item['status']='available_in_week' if item['available'] else 'requires_review'
            if not item['available'] and item['candidates'] and all(row[2]=='finite' for row in item['candidates']):item['status']='completed_finite_only'
            if not item['available'] and item['candidates'] and all(row[2]=='cycle' for row in item['candidates']):item['status']='inactive_cycle'
            if not item['available'] and item['status']=='requires_review':
                repeats=[row for row in item['candidates'] if row[2]=='repeat']
                if repeats and all(('step',row[0]) in removed for row in repeats):
                    item['status']='native_retired_repeat'
                    item['retirement_sources']=[row for row in model['sources'] if row[1]=='detach' and row[2] in removed and row[2][0]=='step' and row[2][1] in {candidate[0] for candidate in repeats}]
                elif repeats and any(row[0] in reachable for row in repeats):
                    item['status']='later_native_repeat_phase'
                    item['transition_edges']={ref:targets for ref,targets in edges.items() if any(target==row[0] for row in repeats for target in targets)}
                elif not item['candidates']:item['status']='no_literal_handler_in_catalogue'
            result['queries'].append(item)
        with open(os.path.join(config.basedir,'perfect_strict_audit.json'),'w',encoding='utf8') as handle:json.dump(result,handle,ensure_ascii=False,indent=2)
        assert not any(row['errors'] for row in result['queries']+result['other_menu_conditions']), 'Native menu condition error; inspect perfect_strict_audit.json'
        renpy.quit(save=False)

    def _ssct_strict_tick(kind):
        state=sys.modules['ssct_strict_probe']
        if kind in ('corp','gate'):renpy.end_interaction(None)
        elif state.phase==0 and kind=='main_menu':
            state.phase=1
            renpy.load('quick-6')
        elif state.phase==1 and kind=='nav':
            state.phase=2
            _ssct_strict_run()
    def _ssct_strict_hook(original,kind):
        def hook(*args,**kwargs):
            original(*args,**kwargs)
            renpy.use_screen('ssct_strict_tick',kind=kind,_scope=kwargs.get('_scope',{}),_name=(kwargs.get('_name',()),'strict'))
        return hook
    import renpy.display.screen as screens
    for (name,variant),screen in tuple(screens.screens.items()):
        if name in ('main_menu','nav','corp','gate'):screen.function=_ssct_strict_hook(screen.function,name)
label ssct_strict_splash:
    return
screen ssct_strict_tick(kind):
    timer .2 repeat True action Function(_ssct_strict_tick,kind)
