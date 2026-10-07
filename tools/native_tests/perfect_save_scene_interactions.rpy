# Isolated-engine regression: actual rendered item controls and ambient assignment.
init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-perfect-mod-tests')
init 1000 python:
    import sys,types
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_scene_splash'
    state=types.ModuleType('ssct_scene_probe')
    state.phase=0
    sys.modules[state.__name__]=state
    def _ssct_scene_write():
        import json,os
        state=sys.modules['ssct_scene_probe']
        with open(os.path.join(config.basedir,'perfect_scene_interactions.json'),'w',encoding='utf8') as f:
            json.dump(state.result,f,indent=2)
    def _ssct_scene_label(name,abnormal):
        state=sys.modules['ssct_scene_probe']
        if state.phase==6 and (name==state.expected_label or name.startswith(state.expected_label+'.')):
            state.result['encounter_entry']={'native_label':name,'actor':state.expected_actor,
                'rendered_button_dispatched':True,'day':saga.time.date,
                'scope':'Native NPC encounter response or entry; not full dialogue playback'}
            assert saga.time.date==1
            _ssct_scene_write()
            renpy.quit(save=False)
    config.label_callbacks.append(_ssct_scene_label)
    def _ssct_scene_tick(kind):
        import importlib,json,os
        state=sys.modules['ssct_scene_probe']
        if kind in ('corp','gate'):
            renpy.end_interaction(None)
        elif state.phase==0 and kind=='main_menu':
            state.phase=1
            renpy.load('quick-6')
        elif kind=='nav' and state.phase==1:
            state.result={'version':config.version,'clock':saga.time.now,'items':[],'ambient':[]}
            assert saga.time.date==1
            state.items=['specs_lab','plans_ocular','costume_lab']
            state.index=0
            saga.cast.anon.where=saga.sets.school_office2
            saga.camera.last=saga.sets.school_office2
            saga.camera.focus=None
            state.phase=2
            renpy.end_interaction({})
        elif kind=='nav' and state.phase==2:
            if state.index<len(state.items):
                item=getattr(saga.prop,state.items[state.index])
                controls=[]
                screen=renpy.get_screen('use') or renpy.get_screen('nav')
                assert screen, 'Native navigation screen missing'
                displayables=[]
                screen.visit_all(displayables.append)
                for node in displayables:
                    action=getattr(node,'clicked',None)
                    if isinstance(action,Emit) and action.value.get('interact') is item and node.is_sensitive():
                        controls.append(action)
                assert controls, 'No rendered sensitive item button: '+item.ref
                state.result['items'].append({'ref':item.ref,'rendered_sensitive':True})
                state.phase=3
                renpy.end_interaction(controls[0].value)
            else:
                state.phase=4
                renpy.end_interaction({})
        elif kind=='nav' and state.phase==3:
            item=getattr(saga.prop,state.items[state.index])
            row=state.result['items'][-1]
            row['source_consumed']=_ssct_owned_origin(item) is None
            row['owned_once']=sum(obj is item for obj in saga.prop.anon_bag.sift(saga.prop))==1
            assert row['source_consumed'] and row['owned_once'],row
            state.index+=1
            state.phase=2
            renpy.end_interaction({})
        elif kind=='nav' and state.phase==4:
            # Native random selection/reservation; not a full encounter playthrough.
            stall=sys.modules.get('saga.logic.stall')
            from saga import step
            state.result['ambient_protocol_available']=stall is not None
            for name in ('pool_stall1','pool_stall2','pool_stall3') if stall is not None else ():
                place=getattr(saga.sets,name)
                stall.stall('swim',place)
                who=stall.find(place,'_swim')
                state.result['ambient'].append({'place':name,'actor':getattr(who,'ref',None),
                    'handler_attached':getattr(step,name) in saga.event.crowd})
            if stall is not None:
                assert any(row['actor'] for row in state.result['ambient']),state.result['ambient']
                assert all(row['handler_attached'] for row in state.result['ambient'])
                occupied=next(row for row in state.result['ambient'] if row['actor'])
                state.target=getattr(saga.sets,occupied['place'])
                state.expected_actor=occupied['actor']
                module=stall.pool[getattr(saga.cast,state.expected_actor)]
                state.expected_label=module.__name__.rsplit('.',1)[1]
                saga.cast.anon.where=saga.sets.pool_side
                saga.camera.last=saga.sets.pool_side
                saga.camera.focus=None
                state.phase=5
                renpy.end_interaction({})
            else:
                _ssct_scene_write()
                renpy.quit(save=False)
        elif kind=='nav' and state.phase==5:
            screen=renpy.get_screen('use') or renpy.get_screen('nav')
            displayables=[]
            screen.visit_all(displayables.append)
            controls=[node.clicked for node in displayables
                if isinstance(getattr(node,'clicked',None),Emit)
                and node.clicked.value.get('interact') is state.target and node.is_sensitive()]
            assert controls,'No rendered sensitive changing-stall entry'
            state.phase=6
            renpy.end_interaction(controls[0].value)
    def _ssct_scene_hook(original,kind):
        def hook(*args,**kwargs):
            original(*args,**kwargs)
            renpy.use_screen('ssct_scene_tick',kind=kind,_scope=kwargs.get('_scope',{}),_name=(kwargs.get('_name',()),'scene_probe'))
        return hook
    import renpy.display.screen as screens
    for (name,variant),screen in tuple(screens.screens.items()):
        if name in ('main_menu','nav','corp','gate'):
            screen.function=_ssct_scene_hook(screen.function,name)
label ssct_scene_splash:
    return
screen ssct_scene_tick(kind):
    timer .2 repeat True action Function(_ssct_scene_tick,kind)
