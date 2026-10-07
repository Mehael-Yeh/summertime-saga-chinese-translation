# Regression fixture: install only in an isolated official-game copy.
init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-perfect-mod-tests')
init 1000 python:
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_perfect_test_splash'
    config.predict_statements=0
    persistent._preferences.language=None
    import sys,types
    _teststate=types.ModuleType('ssct_perfect_mod_teststate')
    _teststate.phase=0
    _teststate.checks=[]
    sys.modules[_teststate.__name__]=_teststate
    def _ssct_perfect_test_hash(slot):
        import hashlib,os
        matches=[os.path.join(config.savedir,n) for n in os.listdir(config.savedir) if n.startswith(slot+'-') and n.endswith('.save')]
        assert len(matches)==1,matches
        return hashlib.sha256(open(matches[0],'rb').read()).hexdigest()
    def saga_snapshot():
        import json,hashlib
        return hashlib.sha256(json.dumps({k:{key:repr(value) for key,value in v.items()} for k,v in renpy.python.store_dicts.items() if k.startswith('#saga.')},sort_keys=True).encode()).hexdigest()
    def _ssct_perfect_test_tick(kind):
        import sys,os,json
        from saga import flow
        t=sys.modules['ssct_perfect_mod_teststate']
        with open(os.path.join(config.basedir,'perfect_mod_phase.json'),'w') as f:json.dump(dict(phase=t.phase,kind=kind,mode=renpy.get_mode()),f)
        if kind in ('corp','gate'):renpy.end_interaction(None)
        elif t.phase==0 and kind=='main_menu':
            t.phase=1
            renpy.change_language(None)
            persistent.lewd={next(iter(saga.lewd)).ref:12345.0}
            persistent.cookies=False
            persistent._ssct_constructed_gallery=[]
            for i in range(1,7):renpy.save('quick-%d'%i,extra_info='fixture%d'%i)
            t.before={str(i):_ssct_perfect_test_hash('quick-%d'%i) for i in range(1,7)}
            t.gallery_before=dict(persistent.lewd or {})
            t.cookies_before=persistent.cookies
            t.current_name=saga.cast.anon.name
            t.saga_before=saga_snapshot()
            t.random_before=renpy.random.getstate()
            renpy.run(FilePage('quick'))
            renpy.run(ShowMenu('load'))
        elif t.phase==1 and kind=='load':
            t.phase=2
            button=renpy.get_displayable('load','ssct_perfect_star')
            assert button is not None
            assert _ssct_perfect_tooltip().startswith('Overwrite quick slot 6')
            t.checks.append({'load_button':True,'english_tooltip':_ssct_perfect_tooltip()})
            renpy.change_language('zh_hans')
            assert _ssct_perfect_tooltip().startswith('覆盖快速存档')
            t.checks.append({'chinese_tooltip':_ssct_perfect_tooltip()})
            def contains(d):
                return d is button or any(contains(c) for c in d.visit())
            def find_button(d):
                if isinstance(d,renpy.display.behavior.Button) and contains(d):return d
                for child in d.visit():
                    result=find_button(child)
                    if result:return result
            actual=find_button(renpy.get_screen('load').child)
            assert actual is not None
            t.random_before=renpy.random.getstate()
            record=_ssct_perfect_record()
            assert t.random_before==renpy.random.getstate()
            assert 'ssct_runtime_generation' in record.json
            assert record.extra_info == _ssct_perfect_text('Constructed save{#ssct_perfect}')
            renpy.run(actual.action)
            assert renpy.slot_json('quick-6')['_version']==config.version
            assert renpy.slot_json('quick-6')['ssct_runtime_generation']['version']==config.version
            t.after={str(i):_ssct_perfect_test_hash('quick-%d'%i) for i in range(1,7)}
            assert all(t.before[str(i)]==t.after[str(i)] for i in range(1,6))
            assert t.before['6']!=t.after['6']
            assert dict(persistent.lewd or {})==t.gallery_before
            assert saga.cast.anon.name==t.current_name
            current=_ssct_perfect_test_hash('quick-6')
            t.random_before=renpy.random.getstate()
            original=renpy.loadsave.SaveRecord
            def fail(*args,**kwargs):raise ValueError('intentional runtime generation failure')
            renpy.loadsave.SaveRecord=fail
            try:_ssct_perfect_write()
            finally:renpy.loadsave.SaveRecord=original
            assert current==_ssct_perfect_test_hash('quick-6')
            assert t.saga_before==saga_snapshot()
            assert t.random_before==renpy.random.getstate()
            t.checks.append({'runtime_failure_preserves_slot':True,'generation_preserves_live_game_and_gallery':True,'all_saga_store_values_preserved':True,'random_state_preserved':True})
            t.phase=3
            renpy.load('quick-6')
        elif t.phase==2 and kind=='save':
            t.phase=3
            try:displayable=renpy.get_displayable('save','ssct_perfect_star')
            except Exception:displayable=None
            assert displayable is None
            t.checks.append({'save_button_absent':True,'other_slots_unchanged':True,'gallery_not_changed_on_generation':True})
            renpy.load('quick-6')
        elif t.phase==3 and kind=='nav' and renpy.get_mode()=='screen':
            t.phase=4
            assert saga.cast.anon.where is saga.sets.debbie_bed3
            assert saga.camera.what is saga.sets.debbie_bed3
            assert ssct_perfect_template==_ssct_perfect_id
            assert all(s.ref in persistent.lewd for s in saga.lewd)
            assert persistent.cookies==t.cookies_before
            assert all(persistent.lewd[k]==v for k,v in t.gallery_before.items())
            # Independently check native hints/action pools, not a version table.
            from saga import step
            retired_programs=ssct_perfect_generation.get('completed_enter_programs',[])
            assert all(getattr(step,item['observer']) not in saga.event.crowd for item in retired_programs)
            t.checks.append({'native_place_program_retirements':retired_programs})
            tested_routes=[]
            for route in flow:
                nodes=[node for node in step if node.ref.startswith(route.ref)
                    and node.ref[len(route.ref):].split('_',1)[0].isdigit()]
                if not nodes:continue
                highest=max(int(node.ref[len(route.ref):].split('_',1)[0]) for node in nodes)
                endpoints=[node for node in nodes
                    if int(node.ref[len(route.ref):].split('_',1)[0])==highest
                    and getattr(node,'done',None) is True and getattr(node,'hint',None)
                    and hasattr(node,'pool') and not node.pool]
                assert route.step is (endpoints[-1] if endpoints else step.null if hasattr(route,'done') else None)
                if hasattr(route,'done'):
                    assert all(node in route.done for node in nodes if node is not route.step)
                assert route.step not in (None,step.null) or route not in saga.event.crowd
                tested_routes.append((route.ref,getattr(route.step,'ref',None),len(nodes)))
            assert tested_routes
            assert saga.cast.jenny > 'deal.pre'
            if getattr(step,'mar_cook',None) is not None:
                assert saga.event.peek(choice='cook',who=saga.cast.maria)
                assert step.mar_cook in saga.event.crowd
            for ref in ('bar_office','mel_office','tor_office','viv_office','deb_pool','deb_island','deb_laundry','jen_cam','jen_finger','jen_pool','jen_table','jen_visit'):
                node=getattr(step,ref,None)
                if node is not None:assert node in saga.event.crowd,ref
            report=ssct_perfect_generation['completion_contract']
            assert report['checked']>100 and not report['failures']
            t.checks.append({'completion_contract':report})
            assert saga.cast.maria > 'baby'
            assert saga.cast.maria.babies==1
            assert saga.cast.anon.babies>=saga.cast.maria.babies
            assert not saga.cast.maria.baby
            assert saga.cast.maria.womb.normal
            assert saga.cast.maria > 'baby.home'
            assert flow.mar_dark.step is step.mar_dark_tony
            assert saga.event.peek(choice='kitchen',who=saga.cast.maria)
            pantry=getattr(step,'mar_pantry',None)
            if pantry is not None:
                assert saga.event.peek(choice='pantry',who=saga.cast.maria)
            assert step.mar_kitchen in saga.event.crowd
            assert pantry is None or pantry in saga.event.crowd
            assert all(node not in saga.event.crowd for node in step if node.ref.startswith('mar_baby_'))
            t.checks.append({'maria_completed_maternity':{'babies':saga.cast.maria.babies,
                'pregnancy_state':saga.cast.maria.womb.state.ref,'active_baby':bool(saga.cast.maria.baby),
                'kitchen_repeat':True,'pantry_repeat':pantry is not None,'appointment_stage':flow.mar_dark.step.ref}})
            future_routes=[route for route in flow if getattr(getattr(route,'step',None),'hint',None)
                and hasattr(route,'done') and not route.step.pool]
            assert all(route in saga.event.crowd for route in future_routes)
            clock_before=saga.time.now
            venue_witnesses=[]
            for actor_ref,place_ref in (('tony','pizza_shop'),('maria','pizza_kitchen'),
                    ('josie','car_shop'),('tina','bank_cubicle'),('ivy','toy_shop'),('liu','bank_lobby')):
                actor=getattr(saga.cast,actor_ref,None)
                place=getattr(saga.sets,place_ref,None)
                if actor is not None and place is not None:
                    witness=None
                    from saga.enum import dow,tod
                    for offset in range(len(tuple(dow))*len(tuple(tod))):
                        saga.time.now=clock_before+offset
                        _ssct_perfect_schedule()
                        saga.event.queue.clear()
                        if actor.where is place and actor in [obj for obj,art in place.view]:
                            witness=saga.time.now
                            break
                    assert witness is not None,(actor_ref,'No legal calendar witness')
                    venue_witnesses.append((actor_ref,place_ref,witness))
            saga.time.now=clock_before
            _ssct_perfect_schedule()
            saga.event.queue.clear()
            assert saga.time.date==1,'Generated save calendar drift'
            t.checks.append({'venue_calendar_witnesses':venue_witnesses,'saved_day':saga.time.date})
            assert saga.prop.book_dict.where is saga.cast.anon
            retained_views=[]
            for what in tuple(saga.sets)+tuple(saga.prop):
                if not hasattr(what,'art') or not hasattr(type(what),'__contains__'):
                    continue
                if what.art not in _ssct_perfect_view_module.cache:
                    continue
                refs=_ssct_perfect_display_refs(what)
                if not refs:
                    continue
                originals={getattr(saga.prop,ref):getattr(saga.prop,ref).where for ref in refs}
                try:
                    for item in originals:
                        catalogue,ref=ssct_perfect_displays[item.ref]
                        item.where=getattr(getattr(saga,catalogue),ref)
                    expected=_ssct_perfect_native_view(what)
                    expected_paths=[path for entity,path in expected
                        if getattr(entity,'ref',None) in refs]
                finally:
                    for item,owner in originals.items():item.where=owner
                actual=what.view
                expected_owned=[(entity,path) for entity,path in expected
                    if getattr(entity,'ref',None) in refs]
                assert all(layer in actual for layer in expected_owned),(what.ref,expected_paths)
                assert all(item.where is owner for item,owner in originals.items())
                if expected_paths:retained_views.append((what.ref,expected_paths))
            assert retained_views
            t.checks.append({'retained_interactive_native_art':retained_views,
                'retained_native_acquisition_entities':True})
            t.checks.append({'native_npc_placement_and_visible_art':True,
                'native_future_hint_routes':[route.ref for route in future_routes],
                'unique_library_item_owned':True})
            # These are actual data used by the contact/inventory/map screens.
            expected_contacts={actor.ref for actor in saga.cast
                if getattr(actor,'type',None) and renpy.has_image('menu_cast_'+actor.ref+'_face')
                and isinstance(getattr(actor,'info',None),tuple)
                and all(hasattr(actor,field) for field in ('name','age','kind','bio'))
                and (actor.kind!='f' or hasattr(actor,'size'))
                and renpy.loadable('art/mini/tel/info/outfit/'+actor.ref+'.png')}
            assert {actor.ref for actor in saga.prop.anon_phone.cast}==expected_contacts
            assert len(expected_contacts)>4
            native_menu=renpy.game.script.namemap['shop.pay']
            while not isinstance(native_menu,renpy.ast.Menu):native_menu=native_menu.next
            with open(os.path.join(config.basedir,'item_menu_conditions.json'),'w',encoding='utf8') as f:
                json.dump([(caption,str(condition)) for caption,condition,block in native_menu.items],f,ensure_ascii=False)
            inventory={item.ref for item in saga.prop.anon_bag.sift(saga.prop)}
            for ref in ('bank_card','library_card','key_school','tool_shovel','tool_rod'):
                if hasattr(saga.prop,ref):assert ref in inventory,ref
            assert len(inventory)>20
            import importlib
            shop=importlib.import_module('saga.logic.shop')
            nav=importlib.import_module('saga.logic.nav')
            owned=[item for item in saga.prop if _ssct_perfect_portable(item)]
            assert inventory=={item.ref for item in owned},(sorted({item.ref for item in owned}-inventory),repr(type(saga.prop.anon_bag).__mro__),repr(saga.prop.anon_bag.sift))
            before_ids=[id(item) for item in saga.prop]
            before_queue=list(saga.event.queue)
            origins=dict(ssct_perfect_displays)
            positions={item:item.where for item in owned}
            buyables=[item for item in owned if item in shop.buyable
                and getattr(item,'cart',None) is not None and item.cost is not None]
            original_call=shop.call
            original_cash=saga.cast.anon.cash
            original_buy=flow.gui.buy
            cart_state={item.cart:getattr(item.cart,'hide',None) for item in buyables}
            native_calls=[]
            collected=[]
            try:
                # Native nav acquisition emits a real move, removes only this
                # scene projection and leaves one inventory catalogue object.
                for item in owned:
                    if item.ref not in origins or item in shop.buyable:continue
                    prior=len(saga.event.queue)
                    nav.take(interact=item)
                    assert item.where is saga.cast.anon
                    assert item.ref not in ssct_perfect_displays
                    assert len(saga.event.queue)>prior,item.ref
                    assert sum(entry is item for entry in saga.prop.anon_bag.sift(saga.prop))==1
                    collected.append(item.ref)
                    item.where=positions[item]
                    ssct_perfect_displays[item.ref]=origins[item.ref]
                # Put-back is a real native prompt with no ownership/visibility
                # change. Accepted add uses the native cart and move events.
                for item in buyables:
                    item.where=positions[item]
                    ssct_perfect_displays[item.ref]=origins[item.ref]
                    shop.call=lambda label,*args,**kwargs:native_calls.append((label,False)) or False
                    shop.take(interact=item)
                    assert item.where is positions[item] and item.ref in ssct_perfect_displays
                    shop.call=lambda label,*args,**kwargs:native_calls.append((label,args[0] if args else None)) or True
                    shop.take(interact=item)
                    assert item.where is item.cart and item in item.cart.sift()
                    assert item.ref not in ssct_perfect_displays
                    assert item.ref not in _ssct_perfect_display_refs(shop.buyable[item])
                    assert sum(entry is item for entry in saga.prop.anon_bag.sift(saga.prop))==1
                    cash_before=saga.cast.anon.cash
                    price=item.cost
                    shop.pay(interact=item.cart)
                    assert saga.cast.anon.cash==cash_before and item.cost==price
                    assert item.where is saga.cast.anon and not item.cart.sift()
                    assert item not in shop.buyable[item]
                    assert native_calls[-1][1]==0
                    item.where=positions[item]
                    ssct_perfect_displays[item.ref]=origins[item.ref]
                direct = next(item for item in owned if item.ref in origins and item not in shop.buyable)
                direct.move(saga.cast.anon)
                assert direct.ref not in ssct_perfect_displays
                assert direct.where is saga.cast.anon
                direct.where=positions[direct]
                ssct_perfect_displays[direct.ref]=origins[direct.ref]
                first=buyables[0]
                # Native cancel returns merchandise to its original stock;
                # the preowned inventory entry is still present exactly once.
                shop.call=lambda *args,**kwargs:True
                shop.take(interact=first)
                shop.call=lambda *args,**kwargs:False
                shop.pay(interact=first.cart)
                assert first.where is shop.buyable[first] and first in shop.buyable[first]
                assert sum(item is first for item in saga.prop.anon_bag.sift(saga.prop))==1
                shop.call=lambda *args,**kwargs:True
                shop.take(interact=first)
                shop.call=lambda *args,**kwargs:None
                shop.pay(interact=first.cart)
                assert first.where is first.cart and first.ref in ssct_owned_cart[first.cart.ref]
                shop.call=lambda *args,**kwargs:True
                shop._fence(area=(),interact=saga.sets.debbie_main)
                assert first.where is shop.buyable[first] and not ssct_owned_cart
                assert flow.gui.buy is None and saga.cast.anon.cash==original_cash
                # Without the constructed-save marker, ordinary saves retain
                # the native price, native stock and original acquisition.
                store.ssct_perfect_template=None
                shop.take(interact=first)
                cash_before=saga.cast.anon.cash
                shop.pay(interact=first.cart)
                assert saga.cast.anon.cash==cash_before-first.cost
                store.ssct_perfect_template=_ssct_perfect_id
                assert [id(item) for item in saga.prop]==before_ids
            finally:
                shop.call=original_call
                store.ssct_perfect_template=_ssct_perfect_id
                saga.cast.anon.cash=original_cash
                flow.gui.buy=original_buy
                for item,where in positions.items():item.where=where
                store.ssct_perfect_displays=renpy.revertable.RevertableDict(origins)
                store.ssct_owned_cart=None
                for cart,hidden in cart_state.items():
                    if hidden is not None:cart.hide=hidden
                saga.event.queue=renpy.revertable.RevertableList(before_queue)
            t.checks.append({'all_portable_inventory_refs':sorted(inventory),
                'real_native_scene_collection':collected,
                'real_native_cart_checkout_items':[item.ref for item in buyables],
                'native_dialogue_return_stubbed':True,
                'scene_consumed_on_collection_or_add':True,
                'native_script_direct_move_consumes_projection':True,
                'cancel_and_leave_restore_native_stock':True,
                'all_checkout_zero_price_unique_inventory':True,
                'ordinary_save_native_price_preserved':True,
                'unique_catalogue_instances_unchanged':True})
            for ref in ('school_main','library_main','diane_main','mall_main','pizza_main','forest_main'):
                if hasattr(saga.sets,ref):assert not getattr(saga.sets,ref).hide,ref
            assert saga.prop.tech_gpu.where is saga.prop.anon_pc
            assert saga.prop.toy_vibe.where is saga.cast.jenny
            t.checks.append({'contacts_complete':sorted(expected_contacts),'inventory_count':len(inventory),'inventory_items':sorted(inventory),'progression_places_visible':True,'delivered_items_preserved':True})
            t.checks.append({'native_route_endpoint_scan':tested_routes})
            renpy.take_screenshot()
            renpy.screenshot(os.path.join(config.basedir,'perfect_mod_room_zh.png'))
            for lang in (None,'zh_hans',None):
                renpy.change_language(lang)
                renpy.save('ssct-perfect-resave',extra_info='resave regression')
            t.checks.append({'runtime_generation':ssct_perfect_generation,'room':repr(saga.camera.what),'name':saga.cast.anon.name,'money':[saga.cast.anon.cash,saga.cast.anon.bank],'gallery_before':len(t.gallery_before),'gallery_unlocked':len(tuple(saga.lewd)),'cookies_preserved':True,'earned_timestamps_preserved':True,'routes_complete_or_future_terminal':True,'native_resaves':3})
            # Reproduce the prior overinclusive constructed contact list.
            original_contacts=saga.prop.anon_phone.cast
            legacy_contacts=[actor for actor in saga.cast if getattr(actor,'type',None)
                and renpy.has_image('menu_cast_'+actor.ref+'_face')]
            saga.prop.anon_phone.cast=renpy.revertable.RevertableList(legacy_contacts)
            invalid_contacts=[actor for actor in legacy_contacts if actor.ref not in expected_contacts]
            assert invalid_contacts
            saga.prop.anon_phone.init('info',mark=None,who=invalid_contacts[0])
            renpy.save('ssct-perfect-legacy-contacts',extra_info='prior incidental contacts regression')
            saga.prop.anon_phone.cast=original_contacts
            saga.prop.anon_phone.init('home')
            with open(os.path.join(config.basedir,'legacy_contact_input.json'),'w',encoding='utf8') as f:
                json.dump({'included':[actor.ref for actor in legacy_contacts],
                    'excluded':sorted({actor.ref for actor in legacy_contacts}-expected_contacts)},f)
            renpy.run(ShowMenu('save'))
        elif t.phase==4 and kind=='save':
            t.phase=5
            assert renpy.get_displayable('save','ssct_perfect_star') is None
            t.checks.append({'save_button_absent':True,'other_slots_unchanged':True})
            with open(os.path.join(config.basedir,'perfect_mod_test.json'),'w',encoding='utf-8') as f:json.dump(dict(version=config.version,checks=t.checks,before=t.before,after=t.after),f,ensure_ascii=False,indent=2)
            renpy.quit(save=False)
    def _ssct_perfect_test_hook(original,kind):
        def hook(*args,**kwargs):
            if kind=='nav':
                import json,os
                with open(os.path.join(config.basedir,'runtime_nav_diagnostic.json'),'w') as f:json.dump({'what':repr(saga.camera.what),'art':saga.camera.what.art,'where':repr(saga.cast.anon.where),'track':repr(saga.camera.track),'focus':repr(saga.camera.focus),'marker':ssct_perfect_template,'queue':repr(saga.event.queue),'stack':repr(saga.event.stack)},f)
            original(*args,**kwargs)
            renpy.use_screen('ssct_perfect_test_tick',kind=kind,_scope=kwargs.get('_scope',{}),_name=(kwargs.get('_name',()),'ssct_perfect_test'))
        return hook
    import renpy.display.screen as _test_screens
    for (n,v),s in tuple(_test_screens.screens.items()):
        if n in ('corp','gate','main_menu','load','save','nav'):s.function=_ssct_perfect_test_hook(s.function,n)
label ssct_perfect_test_splash:
    return
screen ssct_perfect_test_tick(kind):
    timer .3 repeat True action Function(_ssct_perfect_test_tick,kind)
