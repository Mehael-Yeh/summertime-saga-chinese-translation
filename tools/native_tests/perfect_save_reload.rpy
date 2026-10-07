# Regression fixture: install only in an isolated official-game copy.
init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-perfect-mod-tests')
init 999 python:
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_perfect_reload_splash'
    config.predict_statements=0
    import sys,types
    _reload=types.ModuleType('ssct_perfect_reload_state')
    _reload.phase=0
    _reload.checks=[]
    sys.modules[_reload.__name__]=_reload
    def _ssct_entry_label(name,abnormal):
        import json,os
        with open(os.path.join(config.basedir,'world_entry_label.json'),'w',encoding='utf8') as f:
            json.dump({'label':name,'camera':repr(saga.camera.what),
                'queue':repr(saga.event.queue),'stack':repr(saga.event.stack)},f)
    config.label_callbacks.append(_ssct_entry_label)
    def _ssct_perfect_reload_tick(kind):
        import sys,os,json
        from saga import flow
        t=sys.modules['ssct_perfect_reload_state']
        with open(os.path.join(config.basedir,'world_entry_phase.json'),'w',encoding='utf8') as f:
            json.dump({'phase':t.phase,'expected':getattr(t,'expected',None),
                'visited':getattr(t,'visited',[]),'camera':repr(saga.camera.what),
                'mode':renpy.get_mode(),'tick_kind':kind},f)
        if t.phase in (20,33,37) and kind=='choice':
            items=renpy.get_screen('choice').scope['items']
            if t.phase in (33,37):
                accepted=next((item for item in items if item.caption.startswith(('Borrow ','Add to ','Buy items for $'))),None)
                assert accepted is not None,[item.caption for item in items]
                t.library_choices=getattr(t,'library_choices',[])+[accepted.caption]
                return renpy.run(accepted.action)
            if t.expected=='toy_shop':
                accepted=next((item for item in items if item.caption.startswith(('Add to ','Borrow ','Buy items for $[cash].'))),None)
                if accepted is not None:
                    if accepted.caption.startswith('Buy items for $'):
                        assert store.cash==0
                    t.native_purchase_captions=getattr(t,'native_purchase_captions',[])+[accepted.caption]
                    return renpy.run(accepted.action)
            cancel=next((item for item in items if item.caption in ('Put it back.','Leave it.')),None)
            assert cancel is not None,[item.caption for item in items]
            return renpy.run(cancel.action)
        if t.phase in (20,33,37) and renpy.get_mode() in ('pause','say'):
            return renpy.end_interaction(True)
        if t.phase==0 and kind=='main_menu':
            t.phase=1
            renpy.load('ssct-perfect-legacy-contacts')
        elif t.phase==1 and kind=='nav' and renpy.get_mode()=='screen':
            t.phase=2
            assert saga.camera.what is saga.sets.debbie_bed3
            assert all(scene.ref in persistent.lewd for scene in saga.lewd)
            assert persistent.lewd[next(iter(saga.lewd)).ref]==12345.0
            assert persistent.cookies is False
            assert ssct_perfect_template==_ssct_perfect_id
            assert saga.cast.maria.babies==1 and saga.cast.maria > 'baby'
            assert saga.cast.maria.womb.normal and not saga.cast.maria.baby
            assert saga.event.peek(choice='kitchen',who=saga.cast.maria)
            from saga import step
            if getattr(step,'mar_pantry',None) is not None:
                assert saga.event.peek(choice='pantry',who=saga.cast.maria)
            menu=renpy.game.script.namemap['maria_pizza_kitchen.choice']
            while not isinstance(menu,renpy.ast.Menu):menu=menu.next
            offered=[caption for caption,condition,block in menu.items
                if block is not None and renpy.python.py_eval(condition)]
            assert 'Fool around.' in offered,offered
            if getattr(step,'mar_cook',None) is not None:
                assert saga.event.peek(choice='cook',who=saga.cast.maria)
            t.checks.append({'native_maria_kitchen_menu_items':offered})
            import ast
            greetings=[]
            for statement in renpy.game.script.namemap.values():
                if not isinstance(statement,renpy.ast.If):continue
                for condition,block in statement.entries:
                    try:expr=ast.parse(condition,mode='eval').body
                    except (SyntaxError,TypeError):continue
                    if not isinstance(expr,ast.Compare) or len(expr.ops)!=1 or not isinstance(expr.ops[0],ast.Lt):continue
                    left=expr.left
                    if not (isinstance(left,ast.Attribute) and isinstance(left.value,ast.Attribute)
                        and isinstance(left.value.value,ast.Name) and left.value.value.id=='saga'
                        and left.value.attr=='cast' and isinstance(expr.comparators[0],ast.Constant)
                        and expr.comparators[0].value=='met'):continue
                    actor=getattr(saga.cast,left.attr,None)
                    if actor is None or getattr(step,actor.ref+'_level1',None) is None:continue
                    assert not (actor < 'met'),(actor.ref,condition)
                    greetings.append((actor.ref,statement.filename,statement.linenumber))
            assert len(greetings)>5
            t.checks.append({'native_first_meeting_conditions_false':greetings})
            for cycle in ssct_perfect_generation['completion_contract']['maternity']:
                mother=getattr(saga.cast,cycle['actor'])
                assert mother.babies==1 and mother.womb.normal and not mother.baby
                assert mother > 'baby'
            t.checks.append({'fresh_load_native_maternity_ends':ssct_perfect_generation['completion_contract']['maternity']})
            assert ssct_perfect_displays
            assert _ssct_perfect_display_refs(saga.prop.anon_bag)==set()
            with open(os.path.join(config.basedir,'legacy_contact_input.json'),encoding='utf8') as f:
                legacy=json.load(f)
            assert not (set(legacy['excluded']) & {actor.ref for actor in saga.prop.anon_phone.cast})
            assert {actor.ref for actor in saga.prop.anon_phone.cast}==set(legacy['included'])-set(legacy['excluded'])
            saved_app=saga.prop.anon_phone.app.ref
            # Some engines reconstruct app state at load. Exercise the guard
            # explicitly with the same invalid native profile at this boundary.
            saga.prop.anon_phone.init('info',mark=None,who=getattr(saga.cast,legacy['excluded'][0]))
            _ssct_perfect_after_load()
            assert saga.prop.anon_phone.app.ref=='cast'
            t.checks.append({'legacy_invalid_contacts_removed':legacy['excluded'],
                'reconstructed_app':saved_app,'invalid_info_reset_by_after_load_callback':True})
            renpy.change_language(None)
            assert _ssct_perfect_tooltip().endswith('gallery.')
            renpy.save('ssct-perfect-reloaded',extra_info='Fresh process / normal room')
            t.checks.append({'fresh_process_load_and_resave':True,'room':repr(saga.camera.what)})
            assert len(saga.prop.anon_phone.cast) > 4
            assert len(list(saga.prop.anon_bag.sift(saga.prop))) > 20
            saga.prop.anon_phone.init('cast')
            renpy.show_screen('tel', saga.prop.anon_phone)
            t.phase=11
            renpy.restart_interaction()
        elif t.phase==11 and kind=='nav' and renpy.get_mode()=='screen':
            assert renpy.get_screen('tel') is not None
            assert renpy.screenshot(os.path.join(config.basedir,'perfect_contacts.png'))
            renpy.hide_screen('tel')
            t.profiles=[(actor,language) for language in (None,'zh_hans')
                        for actor in saga.prop.anon_phone.cast]
            t.profile_index=0
            t.rendered_profiles=[]
            t.phase=13
            renpy.restart_interaction()
        elif t.phase==13 and kind=='nav' and renpy.get_mode()=='screen':
            if t.profile_index:
                actor,language=t.profiles[t.profile_index-1]
                assert renpy.get_screen('tel') is not None
                assert saga.prop.anon_phone.app.hdd.who is actor
                t.rendered_profiles.append((actor.ref,language))
                renpy.hide_screen('tel')
            if t.profile_index<len(t.profiles):
                actor,language=t.profiles[t.profile_index]
                renpy.change_language(language)
                # Native app initialization uses the contact read arguments.
                saga.prop.anon_phone.init('info',mark=None,who=actor)
                renpy.show_screen('tel',saga.prop.anon_phone)
                t.profile_index+=1
                renpy.restart_interaction()
                return
            t.checks.append({'all_native_contact_profiles_rendered':t.rendered_profiles})
            renpy.change_language(None)
            renpy.show_screen('inv', saga.prop.anon_bag)
            t.phase=12
            renpy.restart_interaction()
        elif t.phase==12 and kind=='nav' and renpy.get_mode()=='screen':
            assert renpy.get_screen('inv') is not None
            assert renpy.screenshot(os.path.join(config.basedir,'perfect_inventory.png'))
            t.checks.append({'native_contact_and_inventory_screens_rendered':True,
                'contacts':len(saga.prop.anon_phone.cast),
                'inventory':len(list(saga.prop.anon_bag.sift(saga.prop)))})
            renpy.hide_screen('inv')
            t.phase=2
            return renpy.run(Emit(interact=saga.prop.map_town))
        elif t.phase==2 and kind=='nav' and renpy.get_mode()=='screen':
            assert saga.camera.what is saga.prop.map_town
            t.phase=3
            targets=[e for e,p in saga.camera.what.view if e]
            assert saga.sets.car_main in targets
            assert saga.sets.bank_main in targets
            for ref in ('school_main','library_main','mall_main','forest_main','pizza_main'):
                place=getattr(saga.sets,ref,None)
                if place is not None: assert place in targets, ref
            t.checks.append({'native_map_navigation':True,'dealership_and_bank_available':True})
            # Generate while the live camera shows the town map, not the room.
            current_context=renpy.game.context()
            current_log=renpy.game.log
            current_where=saga.cast.anon.where
            _ssct_perfect_write()
            assert saga.camera.what is saga.prop.map_town
            assert saga.cast.anon.where is current_where
            assert renpy.game.context() is current_context and renpy.game.log is current_log
            t.checks.append({'in_game_map_generation_preserves_live_context':True})
            t.phase=4
            return renpy.load('quick-6')
        elif t.phase==4 and kind=='nav' and renpy.get_mode()=='screen':
            assert saga.camera.what is saga.sets.debbie_bed3
            t.checks.append({'generated_from_map_loads_into_room':True})
            t.phase=3
            return renpy.run(Emit(interact=saga.sets.debbie_main))
        elif t.phase==3 and kind=='nav' and renpy.get_mode()=='screen':
            t.checks.append({'return_home':repr(saga.camera.what)})
            t.destinations=[ref for ref in ('debbie_lobby','debbie_landing','debbie_bed2',
                'debbie_landing','debbie_lobby','debbie_main','pizza_main','pizza_shop','pizza_kitchen',
                'pizza_shop','pizza_main','car_main','car_shop','car_garage','car_shop',
                'car_lounge','car_shop','car_office','car_shop','car_main',
                'bank_main','bank_lobby','bank_hall','bank_office','bank_cubicle',
                'bank_office','bank_hall','bank_lobby','bank_main',
                'mall_main','mall_hall1','comic_shop','mall_hall1','store_aisle',
                'mall_hall1','mall_hall2','toy_shop','mall_hall2','gift_shop',
                'gift_apparel','gift_shop','mall_hall2','coffee_shop')
                if getattr(saga.sets,ref,None) is not None
                and getattr(saga.sets,ref).view]
            from saga import step
            import dis
            blocked=[]
            for ref in ('car_garage','car_lounge'):
                node=getattr(step,ref,None)
                if node not in saga.event.crowd:continue
                fn=node.pool[0][0]
                ins=[op for op in dis.get_instructions(fn) if op.opname not in ('CACHE','NOP','RESUME')]
                compared=False
                for index,op in enumerate(ins):
                    if op.opname=='COMPARE_OP' and op.argval=='<':
                        compared=True
                        right,cursor=_ssct_completion_expression(ins,index-1,fn.__globals__,{})
                        left,unused=_ssct_completion_expression(ins,cursor,fn.__globals__,{})
                        assert left is flow.jos and right is not None
                        if left < right:blocked.append(ref)
                        break
                if not compared:
                    assert not any(op.opname=='LOAD_GLOBAL' and op.argval=='clear' for op in ins)
                    assert any(op.opname=='LOAD_CONST' and op.argval==ref+'.block' for op in ins)
                    blocked.append(ref)
            t.destinations=[ref for ref in t.destinations if ref not in blocked]
            t.checks.append({'native_unimplemented_dealership_entry_blocks_preserved':blocked})
            t.visited=[]
            t.phase=20
            t.expected=t.destinations.pop(0)
            return renpy.run(Emit(interact=getattr(saga.sets,t.expected)))
        elif t.phase==20 and kind=='nav' and renpy.get_mode()=='screen':
            assert saga.camera.what is getattr(saga.sets,t.expected),(t.expected,repr(saga.camera.what))
            refs=_ssct_perfect_display_refs(saga.camera.what)
            interactive=[entity for entity,path in saga.camera.what.view
                if getattr(entity,'ref',None) in refs]
            if interactive and not getattr(t,'reclicked_'+t.expected,False):
                item=interactive[0]
                setattr(t,'reclicked_'+t.expected,True)
                t.reclicked_items=getattr(t,'reclicked_items',[])+[item.ref]
                t.item_count_before=len(list(saga.prop.anon_bag.sift(saga.prop)))
                t.reclicked_item=item
                if t.expected=='toy_shop':t.purchase_cash_before=saga.cast.anon.cash
                return renpy.run(Emit(interact=item))
            if t.expected=='toy_shop' and ssct_owned_cart and ssct_owned_cart.get(saga.gui.buy.ref):
                return renpy.run(Emit(interact=saga.cast.ivy))
            if getattr(t,'reclicked_item',None) is not None:
                assert t.reclicked_item.where is saga.cast.anon
                if t.expected=='toy_shop' or t.reclicked_item not in _ssct_owned_buyable:
                    assert t.reclicked_item.ref not in ssct_perfect_displays
                    assert t.reclicked_item not in [entity for entity,path in saga.camera.what.view]
                    t.checks.append({'consumed_scene_item_after_native_action':t.reclicked_item.ref})
                assert len(list(saga.prop.anon_bag.sift(saga.prop)))==t.item_count_before
                t.reclicked_item=None
                if t.expected=='toy_shop':
                    assert saga.cast.anon.cash==t.purchase_cash_before
                    assert not ssct_owned_cart
                    assert len(t.native_purchase_captions)==2
                    assert t.native_purchase_captions[-1]=='Buy items for $[cash].'
                    t.checks.append({'native_owned_checkout_ui':t.native_purchase_captions,
                        'cash_unchanged':True,'inventory_unique':True,'dialogue_result_stubbed':False})
            if t.expected=='toy_shop':
                import time
                if not getattr(t,'capture_after',None):t.capture_after=time.monotonic()+.8
                if time.monotonic()<t.capture_after:return
                assert renpy.screenshot(os.path.join(config.basedir,'perfect_retained_toy_shop.png'))
            t.visited.append(t.expected)
            if t.destinations:
                t.expected=t.destinations.pop(0)
                return renpy.run(Emit(interact=getattr(saga.sets,t.expected)))
            t.checks.append({'native_scene_entry_actions':t.visited})
            t.checks.append({'native_owned_item_repeat_interactions':getattr(t,'reclicked_items',[])})
            renpy.save('ssct-item-lifecycle',extra_info='Consumed scene item lifecycle')
            t.phase=23
            return renpy.load('ssct-item-lifecycle')
        elif t.phase==23 and kind=='nav' and renpy.get_mode()=='screen':
            assert not ssct_owned_cart
            assert t.reclicked_toy_shop
            consumed=[row['consumed_scene_item_after_native_action'] for row in t.checks
                if 'consumed_scene_item_after_native_action' in row]
            assert consumed
            for ref in consumed:
                item=getattr(saga.prop,ref)
                assert ref not in ssct_perfect_displays,ref
                assert sum(entry is item for entry in saga.prop.anon_bag.sift(saga.prop))==1
            t.checks.append({'item_lifecycle_save_reload':True,
                'consumed_projection_refs':sorted(set(t.reclicked_items)-set(ssct_perfect_displays))})
            t.phase=21
            saga.time.tick(1)
            return renpy.run(Emit())
        elif t.phase==21 and kind=='nav' and renpy.get_mode()=='screen':
            assert not saga.time.dawn
            assert saga.cast.tony.where is saga.sets.pizza_shop
            t.checks.append({'native_clock_advance':saga.time.now})
            t.phase=22
            return renpy.run(Emit(interact=saga.sets.sushi_shop))
        elif t.phase==22 and kind=='nav' and renpy.get_mode()=='screen':
            assert saga.camera.what is saga.sets.sushi_shop
            t.checks.append({'restaurant_entry_after_native_clock_advance':True})
            # Evaluate the actual native menu condition and its registered
            # callback, not only the constructed memoir/quest done flags.
            from saga import step
            tested_choices=[]
            for choice in ('kitchen','pantry'):
                expected=getattr(step,'mar_'+choice,None)
                if expected is None:continue
                tested_choices.append(choice)
                assert saga.event.peek(choice=choice,who=saga.cast.maria)
                saga.event.emit(choice=choice,who=saga.cast.maria)
                matches=list(saga.event.find(saga.event.queue[-1]))
                assert any(ctx is expected for weight,ctx,args,fn,mutex in matches)
                saga.event.queue.pop()
            t.checks.append({'fresh_load_maria_repeat_menu_callbacks':True,
                'babies':saga.cast.maria.babies,'post_native_clock':True,'choices':tested_choices})
            t.phase=30
            return renpy.run(Emit(interact=saga.sets.library_main))
        elif t.phase==30 and kind=='nav' and renpy.get_mode()=='screen':
            assert saga.camera.what is saga.sets.library_main
            t.phase=31
            return renpy.run(Emit(interact=saga.sets.library_lobby))
        elif t.phase==31 and kind=='nav' and renpy.get_mode()=='screen':
            assert saga.camera.what is saga.sets.library_lobby
            assert saga.prop.library_card.where is saga.cast.anon
            assert saga.prop.library_shelf not in saga.event.crowd
            t.phase=32
            return renpy.run(Emit(interact=saga.prop.library_shelf))
        elif t.phase==32 and kind=='nav' and renpy.get_mode()=='screen':
            assert saga.camera.what is saga.prop.library_shelf
            available=[entity for entity,path in saga.camera.what.view
                if entity is not None and getattr(entity,'cart',None) is saga.prop.library_books]
            assert available,'No library shelf book buttons rendered'
            t.library_book=available[0]
            t.library_cash=saga.cast.anon.cash
            t.library_count=sum(item is t.library_book for item in saga.prop.anon_bag.sift(saga.prop))
            t.checks.append({'native_card_holder_opens_library_books':True,'available_books':len(available)})
            t.phase=33
            return renpy.run(Emit(interact=t.library_book))
        elif t.phase==33 and kind=='nav' and renpy.get_mode()=='screen':
            assert hasattr(t,'library_choices'),'Borrow confirmation was not executed'
            assert ssct_owned_cart.get(saga.gui.buy.ref)
            t.phase=35
            # Shelf is a camera prop focus. Use the real hud_prop Back input;
            # treating it as a graph location creates an invalid navigation.
            return renpy.run(Emit(interact=None))
        elif t.phase==35 and kind=='nav' and renpy.get_mode()=='screen':
            assert saga.camera.what is saga.sets.library_lobby
            t.phase=37
            return renpy.run(Emit(interact=saga.cast.jane))
        elif t.phase==37 and kind=='nav' and renpy.get_mode()=='screen':
            assert len(t.library_choices)==2,t.library_choices
            assert t.library_book.where is saga.cast.anon
            assert saga.cast.anon.cash==t.library_cash
            assert sum(item is t.library_book for item in saga.prop.anon_bag.sift(saga.prop))==t.library_count==1
            assert t.library_book.ref not in ssct_perfect_displays
            remaining=[entity for entity,path in saga.prop.library_shelf.view if entity]
            assert t.library_book not in remaining
            t.checks.append({'native_card_holder_borrow_confirmed':t.library_book.ref,
                'confirmation':t.library_choices,'cash_unchanged':True,'inventory_unique':True,
                'scene_book_consumed':True,'dialogue_result_stubbed':False})
            with open(os.path.join(config.basedir,'perfect_mod_reload_test.json'),'w',encoding='utf-8') as f:json.dump(t.checks,f,ensure_ascii=False,indent=2)
            renpy.quit(save=False)
    def _ssct_perfect_reload_hook(original,kind):
        def hook(*args,**kwargs):
            original(*args,**kwargs)
            renpy.use_screen('ssct_perfect_reload_tick',kind=kind,_scope=kwargs.get('_scope',{}),_name=(kwargs.get('_name',()),'ssct_perfect_reload'))
        return hook
    import renpy.display.screen as _reload_screens
    for (n,v),s in tuple(_reload_screens.screens.items()):
        if n in ('main_menu','nav','use','choice','say'):s.function=_ssct_perfect_reload_hook(s.function,n)
    config.overlay_screens.append('ssct_perfect_reload_overlay')
    def _ssct_reload_pulse():
        return _ssct_perfect_reload_tick('choice' if renpy.get_screen('choice') is not None else 'overlay')
    def _ssct_reload_interaction():
        renpy.ui.timer(.1,action=Function(_ssct_reload_pulse),repeat=True)
    config.interact_callbacks.append(_ssct_reload_interaction)
label ssct_perfect_reload_splash:
    return
screen ssct_perfect_reload_tick(kind):
    timer .1 repeat True action Function(_ssct_perfect_reload_tick,kind)
screen ssct_perfect_reload_overlay():
    timer .1 repeat True action Function(_ssct_perfect_reload_tick,'overlay')
