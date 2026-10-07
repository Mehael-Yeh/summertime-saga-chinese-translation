# Construct a native save from the running game's catalogue, not a playthrough.
default ssct_perfect_template = None
default ssct_perfect_generation = None
default ssct_perfect_displays = None
default ssct_perfect_inventory = None

init 998 python:
    _ssct_perfect_id = 'ssct-runtime-completion-v1'

    def _ssct_perfect_text(source):
        return renpy.translate_string(source).replace('{#ssct_perfect}', '')

    def _ssct_perfect_supported():
        return callable(getattr(renpy.loadsave.location, 'save', None))

    def _ssct_perfect_tooltip():
        if not _ssct_perfect_supported():
            return _ssct_perfect_text('The save-writing interface is unavailable.{#ssct_perfect}')
        return _ssct_perfect_text('Overwrite quick slot 6. Load the constructed save to unlock the gallery.{#ssct_perfect}')

    def _ssct_perfect_stages(route, steps):
        return tuple(node for node in steps if node.ref.startswith(route.ref)
            and node.ref[len(route.ref):].split('_', 1)[0].isdigit())

    def _ssct_perfect_terminal(route, stages, empty):
        # Native future-story placeholders have a hint, no event pool and a
        # terminal completion marker. Only the last registered quest number
        # can be a current endpoint; a retained older placeholder is completed.
        if not stages:
            return empty
        def quest(node):
            return int(node.ref[len(route.ref):].split('_', 1)[0])
        final_quest = max(quest(node) for node in stages)
        waiting = [node for node in stages if quest(node) == final_quest
            and getattr(node, 'done', None) is True
            and getattr(node, 'hint', None)
            and hasattr(node, 'pool') and not node.pool]
        if len(waiting)>1:
            raise ValueError('Ambiguous native future-story endpoints: ' + route.ref)
        return waiting[0] if waiting else empty

    def _ssct_perfect_open_targets(nodes, places):
        # Read native callbacks; do not execute arbitrary quest functions or
        # assume that marking a quest done runs its completion consequences.
        import dis
        known = {id(place): place for place in places}
        opened, visited = {}, set()
        pending = [entry[0] for node in nodes for entry in getattr(node, 'pool', ())]
        while pending:
            callback = pending.pop()
            while not hasattr(callback, '__code__') and hasattr(callback, 'func'):
                callback = callback.func
            code = getattr(callback, '__code__', None)
            if code is None or id(code) in visited:
                continue
            visited.add(id(code))
            globals_ = callback.__globals__
            defaults = getattr(callback, '__defaults__', None) or ()
            bound = dict(zip(code.co_varnames[code.co_argcount-len(defaults):code.co_argcount], defaults))
            instructions = [i for i in dis.get_instructions(callback)
                            if i.opname not in ('CACHE', 'EXTENDED_ARG', 'NOP')]
            for index, instruction in enumerate(instructions):
                if instruction.opname == 'LOAD_GLOBAL':
                    value = globals_.get(instruction.argval)
                    if callable(value) and getattr(value, '__module__', '').startswith('saga.logic.'):
                        pending.append(value)
                elif instruction.opname == 'LOAD_FAST':
                    value = bound.get(instruction.argval)
                else:
                    continue
                for attribute in instructions[index+1:]:
                    if attribute.opname not in ('LOAD_ATTR', 'LOAD_METHOD'):
                        break
                    if attribute.argval == 'open':
                        if id(value) in known:
                            opened[id(value)] = known[id(value)]
                        break
                    # Catalogue references are literal native attributes.
                    # Never evaluate view/plan properties while inspecting.
                    if value is not saga.sets:
                        break
                    value = getattr(value, attribute.argval, None)
        return tuple(opened.values())

    def _ssct_perfect_contacts(candidates):
        # A face/category also exists for incidental actors with no phone bio.
        # Only native profiles that can render the detail page are contacts.
        return [actor for actor in candidates
                if getattr(actor, 'type', None)
                and renpy.has_image('menu_cast_' + actor.ref + '_face')
                and isinstance(getattr(actor, 'info', None), tuple)
                and all(hasattr(actor, field) for field in ('name', 'age', 'kind', 'bio'))
                and (actor.kind != 'f' or hasattr(actor, 'size'))
                and renpy.loadable('art/mini/tel/info/outfit/' + actor.ref + '.png')]

    def _ssct_perfect_progression(completed, origins):
        from saga import cast, prop, sets
        opened = _ssct_perfect_open_targets(completed, tuple(sets))
        for place in opened:
            place.open()
        # Detail-page metadata and artwork must exist as well as the card.
        phone = prop.anon_phone
        contacts = _ssct_perfect_contacts(cast)
        # Some older native contacts have no surname field, while that release's
        # contact-card screen accesses it unconditionally. Preserve known names.
        for actor in contacts:
            if not hasattr(actor, 'clan'):
                actor.clan = ''
        phone.cast = renpy.revertable.RevertableList(contacts)
        # One native catalogue object per portable item. Delivered/equipped
        # objects retain their real owner; the bag also lists those same objects.
        items = []
        displays = renpy.revertable.RevertableDict(origins)
        actors = {id(actor) for actor in cast}
        for item in prop:
            if not _ssct_perfect_portable(item):
                continue
            owner, seen = getattr(item, 'where', None), set()
            while owner is not None and id(owner) not in seen:
                seen.add(id(owner))
                if id(owner) in actors:
                    break
                owner = getattr(owner, 'where', None)
            if id(owner) not in actors or owner is cast.anon:
                item.move(cast.anon)
            items.append(item.ref)
        prop.anon_bag.sift = cast.anon.sift
        store.ssct_perfect_inventory = renpy.revertable.RevertableSet(items)
        store.ssct_perfect_displays = displays
        return {'contacts': [actor.ref for actor in contacts],
                'opened_places': sorted(place.ref for place in opened),
                'inventory': [item.ref for item in prop.anon_bag.sift(prop)],
                'granted_portable_items': items}

    def _ssct_perfect_portable(item):
        return (any(base.__name__ == 'Collectable' for base in type(item).__mro__)
                and renpy.loadable('art/prop/' + item.ref + '/icon.png'))

    def _ssct_perfect_item_origins():
        from saga import prop, sets
        import importlib
        stock = importlib.import_module('saga.logic.shop').buyable
        containers = {id(obj): ('prop', obj.ref) for obj in prop}
        containers.update({id(obj): ('sets', obj.ref) for obj in sets})
        return {item.ref: containers[id(stock.get(item, getattr(item, 'where', None)))]
                for item in prop if _ssct_perfect_portable(item)
                and id(stock.get(item, getattr(item, 'where', None))) in containers}

    def _ssct_perfect_display_refs(what):
        if (getattr(store, 'ssct_perfect_template', None) != _ssct_perfect_id
                or not getattr(store, 'ssct_perfect_displays', None)
                or not hasattr(type(what), '__contains__')):
            return set()
        result = set(getattr(store, 'ssct_owned_cart', None).get(what.ref, ())) if getattr(store, 'ssct_owned_cart', None) else set()
        for ref, (catalogue, location) in store.ssct_perfect_displays.items():
            item = getattr(saga.prop, ref, None)
            owner = getattr(getattr(saga, catalogue), location, None)
            if item is None or owner is None or item.ref not in (store.ssct_perfect_inventory or ()):
                continue
            if owner is what or owner in what:
                result.add(ref)
        return result

    def _ssct_perfect_display_sift(what, defs):
        return _ssct_perfect_native_sift(what, defs) | _ssct_perfect_display_refs(what)

    def _ssct_perfect_display_view(what, attr=None):
        # Preserve native entities/actions as well as art. Native acquisition
        # moves the existing unique object and consumes its scene projection.
        # Do not clone items or temporarily spoof their real location to render.
        return _ssct_perfect_native_view(what, attr)

    def _ssct_perfect_reset_supported(callback):
        """Only actor-field resets and literal memory removal may run here."""
        import dis
        if not hasattr(callback,'__code__'):return False
        instructions=[op for op in dis.get_instructions(callback)
            if op.opname not in ('CACHE','EXTENDED_ARG','RESUME','PRECALL','NOP')]
        if any(op.opname in ('FOR_ITER','JUMP_BACKWARD','JUMP_BACKWARD_NO_INTERRUPT')
               for op in instructions):return False
        for index,op in enumerate(instructions):
            if op.opname.startswith('CALL'):
                if op.opname!='CALL':return False
                start=index-op.arg-1
                if start<1:return False
                method=instructions[start]
                owner=instructions[start-1]
                if not (method.opname in ('LOAD_ATTR','LOAD_METHOD') and method.argval=='remove'
                        and owner.opname=='LOAD_FAST' and owner.argval=='ctx'
                        and all(arg.opname=='LOAD_CONST' and isinstance(arg.argval,str)
                            for arg in instructions[start+1:index])):return False
        return True

    def _ssct_perfect_schedule():
        # New-game setup installs listeners but does not place the NPCs until
        # the first clock event. Dispatch native placement/venue callbacks
        # using the native argument protocol, without running story cutscenes.
        from saga import cast, sets
        event = saga.event
        event.emit(dow=saga.time.dow, tick=saga.time.now,
                   tod=saga.time.tod, skip=0)
        handlers = sorted(event.find(event.queue[-1]), key=lambda entry: entry[0])
        actor_refs = {actor.ref for actor in cast}
        place_ids = {id(place) for place in sets}
        dispatched = []
        for weight, ctx, args, callback, mutex in handlers:
            name = callback.__name__
            placement = (ctx.ref in actor_refs and name.startswith('move')
                         and name[4:].isdigit())
            daily_reset = ctx.ref in actor_refs and name == 'reset'
            if daily_reset:
                # The actor scheduling protocol may reset daily work/clothing
                # and transient memories, but must never run a story cutscene.
                if not _ssct_perfect_reset_supported(callback):
                    raise ValueError('Unsupported native actor reset protocol: '+ctx.ref)
            venue = name in ('busy', 'display') and id(ctx) in place_ids
            if not (placement or daily_reset or venue):
                continue
            kwargs = {key: value for key, value in args if key in callback._req}
            if callback._ctx:
                callback(ctx, **kwargs)
            else:
                callback(**kwargs)
            dispatched.append((ctx.ref, name))
        return {'callbacks': dispatched,
                'actors': {actor.ref: getattr(getattr(actor, 'where', None), 'ref', None)
                           for actor in cast}}

    def _ssct_perfect_construct():
        from saga import cast, flow, step, sets
        from saga.game import init as init_game
        # Native new-game setup installs the GUI, map and daily-life listeners.
        # Defaults alone leave an inert world even though a room can render.
        init_game()
        # The user-visible save starts on day one. Temporal gate scenarios
        # belong to isolated validation and must not change this saved clock.
        from saga.enum import tod
        saga.time.now = len(tuple(tod))
        steps = tuple(step)
        # First-arrival introductions are separate from numbered quests. A
        # completed world must not replay these before opening its venues.
        # Remove only native place-introduction listeners, not read history.
        introductions = []
        for place in sets:
            node = getattr(step, place.ref, None)
            if node is not None and any(
                    getattr(entry[0], '__module__', '') == 'saga.logic.once'
                    for entry in getattr(node, 'pool', ())):
                saga.event.detach(node)
                introductions.append(node.ref)
        prologue = getattr(step, 'prologue', None)
        if prologue is not None:
            saga.event.detach(prologue)
        routes = []
        completed = []
        for route in tuple(flow):
            stages = _ssct_perfect_stages(route, steps)
            if not stages:
                if hasattr(route,'done') and getattr(route,'step',None) not in (None,step.null):
                    raise ValueError('Unrecognized native quest-stage protocol: ' + route.ref)
                continue
            terminal = _ssct_perfect_terminal(route, stages,
                step.null if hasattr(route,'done') else None)
            if hasattr(route,'done'):
                route.done.update(s for s in stages if s is not terminal)
            completed.extend(s for s in stages if s is not terminal)
            route.next(terminal)
            if terminal is None or terminal is step.null:
                saga.event.detach(route)
            else:
                saga.event.attach(route)
            saga.event.detach(*(s for s in stages if s is not terminal))
            routes.append((route.ref, getattr(terminal,'ref',None), len(stages)))

        # NPC levels moved from flow entries to actors between these releases.
        # Select only entries that exist in this game's own catalogue.
        levels = []
        for actor in tuple(cast):
            prefix = actor.ref + '_level'
            candidates = [s for s in steps if s.ref.startswith(prefix)
                          and s.ref[len(prefix):].isdigit()]
            if not candidates:
                continue
            target = actor if hasattr(actor, 'step') else getattr(flow, actor.ref, None)
            if target is None:
                continue
            highest = max(candidates, key=lambda s: int(s.ref[len(prefix):]))
            target.step = highest
            levels.append((actor.ref, highest.ref))

        origins = _ssct_perfect_item_origins()

        # Project durable native quest consequences before selecting repeat states.
        completion_model = _ssct_completion_model(
            [route for route in flow if _ssct_perfect_stages(route,steps)], steps)
        _ssct_completion_place_entries(completion_model, steps)
        _ssct_completion_greetings(completion_model)
        _ssct_completion_apply(completion_model, steps)

        # Native event registration and repeat-state resets drive the model.
        _ssct_completion_repeat_states(completion_model)

        # Numbered quests omit independent repeatable childbirth endings.
        _ssct_completion_cycles(completion_model, steps)

        # Repeat scenes (e.g. pregnancy/clinic) also open places; they are not
        # numbered route quests. Include their registered native callbacks.
        progression = _ssct_perfect_progression(steps, origins)

        anon = cast.anon
        anon.name = 'Anon'
        anon.cash, anon.bank = 100000, 9990000
        anon.chr = anon.dex = anon.int = anon.str = 10
        anon.costume = 'casual'
        anon.move(sets.debbie_bed3)
        saga.camera.track = anon
        saga.camera.focus = None
        saga.camera.last = sets.debbie_bed3
        gui = getattr(flow, 'gui', None) or saga.gui
        gui.step = step.nav
        # Inventory grants precede the final native delivery postconditions.
        _ssct_completion_apply(completion_model, steps)
        # Qualification endings depend on actual final reward ownership,
        # after inventory grants and native delivery postconditions settle.
        _ssct_completion_device_states(completion_model, steps)
        progression['inventory'] = sorted(store.ssct_perfect_inventory)
        completion_report = _ssct_completion_validate(completion_model)
        activity_history = _ssct_completion_activity_history(steps)
        schedule = _ssct_perfect_schedule()
        saga.event.queue = renpy.revertable.RevertableList()
        saga.event.stack = renpy.revertable.RevertableList()
        saga.event.locks = renpy.revertable.RevertableSet()
        store.main_menu = False
        store.ssct_perfect_template = _ssct_perfect_id
        store.ssct_perfect_generation = {
            'version': config.version, 'routes': routes, 'npc_levels': levels,
            'gallery_refs': [scene.ref for scene in saga.lewd],
            'progression': progression,
            'completion_contract': completion_report,
            'schedule': schedule,
            'activity_date_history': activity_history,
            'completed_place_introductions': introductions,
            'completed_enter_programs': completion_model.get('place_entry_retirements',[]),
            'executed_dialogue': False, 'source': 'fresh current-engine defaults'}

    def _ssct_perfect_record():
        import io, json, time
        from renpy.compat import pickle
        from renpy.rollback import RollbackLog
        # Clean stores and execute native defaults in a disposable context.
        # StoreBackup restores the live objects, contexts and rollback history.
        backup = renpy.python.StoreBackup()
        contexts, log = renpy.game.contexts, renpy.game.log
        random_state = renpy.random.getstate()
        try:
            renpy.python.clean_stores()
            renpy.execute_default_statement(True)
            context = renpy.execution.Context(True, clear=True)
            renpy.game.contexts = [context]
            renpy.game.log = RollbackLog()
            context.goto_label('ssct_perfect_runtime_resume')
            renpy.game.log.begin(force=True)
            _ssct_perfect_construct()
            # Include the native #saga stores in the saved roots before starting
            # the resume checkpoint; begin() alone resets their change baseline.
            renpy.game.log.complete(False)
            # Loading rolls back to this checkpoint before resuming the label.
            # Capture it after construction so the room/state stay intact.
            renpy.game.log.begin(force=True)
            renpy.game.log.log[:] = renpy.game.log.log[-1:]
            roots = renpy.game.log.freeze(None)
            payload = pickle.dumps((roots, renpy.game.log))
            title = _ssct_perfect_text('Constructed save{#ssct_perfect}')
            metadata = {'_save_name': title, '_version': config.version,
                        '_renpy_version': list(renpy.version_tuple),
                        '_ctime': time.time(), '_game_runtime': 0,
                        'ssct_runtime_generation': store.ssct_perfect_generation}
            for callback in config.save_json_callbacks:
                callback(metadata)
            # Room artwork comes from this version, not a bundled screenshot.
            image = saga.easy.image(saga.camera.what.view[0][1])
            rendered = renpy.render(image, config.screen_width, config.screen_height, 0, 0)
            screenshot = io.BytesIO()
            surface = renpy.display.draw.screenshot(rendered)
            surface = renpy.display.scale.smoothscale(surface,
                (config.thumbnail_width, config.thumbnail_height))
            renpy.display.module.save_png(surface, screenshot, 0)
            return renpy.loadsave.SaveRecord(screenshot.getvalue(), title,
                json.dumps(metadata, ensure_ascii=False), payload)
        finally:
            renpy.game.contexts, renpy.game.log = contexts, log
            backup.restore()
            renpy.random.setstate(random_state)

    def _ssct_perfect_write():
        if not _ssct_perfect_supported():
            renpy.notify(_ssct_perfect_tooltip())
            return
        try:
            record = _ssct_perfect_record()
            # Canonical fixed slot: no QuickSave, rotation or page dependency.
            # SaveRecord writes atomically and uses the engine's save locations.
            renpy.loadsave.location.save('quick-6', record)
            renpy.loadsave.clear_slot('quick-6')
            renpy.restart_interaction()
            renpy.notify(_ssct_perfect_text('Constructed save written to quick slot 6.{#ssct_perfect}'))
        except Exception as error:
            renpy.log('SSCT constructed save write failed: %r' % error)
            renpy.notify(_ssct_perfect_text('Could not write the constructed save. See log.txt.{#ssct_perfect}'))

    def _ssct_perfect_after_load():
        if ssct_perfect_template != _ssct_perfect_id:
            return
        import time
        if getattr(store, 'ssct_perfect_inventory', None):
            saga.prop.anon_bag.sift = saga.cast.anon.sift
        # Repair previous constructed saves containing incidental actors with
        # no native detail page. Do not fabricate a biography or contact stats.
        phone = saga.prop.anon_phone
        phone.cast = renpy.revertable.RevertableList(_ssct_perfect_contacts(phone.cast))
        app = getattr(phone, 'app', None)
        if (getattr(app, 'ref', None) == 'info'
                and getattr(getattr(app, 'hdd', None), 'who', None) not in phone.cast):
            phone.init('cast')
        # Catalogue attributes can be reconstructed from the engine rather than
        # serialized as store fields. Reapply missing native card defaults here.
        for actor in saga.prop.anon_phone.cast:
            if not hasattr(actor, 'clan'):
                actor.clan = ''
        # Explicitly constructed records; these are not earned-play evidence.
        # Preserve existing timestamps, preferences and the cookies toggle.
        if persistent.lewd is None:
            persistent.lewd = {}
        added = set(getattr(persistent, '_ssct_constructed_gallery', None) or ())
        timestamp = time.time()
        for scene in saga.lewd:
            if scene.ref not in persistent.lewd:
                persistent.lewd[scene.ref] = timestamp
                added.add(scene.ref)
        persistent._ssct_constructed_gallery = sorted(added)
        renpy.save_persistent()

    def _ssct_perfect_attach(original):
        def with_star(*args, **kwargs):
            original(*args, **kwargs)
            renpy.use_screen('ssct_perfect_save_button',
                _scope=kwargs.get('_scope', {}),
                _name=(kwargs.get('_name', ()), 'ssct_perfect_star'))
        return with_star

init 999 python:
    import saga.display.view as _ssct_perfect_view_module
    from saga.entity import Viewable as _ssct_perfect_viewable
    _ssct_perfect_native_sift = _ssct_perfect_view_module.sift
    _ssct_perfect_native_view = _ssct_perfect_view_module.get
    _ssct_perfect_view_module.sift = _ssct_perfect_display_sift
    _ssct_perfect_viewable.view = property(_ssct_perfect_display_view)
    import renpy.display.screen as _ssct_perfect_screens
    for (_ssct_perfect_name, _ssct_perfect_variant), _ssct_perfect_screen in tuple(_ssct_perfect_screens.screens.items()):
        if _ssct_perfect_name == 'load':
            _ssct_perfect_screen.function = _ssct_perfect_attach(_ssct_perfect_screen.function)
    config.after_load_callbacks.append(_ssct_perfect_after_load)

label ssct_perfect_runtime_resume:
    jump loop

screen ssct_perfect_save_button():
    textbutton '\u2605':
        id 'ssct_perfect_star'
        align (.97, .03)
        xysize (80, 80)
        padding (8, 8)
        background Solid('#0007')
        hover_background Solid('#40566ecc')
        text_font 'DejaVuSans.ttf'
        text_size 48
        text_color '#ffd54f'
        text_align (.5, .5)
        sensitive _ssct_perfect_supported()
        alt _ssct_perfect_tooltip()
        tooltip _ssct_perfect_tooltip()
        action Function(_ssct_perfect_write)

    if GetTooltip():
        frame:
            xalign .86
            ypos 28
            xmaximum 640
            padding (18, 14)
            background Solid('#000d')
            text GetTooltip() size 24

translate zh_hans strings:
    old 'Constructed save{#ssct_perfect}'
    new '构造存档'

    old 'The save-writing interface is unavailable.{#ssct_perfect}'
    new '当前存档写入接口不可用'

    old 'Overwrite quick slot 6. Load the constructed save to unlock the gallery.{#ssct_perfect}'
    new '覆盖快速存档第6格；读取构造存档解锁图鉴'

    old 'Constructed save written to quick slot 6.{#ssct_perfect}'
    new '已将构造存档写入快速存档第6格'

    old 'Could not write the constructed save. See log.txt.{#ssct_perfect}'
    new '构造存档写入失败，请查看log.txt'
