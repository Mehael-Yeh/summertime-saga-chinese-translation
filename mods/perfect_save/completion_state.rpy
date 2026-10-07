# Compile completed-quest consequences from the running native catalogue.
# This is a state projection, not execution of dialogue or arbitrary callbacks.
init 997 python:
    def _ssct_completion_activity_dates(callback, catalogues, clock, diagnostics=None):
        """Identify native date stamps and their explicit missing-history defaults.

        No native callback is run. Only an exact clock.date write qualifies;
        deadlines, durations and arbitrary integer fields are excluded.
        """
        import dis, functools, types, builtins
        supplied = {}
        while isinstance(callback, functools.partial) or (not hasattr(callback, '__code__') and hasattr(callback, 'func')):
            fn = callback.func
            if hasattr(fn, '__code__'):
                supplied.update(zip(fn.__code__.co_varnames, callback.args))
            supplied.update(callback.keywords or {})
            callback = fn
        while hasattr(callback, '__wrapped__'):
            callback = callback.__wrapped__
        if not hasattr(callback, '__code__'):
            return []
        code = callback.__code__
        defaults = callback.__defaults__ or ()
        bound = dict(zip(code.co_varnames[code.co_argcount-len(defaults):code.co_argcount], defaults))
        bound.update(zip(code.co_freevars, (cell.cell_contents for cell in (callback.__closure__ or ()))))
        bound.update(supplied)
        date = object()
        unknown = object()
        entities = {id(obj): obj for name in ('cast', 'prop', 'sets', 'flow') for obj in catalogues[name]}
        catalogue_ids = {id(value) for value in catalogues.values()}
        actors = {id(obj): obj for obj in catalogues['cast']}
        writes, missing = [], {}
        # Dynamic actor selection is admitted only from a referenced native
        # actor-to-module registry, not from a guessed character list.
        dynamic = {}
        for name in code.co_names:
            registry = callback.__globals__.get(name)
            if isinstance(registry, builtins.dict) and registry and all(
                    id(key) in actors and isinstance(value, types.ModuleType)
                    for key, value in registry.items()):
                dynamic.update({id(key): key for key in registry})
        def inspect(code, locals_):
            ins = [op for op in dis.get_instructions(code) if op.opname not in ('CACHE','EXTENDED_ARG','PRECALL','NOP')]
            def expression(end):
                if end < 0:return unknown, end
                op = ins[end]
                if op.opname == 'LOAD_CONST':return op.argval, end-1
                if op.opname == 'LOAD_GLOBAL':return callback.__globals__.get(op.argval, getattr(builtins, op.argval, unknown)), end-1
                if op.opname in ('LOAD_FAST','LOAD_DEREF'):return locals_.get(op.argval, unknown), end-1
                if op.opname in ('LOAD_ATTR','LOAD_METHOD'):
                    owner, cursor = expression(end-1)
                    if owner is clock and op.argval == 'date':return date, cursor
                    if id(owner) in catalogue_ids:return getattr(owner, op.argval, unknown), cursor
                    return unknown, cursor
                return unknown, end-1
            for index, op in enumerate(ins):
                if op.opname in ('STORE_FAST','STORE_DEREF'):
                    locals_[op.argval] = expression(index-1)[0]
                elif op.opname == 'STORE_ATTR':
                    owner, cursor = expression(index-1)
                    value, unused = expression(cursor)
                    if value is date and id(owner) in entities:
                        writes.append((owner, op.argval))
                elif op.opname == 'CALL' and op.arg == 3:
                    values, cursor = [], index-1
                    for unused in range(3):
                        value, cursor = expression(cursor)
                        values.insert(0, value)
                    method, unused = expression(cursor)
                    owner, field, value = values
                    if diagnostics is not None:
                        diagnostics.append((code.co_name,repr(method),repr(field),value is date,repr(value)))
                    if method is builtins.getattr and isinstance(field, str) and type(value) is int:
                        missing[field] = value
                    elif method is builtins.setattr and isinstance(field, str) and value is date:
                        targets = [owner] if id(owner) in entities else list(dynamic.values()) if owner is unknown else []
                        writes.extend((target, field) for target in targets)
            for child in code.co_consts:
                if isinstance(child, types.CodeType):inspect(child, dict(locals_))
        inspect(code, bound)
        result = {}
        for entity, field in writes:
            if field in missing:
                result[(id(entity), field)] = (entity, field, missing[field])
        return list(result.values())

    def _ssct_completion_activity_history(steps):
        # A completed constructed world has activity history before visible
        # day one. Backdate only discovered native activity stamps, preserving
        # the native probabilities, daily limits, reservations and callbacks.
        from saga.enum import dow
        history_days = len(tuple(dow))
        applied, seen = [], set()
        catalogues = _ssct_completion_catalogues()
        for node in steps:
            for entry in getattr(node, 'pool', ()):
                for entity, field, default in _ssct_completion_activity_dates(entry[0], catalogues, saga.time):
                    key = (id(entity), field)
                    if key in seen:continue
                    seen.add(key)
                    value = getattr(entity, field, default)
                    if type(value) is not int:
                        raise ValueError('Unknown native activity-date type: '+entity.ref+'.'+field)
                    setattr(entity, field, value-history_days)
                    applied.append((entity.ref, field, value, value-history_days))
        return applied

    def _ssct_completion_catalogues():
        from saga import cast, prop, sets, step, flow
        return dict(cast=cast, prop=prop, sets=sets, step=step, flow=flow)

    def _ssct_completion_script_returns(label):
        """Inspect literal/native-reference returns; never evaluate game expressions."""
        import ast
        variables={}
        def literal(expr):
            if isinstance(expr, ast.Constant):return expr.value
            if isinstance(expr,ast.Name):return variables.get(expr.id)
            if isinstance(expr, ast.Attribute):
                path=[]
                while isinstance(expr, ast.Attribute):
                    path.insert(0, expr.attr)
                    expr=expr.value
                if isinstance(expr, ast.Name) and expr.id == 'saga' and len(path)==2:
                    namespace=_ssct_completion_catalogues().get(path[0])
                    if namespace is not None:return getattr(namespace,path[1],None)
            return None
        pending=[renpy.game.script.namemap.get(label)]
        visited=set()
        values=set()
        returns=[]
        while pending:
            node=pending.pop()
            if node is None or id(node) in visited:continue
            visited.add(id(node))
            if isinstance(node, renpy.ast.Return) and getattr(node,'expression',None):
                returns.append(node.expression)
            if isinstance(node,renpy.ast.Python):
                try:
                    for expression in ast.walk(ast.parse(node.code.source)):
                        pairs=[]
                        if isinstance(expression,ast.Assign):
                            pairs=[(target.id,expression.value) for target in expression.targets if isinstance(target,ast.Name)]
                        elif isinstance(expression,ast.Call) and isinstance(expression.func,ast.Attribute) and isinstance(expression.func.value,ast.Name) and expression.func.value.id=='renpy' and expression.func.attr=='dynamic':
                            pairs=[(keyword.arg,keyword.value) for keyword in expression.keywords]
                        for name,expr in pairs:
                            value=literal(expr)
                            if isinstance(value,(str,int,float,bool)):
                                variables.setdefault(name,set()).add(value)
                except (SyntaxError,TypeError):pass
            for child in getattr(node,'block', ()) or ():
                pending.append(child)
            if isinstance(node, renpy.ast.If):
                for condition, block in node.entries:pending.extend(block)
            elif isinstance(node, renpy.ast.Menu):
                for caption,condition,block in node.items:
                    if block:pending.extend(block)
            elif isinstance(node, renpy.ast.Jump) and not node.expression:
                pending.append(renpy.game.script.namemap.get(node.target))
            elif isinstance(node, renpy.ast.Call) and not node.expression:
                pending.append(renpy.game.script.namemap.get(node.label))
        variables={key:frozenset(value) for key,value in variables.items()}
        for expression in returns:
            try:
                value=literal(ast.parse(expression,mode='eval').body)
                if isinstance(value,frozenset):values.update(value)
                elif value is not None:values.add(value)
            except (SyntaxError,TypeError):pass
        return frozenset(values)

    def _ssct_completion_script_choices(label):
        """Read literal native menu tags without executing a scene."""
        import ast
        pending=[renpy.game.script.namemap.get(label)]
        visited=set()
        choices=set()
        while pending:
            node=pending.pop()
            if node is None or id(node) in visited:continue
            visited.add(id(node))
            pending.extend(getattr(node,'block',()) or ())
            if isinstance(node,renpy.ast.If):
                for condition,block in node.entries:pending.extend(block)
            elif isinstance(node,renpy.ast.Menu):
                for args in getattr(node,'item_arguments',()) or ():
                    for name,expression in getattr(args,'arguments',()) or ():
                        if name!='_choice':continue
                        try:value=ast.literal_eval(expression)
                        except (ValueError,SyntaxError,TypeError):continue
                        if isinstance(value,str):choices.add(value)
                for caption,condition,block in node.items:
                    if block:pending.extend(block)
            elif isinstance(node,renpy.ast.Jump) and not node.expression:
                pending.append(renpy.game.script.namemap.get(node.target))
            elif isinstance(node,renpy.ast.Call) and not node.expression:
                pending.append(renpy.game.script.namemap.get(node.label))
        return frozenset(choices)

    def _ssct_completion_expression(instructions, end, globals_, locals_):
        """Resolve only literal/catalogue expressions; never call native code."""
        if end < 0:
            return None, -1
        op = instructions[end]
        if op.opname == 'LOAD_CONST':
            return op.argval, end - 1
        if op.opname == 'LOAD_GLOBAL':
            return globals_.get(op.argval), end - 1
        if op.opname == 'LOAD_FAST':
            return locals_.get(op.argval), end - 1
        if op.opname in ('LOAD_ATTR', 'LOAD_METHOD'):
            owner, start = _ssct_completion_expression(instructions, end - 1, globals_, locals_)
            if op.argval=='_choice' and owner is not None and owner is globals_.get('store') and '__script_choices__' in locals_:
                return locals_['__script_choices__'], start
            if owner is None:
                return None, start
            # Catalogue lookups and stored fields only; no computed plan/view.
            if any(owner is _ssct_completion_catalogues()[name] for name in ('cast', 'prop', 'sets', 'step', 'flow')):
                return getattr(owner, op.argval, None), start
            if owner is saga.time and op.argval in ('now','tod','dow','date','dawn','dark'):
                return getattr(owner,op.argval), start
            if type(owner).__module__.startswith('saga.enum') and op.argval=='ref':
                return getattr(owner,'ref'), start
            return getattr(owner, '__dict__', {}).get(op.argval), start
        if op.opname=='SET_UPDATE':
            value,start=_ssct_completion_expression(instructions,end-1,globals_,locals_)
            base,start=_ssct_completion_expression(instructions,start,globals_,locals_)
            return (base | value if isinstance(base,frozenset) and isinstance(value,frozenset) else None),start
        if op.opname=='CALL' and op.arg==1:
            value,start=_ssct_completion_expression(instructions,end-1,globals_,locals_)
            if start>=0 and instructions[start].opname in ('LOAD_ATTR','LOAD_METHOD') and instructions[start].argval=='intersection':
                owner,start=_ssct_completion_expression(instructions,start-1,globals_,locals_)
                if isinstance(owner,frozenset) and isinstance(value,frozenset):return owner & value,start
            return None,start
        if op.opname in ('BUILD_TUPLE', 'BUILD_LIST', 'BUILD_SET'):
            values = []
            start = end - 1
            for unused in range(op.arg):
                value, start = _ssct_completion_expression(instructions, start, globals_, locals_)
                values.insert(0, value)
            return (frozenset(values) if op.opname=='BUILD_SET' else tuple(values)), start
        if op.opname in ('FORMAT_VALUE', 'UNARY_NOT'):
            value, start = _ssct_completion_expression(instructions, end-1, globals_, locals_)
            if op.opname=='FORMAT_VALUE' and isinstance(value,frozenset):
                return frozenset(str(v) for v in value), start
            return (str(value) if op.opname == 'FORMAT_VALUE' and value is not None else None), start
        if op.opname in ('BINARY_OP', 'BUILD_STRING'):
            count = 2 if op.opname == 'BINARY_OP' else op.arg
            values, start = [], end-1
            for unused in range(count):
                value, start = _ssct_completion_expression(instructions, start, globals_, locals_)
                values.insert(0, value)
            if all(isinstance(v,str) or isinstance(v,frozenset) and all(isinstance(x,str) for x in v) for v in values) and (op.opname == 'BUILD_STRING' or op.argrepr == '+'):
                import itertools
                choices=[tuple(v) if isinstance(v,frozenset) else (v,) for v in values]
                results=frozenset(''.join(v) for v in itertools.product(*choices))
                return next(iter(results)) if len(results)==1 else results, start
            return None, start
        return None, end - 1

    def _ssct_completion_model(routes, steps, extra_contexts=()):
        import dis
        model = {'memo': {}, 'listeners': {}, 'deliveries': {}, 'grades': {},
                 'fields': {}, 'deleted_fields': set(), 'diaries': {}, 'device_tags': {}, 'prop_tags': {}, 'sources': [], 'dynamic': [],
                 'inspected_callbacks': [], 'unclassified_fields': [],
                 'unsupported_callbacks': [],
                 'initial_repeat_states': {item.ref: getattr(getattr(item, 'step', None), 'ref', None)
                     for item in _ssct_completion_catalogues()['flow'] if not hasattr(item, 'done')}}
        native = {id(obj): (name, obj.ref) for name in ('cast', 'prop', 'sets', 'step', 'flow')
                  for obj in _ssct_completion_catalogues()[name]}
        def address(obj):
            return native.get(id(obj))
        def record(source, kind, target, values):
            model['sources'].append((source, kind, target, values))
        contexts = [(route, _ssct_perfect_stages(route, steps)) for route in routes]
        # Normal NPC conversations also have durable first-meeting consequences.
        contexts += [(actor, tuple(node for node in steps
            if node.ref.startswith(actor.ref + '_level'))) for actor in saga.cast]
        # Device/item programs have independent completion states as well.
        contexts += [(item,tuple(node for node in steps if node.ref.startswith(item.ref+'_')))
            for item in saga.prop if getattr(item,'step',None) is not None]
        contexts += list(extra_contexts)
        expanded=set()
        for route, stages in contexts:
            # Numeric quest order, then the native catalogue's within-quest order.
            finite_stages=_ssct_perfect_stages(route,stages)
            if finite_stages and len(finite_stages)==len(stages):
                stages=sorted(stages,key=lambda node:int(node.ref[len(route.ref):].split('_',1)[0]))
            for node in stages:
                for entry in getattr(node, 'pool', ()):
                    callback = entry[0]
                    partials, seen_partials = [], set()
                    while not hasattr(callback, '__code__') and hasattr(callback, 'func'):
                        if id(callback) in seen_partials:break
                        seen_partials.add(id(callback))
                        partials.append((getattr(callback, 'args', ()), getattr(callback, 'keywords', None) or {}))
                        callback = callback.func
                    if not hasattr(callback, '__code__'):
                        model['unsupported_callbacks'].append((node.ref, getattr(callback, '__name__', type(callback).__name__)))
                        continue
                    if '_baby_' in node.ref and callback.__name__ not in ('home', 'post'):
                        continue
                    defaults = getattr(callback, '__defaults__', None) or ()
                    code = callback.__code__
                    bound = dict(zip(code.co_varnames[code.co_argcount-len(defaults):code.co_argcount], defaults))
                    bound.update(dict(entry[1]))
                    bound['ctx'] = route
                    for arguments, keywords in reversed(partials):
                        bound.update(zip(code.co_varnames[:code.co_argcount], arguments))
                        bound.update(keywords)
                    source = node.ref + '.' + callback.__name__
                    model['inspected_callbacks'].append(source)
                    ins = [i for i in dis.get_instructions(callback)
                           if i.opname not in ('CACHE', 'EXTENDED_ARG', 'NOP', 'RESUME')]
                    # Merge literal assignments across branch joins. A call's
                    # possible replies come from this engine's own script AST.
                    script_choices=set()
                    for call_index,call_op in enumerate(ins):
                        if call_op.opname!='CALL':continue
                        args,cursor=[],call_index-1
                        for unused in range(call_op.arg):
                            argument,cursor=_ssct_completion_expression(ins,cursor,callback.__globals__,bound)
                            args.insert(0,argument)
                        if cursor>=0 and ins[cursor].opname=='LOAD_GLOBAL' and ins[cursor].argval=='call' and args and isinstance(args[0],str):
                            script_choices.update(_ssct_completion_script_choices(args[0]))
                    bound['__script_choices__']=frozenset(script_choices)
                    assigned={}
                    for index,op in enumerate(ins):
                        if op.opname != 'STORE_FAST' or not index:continue
                        previous=ins[index-1]
                        value,unused=_ssct_completion_expression(ins,index-1,callback.__globals__,bound)
                        if previous.opname=='CALL' and isinstance(value,frozenset):
                            # A set of menu tags is one collection, not alternative
                            # scalar replies; retain its type for later *opts.
                            bound[op.argval]=value
                            continue
                        if previous.opname=='CALL':
                            cursor=index-2
                            arguments=[]
                            for unused in range(previous.arg):
                                argument,cursor=_ssct_completion_expression(ins,cursor,callback.__globals__,bound)
                                arguments.insert(0,argument)
                            if cursor>=0 and arguments:
                                fn=ins[cursor]
                                if fn.opname=='LOAD_GLOBAL' and fn.argval=='call' and isinstance(arguments[0],str):
                                    value=_ssct_completion_script_returns(arguments[0])
                        if value is not None:
                            choices=value if isinstance(value,frozenset) else (value,)
                            for choice in choices:
                                if isinstance(choice,(str,int,float,bool)) or address(choice):
                                    assigned.setdefault(op.argval,set()).add(choice)
                        for jump_index,jump in enumerate(ins[:index]):
                            if jump.opname=='JUMP_FORWARD' and jump.argval==op.offset and jump_index:
                                alternative,unused=_ssct_completion_expression(ins,jump_index-1,callback.__globals__,bound)
                                if isinstance(alternative,(str,int,float,bool)) or address(alternative):
                                    assigned.setdefault(op.argval,set()).add(alternative)
                    for key,values in assigned.items():
                        if values:bound[key]=next(iter(values)) if len(values)==1 else frozenset(values)
                    for index, op in enumerate(ins):
                        if op.opname in ('CALL','CALL_FUNCTION_EX'):
                            if op.opname=='CALL_FUNCTION_EX':
                                if op.arg:continue
                                expanded_tags,cursor=_ssct_completion_expression(ins,index-1,callback.__globals__,bound)
                                if not isinstance(expanded_tags,(tuple,frozenset)):continue
                                if cursor<0 or ins[cursor].argval not in ('put','remove'):continue
                                arguments=list(expanded_tags)
                            else:
                                arguments, cursor = [], index - 1
                            if cursor >= 0 and ins[cursor].opname == 'KW_NAMES':
                                continue
                            for unused in range(op.arg if op.opname=='CALL' else 0):
                                value, cursor = _ssct_completion_expression(ins, cursor, callback.__globals__, bound)
                                arguments.insert(0, value)
                            if cursor < 0:
                                continue
                            method = ins[cursor]
                            if method.opname in ('LOAD_ATTR', 'LOAD_METHOD') and method.argval in ('put', 'add', 'remove', 'move', 'write'):
                                owner, unused = _ssct_completion_expression(ins, cursor-1, callback.__globals__, bound)
                                target = address(owner)
                                if isinstance(owner,frozenset) and method.argval in ('put','remove'):
                                    for member in owner:
                                        where=address(member)
                                        if where and all(isinstance(flag,str) for flag in arguments):
                                            for flag in arguments:model['memo'][where+(flag,)]=method.argval=='put'
                                            record(source,method.argval,where,tuple(arguments))
                                    continue
                                if target is None:
                                    # Local quest pools/reservations are discarded with the completed quest.
                                    if method.argval == 'put':
                                        model['dynamic'].append((source, method.argval, 'target', tuple(arguments)))
                                    continue
                                device = target[0] == 'prop' and any(base.__name__ in ('PC', 'Computer') for base in type(owner).__mro__)
                                if device and method.argval in ('add', 'remove') and all(isinstance(flag, str) for flag in arguments):
                                    for flag in arguments:
                                        model['device_tags'][target + (flag,)] = method.argval == 'add'
                                    record(source, 'device-tag', target, tuple(arguments))
                                    continue
                                if target[0] == 'prop' and hasattr(owner,'tags') and method.argval in ('add','remove') and all(isinstance(flag,str) for flag in arguments):
                                    for flag in arguments:
                                        model['prop_tags'][target + (flag,)] = method.argval == 'add'
                                    record(source, 'prop-tag', target, tuple(arguments))
                                    continue
                                if method.argval in ('put', 'remove'):
                                    arguments=[value for argument in arguments
                                        for value in (argument if isinstance(argument,frozenset) else (argument,))]
                                    known = [v for v in arguments if isinstance(v, str)]
                                    if len(known) != len(arguments):
                                        model['dynamic'].append((source, method.argval, target, tuple(known)))
                                    for flag in known:
                                        model['memo'][target + (flag,)] = method.argval == 'put'
                                    record(source, method.argval, target, tuple(known))
                                elif method.argval == 'write' and target[0] == 'prop' and all(isinstance(v, str) for v in arguments):
                                    model['diaries'].setdefault(target, set()).update(arguments)
                                    record(source, 'diary', target, tuple(arguments))
                                elif method.argval == 'move' and target[0] == 'prop' and len(arguments) == 1:
                                    destination = address(arguments[0])
                                    if destination:
                                        model['deliveries'].pop(target, None)
                                    receiver = arguments[0]
                                    device = destination and destination[0] == 'prop' and any(base.__name__ in ('PC', 'Computer') for base in type(receiver).__mro__)
                                    if destination and (destination[0] == 'cast' or device) and destination != ('cast', 'anon'):
                                        model['deliveries'][target] = destination
                                        record(source, 'delivery', target, destination)
                            elif method.opname == 'LOAD_GLOBAL' and method.argval in ('attach', 'detach'):
                                for value in arguments:
                                    target = address(value)
                                    if target and target[0] in ('step', 'flow', 'cast'):
                                        model['listeners'][target] = method.argval == 'attach'
                                        record(source, method.argval, target, ())
                        elif op.opname == 'DELETE_ATTR':
                            owner, unused = _ssct_completion_expression(ins,index-1,callback.__globals__,bound)
                            target = address(owner)
                            if target and target[0] in ('prop','sets') and op.argval in ('noop','lock'):
                                field = target + (op.argval,)
                                model['fields'].pop(field,None)
                                model['deleted_fields'].add(field)
                                record(source,'delete-field',field,())
                            else:
                                model['unclassified_fields'].append((source,target,'delete:'+op.argval))
                        elif op.opname == 'STORE_ATTR':
                            owner, cursor = _ssct_completion_expression(ins, index-1, callback.__globals__, bound)
                            value, unused = _ssct_completion_expression(ins, cursor, callback.__globals__, bound)
                            target = address(owner)
                            if owner is route and op.argval == 'grade' and isinstance(value, str):
                                # Choose the native successful final grading branch.
                                if value == 'A+':
                                    model['grades'][route.ref] = value
                                    record(source, 'grade', ('flow', route.ref), (value,))
                            elif target and isinstance(value, bool) and (op.argval in ('lock', 'noop')
                                    or (op.argval == 'auto' and target[0] == 'prop' and any(base.__name__ in ('PC', 'Computer') for base in type(owner).__mro__))):
                                model['deleted_fields'].discard(target + (op.argval,))
                                model['fields'][target + (op.argval,)] = value
                                record(source, 'field', target + (op.argval,), (value,))
                            elif target and target[0] == 'cast' and op.argval == 'lust' and isinstance(value, (int, float)):
                                model['deleted_fields'].discard(target + (op.argval,))
                                model['fields'][target + (op.argval,)] = value
                                record(source, 'field', target + (op.argval,), (value,))
                            elif op.argval not in ('where', 'costume', 'mood', 'cash', 'bank', 'cast', 'step', 'wait', 'last', 'chat', 'plan'):
                                model['unclassified_fields'].append((source, target, op.argval))
            # Follow registered completion consequences to their own native
            # repeat programs, instead of maintaining character/event lists.
            for target,attached in tuple(model['listeners'].items()):
                if not attached or target in expanded:continue
                expanded.add(target)
                entity=getattr(_ssct_completion_catalogues()[target[0]],target[1])
                if target[0]=='flow' and not _ssct_perfect_stages(entity,steps):
                    family=tuple(node for node in steps if node.ref==getattr(entity.step,'ref',None)
                        or node.ref.startswith(entity.ref+'_'))
                    if family:contexts.append((entity,family))
                elif target[0]=='step' and not any(node is entity for route,nodes in contexts for node in nodes):
                    if '_baby_' not in entity.ref and not __import__('re').match(r'^[a-z]+[0-9]+_',entity.ref):
                        contexts.append((entity,(entity,)))
        return model

    def _ssct_completion_tv_accounts(model):
        """Persist the native remembered subscription, not a password UI bypass."""
        from saga.tech.television import Television, PPV
        accounts=[]
        for device in saga.prop:
            if not isinstance(device,Television):continue
            for number,channel in device.tuner.items():
                account=channel.freq
                if not isinstance(account,PPV) or account.dev is not device:continue
                # PPV.auto reads hdd; native surf uses auto to authenticate into
                # ram on each boot. Leave that session lifecycle to the game.
                device.hdd.add(account.freq)
                accounts.append((device.ref,number,account.freq))
        model['tv_accounts']=accounts

    def _ssct_completion_place_entries(model, steps):
        """Retire native presentation-only place programs that return clear.

        The native handler owns retirement: removing its observer also removes
        its temporary access guards. Do not invent a separate door flag or
        detach ambient/repeat programs without an explicit enter/clear contract.
        """
        import dis, re
        from saga.util.sentinel import clear, abort
        from saga.event import call as native_call
        from saga.logic.util import req as native_req
        places={id(place):place for place in saga.sets}
        ignored={'RESUME','CACHE','EXTENDED_ARG','NOP','PUSH_NULL','PRECALL'}
        allowed=tuple(getattr(renpy.ast,name) for name in
            ('Scene','Show','ShowLayer','Camera','Hide','Say','With','Pass') if hasattr(renpy.ast,name))
        resolved=[]
        for node in steps:
            for callback,requirements,mutex,weight in getattr(node,'pool',()):
                event=dict(requirements)
                trigger='enter' if 'enter' in event else 'interact'
                place=event.get(trigger)
                participants=[event[key] for key in ('what','who') if key in event]
                if id(place) not in places or any(actor is not saga.cast.anon for actor in participants):continue
                if trigger=='enter' and not participants:continue
                while not hasattr(callback,'__code__') and hasattr(callback,'func'):callback=callback.func
                if not hasattr(callback,'__code__'):continue
                ops=[op for op in dis.get_instructions(callback) if op.opname not in ignored]
                # A single native presence check may postpone a one-off scene.
                # Admit its exact guard protocol, not arbitrary predicate calls
                # or mutation-heavy first-meeting/quest handlers.
                if len(ops)>8:
                    prefix=ops[:9]
                    if [op.opname for op in prefix[:8]]!=['LOAD_GLOBAL','LOAD_GLOBAL','LOAD_ATTR','LOAD_GLOBAL','LOAD_ATTR','CALL','STORE_FAST','LOAD_FAST']:continue
                    if not prefix[8].opname.startswith('POP_JUMP') or not prefix[8].opname.endswith('IF_TRUE'):continue
                    start=10 if ops[9].opname=='RETURN_CONST' and ops[9].argval is None else 11 if [op.opname for op in ops[9:11]]==['LOAD_CONST','RETURN_VALUE'] and ops[9].argval is None else None
                    if start is None or start>=len(ops):continue
                    if callback.__globals__.get(prefix[0].argval) is not native_req or prefix[5].arg!=2:continue
                    if callback.__globals__.get(prefix[1].argval) is not saga.cast or callback.__globals__.get(prefix[3].argval) is not saga.sets:continue
                    if prefix[6].argval!=prefix[7].argval or prefix[8].argval!=ops[start].offset:continue
                    ops=ops[start:]
                names=[op.opname for op in ops]
                if names==['LOAD_GLOBAL','LOAD_CONST','CALL','POP_TOP','LOAD_GLOBAL','RETURN_VALUE']:
                    if callback.__globals__.get(ops[4].argval) is not clear:continue
                elif names==['LOAD_GLOBAL','LOAD_CONST','CALL','POP_TOP','LOAD_GLOBAL','LOAD_GLOBAL','BUILD_TUPLE','RETURN_VALUE']:
                    if ops[6].arg!=2 or callback.__globals__.get(ops[4].argval) is not abort or callback.__globals__.get(ops[5].argval) is not clear:continue
                else:continue
                if ops[2].arg!=1 or callback.__globals__.get(ops[0].argval) is not native_call:continue
                label=ops[1].argval
                statement=renpy.game.script.namemap.get(label) if isinstance(label,str) else None
                if not isinstance(statement,renpy.ast.Label):continue
                safe=True
                for child in statement.block:
                    if isinstance(child,allowed):continue
                    if isinstance(child,renpy.ast.Return) and child.expression in (None,'None'):continue
                    if isinstance(child,getattr(renpy.ast,'UserStatement',type(None))) and re.fullmatch(r'pause(?:\s+\d+(?:\.\d+)?)?',getattr(child,'line','')):continue
                    safe=False
                    break
                if not safe:continue
                target=('step',node.ref)
                model['listeners'][target]=False
                model['sources'].append((node.ref+'.'+callback.__name__,'presentation-entry-clear',target,(label,place.ref)))
                resolved.append({'observer':node.ref,'place':place.ref,'label':label,'trigger':trigger})
                break
        model['place_entry_retirements']=resolved

    def _ssct_completion_initial_interactions(model, steps):
        """Complete native one-off observers and guarded first-use markers.

        Keep repeat handlers registered. Never run callbacks, set read history,
        or infer completion from the name of an item or dialogue label.
        """
        import dis, re
        from saga.event import call as native_call
        native_transition=getattr(getattr(native_call,'__func__',native_call),'__globals__',{}).get('transition')
        from saga.logic.util import req as native_req
        from saga.util.sentinel import clear, abort
        catalogues=_ssct_completion_catalogues()
        props={id(item):item for item in catalogues['prop']}
        actors={id(actor):actor for actor in catalogues['cast']}
        allowed=tuple(getattr(renpy.ast,name) for name in
            ('Scene','Show','ShowLayer','Camera','Hide','Say','With','Pass') if hasattr(renpy.ast,name))
        def presentation(label):
            pending=[renpy.game.script.namemap.get(label)]
            seen=set()
            while pending:
                node=pending.pop()
                if node is None:return False
                if id(node) in seen:continue
                seen.add(id(node))
                if isinstance(node,allowed):continue
                if isinstance(node,renpy.ast.Label):pending.extend(node.block)
                elif isinstance(node,renpy.ast.Return):
                    if node.expression not in (None,'None'):return False
                elif isinstance(node,renpy.ast.If):
                    for condition,block in node.entries:pending.extend(block)
                elif isinstance(node,renpy.ast.Call) and not node.expression:
                    pending.append(renpy.game.script.namemap.get(node.label))
                elif isinstance(node,renpy.ast.Jump) and not node.expression:
                    pending.append(renpy.game.script.namemap.get(node.target))
                elif isinstance(node,getattr(renpy.ast,'UserStatement',type(None))) and re.fullmatch(
                        r'pause(?:\s+\d+(?:\.\d+)?)?|window\s+(?:show|hide)(?:\s+.*)?',getattr(node,'line','')):
                    continue
                else:return False
            return True
        completed=[]
        unresolved=[]
        markers=[]
        for node in steps:
            for callback,requirements,mutex,weight in getattr(node,'pool',()):
                while not hasattr(callback,'__code__') and hasattr(callback,'func'):callback=callback.func
                if not hasattr(callback,'__code__'):continue
                code=callback.__code__
                defaults=callback.__defaults__ or ()
                bound=dict(zip(code.co_varnames[code.co_argcount-len(defaults):code.co_argcount],defaults))
                bound.update(dict(requirements))
                bound['ctx']=node
                ins=[op for op in dis.get_instructions(callback) if op.opname not in
                     ('CACHE','EXTENDED_ARG','RESUME','NOP','PRECALL','PUSH_NULL')]
                calls=[]
                call_sites={}
                unsafe=False
                for index,op in enumerate(ins):
                    if op.opname in ('STORE_GLOBAL','STORE_DEREF','DELETE_ATTR','STORE_SUBSCR'):unsafe=True
                    if op.opname!='CALL':continue
                    call_sites[op.offset]=False
                    args,cursor=[],index-1
                    for unused in range(op.arg):
                        value,cursor=_ssct_completion_expression(ins,cursor,callback.__globals__,bound)
                        args.insert(0,value)
                    if cursor<0:unsafe=True;continue
                    method=ins[cursor]
                    if method.opname=='LOAD_GLOBAL':
                        function=callback.__globals__.get(method.argval)
                        if function is native_call and args and isinstance(args[0],str):
                            calls.append(args[0]);call_sites[op.offset]=True
                        elif function is not native_req and function is not native_transition:unsafe=True
                    elif method.opname in ('LOAD_ATTR','LOAD_METHOD') and method.argval=='move':
                        owner,unused=_ssct_completion_expression(ins,cursor-1,callback.__globals__,bound)
                        if id(owner) not in actors:unsafe=True
                    else:unsafe=True
                # The native module explicitly owns these independent one-shot
                # programs. Its terminal clear, not a guessed flag, retires them.
                if callback.__module__=='saga.logic.once':
                    terminal=None
                    if ins and ins[-1].opname=='RETURN_VALUE':
                        terminal,unused=_ssct_completion_expression(ins,len(ins)-2,callback.__globals__,bound)
                    values=terminal if isinstance(terminal,tuple) else (terminal,)
                    writes=[op.argval for op in ins if op.opname=='STORE_ATTR']
                    returns=[op for op in ins if op.opname.startswith('RETURN')]
                    missing=[label for label in calls if label not in renpy.game.script.namemap]
                    if not unsafe and (not missing or not writes) and len(returns)==1 and clear in values and all(
                            value is clear or value is abort for value in values) and calls and all(
                            presentation(label) or label in missing for label in calls) and all(field in ('costume','where') for field in writes):
                        target=('step',node.ref)
                        model['listeners'][target]=False
                        model['sources'].append((node.ref+'.'+callback.__name__,'native-one-off-clear',target,tuple(calls)))
                        completed.append({'observer':node.ref,'labels':calls,'event_keys':sorted(dict(requirements)),
                            'missing_presentation_labels':missing})
                    else:unresolved.append({'observer':node.ref,'callback':callback.__name__,'reason':'unclassified_native_one_off'})
                # A repeated action can contain one initial presentation guarded
                # by a stored boolean. Project that marker without detaching it.
                for index,op in enumerate(ins):
                    if op.opname!='STORE_ATTR':continue
                    owner,cursor=_ssct_completion_expression(ins,index-1,callback.__globals__,bound)
                    value,unused=_ssct_completion_expression(ins,cursor,callback.__globals__,bound)
                    if id(owner) not in props or value is not True or type(
                            getattr(owner,'__dict__',{}).get(op.argval)) is not bool:continue
                    guarded=False
                    for guard_index,guard in enumerate(ins[:index]):
                        if guard.opname!='LOAD_ATTR' or guard.argval!=op.argval:continue
                        checked,unused=_ssct_completion_expression(ins,guard_index-1,callback.__globals__,bound)
                        if checked is owner and guard_index+1<len(ins) and ins[guard_index+1].opname=='POP_JUMP_IF_TRUE':
                            destination=ins[guard_index+1].argval
                            branch_calls=[safe for offset,safe in call_sites.items() if guard.offset<offset<op.offset]
                            guarded=op.offset<destination and bool(branch_calls) and all(branch_calls)
                    if not guarded or not calls or not all(presentation(label) for label in calls):continue
                    target=('prop',owner.ref,op.argval)
                    model['fields'][target]=True
                    model['sources'].append((node.ref+'.'+callback.__name__,'first-use-marker',target,tuple(calls)))
                    markers.append(list(target))
        model['one_off_retirements']=completed
        model['unresolved_one_offs']=unresolved
        model['first_use_markers']=markers

    def _ssct_completion_repeat_states(model):
        """Settle pure native reset transitions without running story callbacks."""
        import dis
        settled={}
        native_steps={id(node):node for node in _ssct_completion_catalogues()['step']}
        for (catalogue,ref),attached in model['listeners'].items():
            if not attached or catalogue!='flow':continue
            listener=getattr(_ssct_completion_catalogues()['flow'],ref)
            if _ssct_perfect_stages(listener,_ssct_completion_catalogues()['step']):continue
            visited=set()
            while id(listener.step) not in visited:
                visited.add(id(listener.step))
                destinations=[]
                for entry in getattr(listener.step,'pool',()):
                    fn=entry[0]
                    if not hasattr(fn,'__code__'):continue
                    ins=[i for i in dis.get_instructions(fn) if i.opname not in ('CACHE','RESUME','NOP')]
                    if any(op.opname.startswith(('CALL','JUMP','POP_JUMP','STORE')) for op in ins):continue
                    for index,op in enumerate(ins):
                        if op.opname=='RETURN_VALUE':
                            value,unused=_ssct_completion_expression(ins,index-1,fn.__globals__,{})
                            if id(value) in native_steps:destinations.append(value)
                if len({id(node) for node in destinations})!=1:break
                listener.step=destinations[0]
            settled[ref]=listener.step.ref
        model['repeat_states']=settled

    def _ssct_completion_greetings(model):
        """Infer first/repeat encounter memory from native sibling branches."""
        import ast
        seen=set()
        for statement in renpy.game.script.namemap.values():
            if not isinstance(statement,renpy.ast.If):continue
            following=getattr(statement,'next',None)
            repeated=isinstance(following,renpy.ast.Jump) and not following.expression and following.target.endswith('2')
            prefix=following.target[:-1] if repeated else None
            for condition,block in statement.entries:
                topology=repeated and any(isinstance(child,renpy.ast.Jump) and not child.expression
                           and child.target==prefix+'1' for child in block)
                try:expr=ast.parse(condition,mode='eval').body
                except (SyntaxError,TypeError):continue
                if not isinstance(expr,ast.Compare) or len(expr.ops)!=1 or not isinstance(expr.ops[0],ast.Lt):continue
                owner=expr.left
                if not (isinstance(owner,ast.Attribute) and isinstance(owner.value,ast.Attribute)
                        and isinstance(owner.value.value,ast.Name) and owner.value.value.id=='saga'
                        and owner.value.attr=='cast' and isinstance(expr.comparators[0],ast.Constant)
                        and isinstance(expr.comparators[0].value,str)):continue
                actor=getattr(saga.cast,owner.attr,None)
                if actor is None:continue
                flag=expr.comparators[0].value
                # Native 'met' is the common encounter-memory protocol; other
                # memories need an explicit initial/repeat branch topology.
                if not topology and flag!='met':continue
                if not any(node.ref.startswith(actor.ref+'_level') for node in _ssct_completion_catalogues()['step']):continue
                target=('cast',actor.ref,flag)
                if target in seen:continue
                seen.add(target)
                model['memo'][target]=True
                model['sources'].append((str(statement.filename)+':'+str(statement.linenumber),
                    'greeting',target,(following.target if repeated else 'native encounter memory',)))
        model['greetings']=[list(value) for value in sorted(seen)]

    def _ssct_completion_device_states(model, steps):
        """Follow acyclic device setup edges into its stable native state."""
        import dis
        from saga.util.sentinel import clear
        states={}
        terminals=[]
        for device in saga.prop:
            current=getattr(device,'step',None)
            if current is None:continue
            family={id(node):node for node in steps if node.ref.startswith(device.ref+'_')}
            if id(current) not in family:continue
            visited=set()
            while id(current) not in visited:
                visited.add(id(current))
                choices={}
                terminal=None
                for entry in getattr(current,'pool',()):
                    fn=entry[0]
                    if not hasattr(fn,'__code__'):continue
                    defaults=fn.__defaults__ or ()
                    code=fn.__code__
                    bound=dict(zip(code.co_varnames[code.co_argcount-len(defaults):code.co_argcount],defaults))
                    bound.update(dict(entry[1]))
                    bound['ctx']=device
                    ins=list(dis.get_instructions(fn))
                    acquired_at=None
                    for index,op in enumerate(ins):
                        if op.opname=='CALL' and op.arg==1:
                            recipient,cursor=_ssct_completion_expression(ins,index-1,fn.__globals__,bound)
                            if cursor>=0 and ins[cursor].opname in ('LOAD_ATTR','LOAD_METHOD') and ins[cursor].argval=='move':
                                reward,unused=_ssct_completion_expression(ins,cursor-1,fn.__globals__,bound)
                                if recipient is saga.cast.anon and reward is not None and getattr(reward,'where',None) is recipient:
                                    acquired_at=index
                        if op.opname!='RETURN_VALUE':continue
                        result,unused=_ssct_completion_expression(ins,index-1,fn.__globals__,bound)
                        values=result if isinstance(result,tuple) else (result,)
                        # An already acquired native reward proves the successful
                        # branch only when it leads straight to the clear sentinel.
                        # Keep retry/ambiguous/dynamic branches intact.
                        if acquired_at is not None and any(value is clear for value in values) and not any(
                                instruction.opname.startswith(('JUMP','POP_JUMP','STORE')) or instruction.opname=='CALL'
                                for instruction in ins[acquired_at+1:index]):
                            terminal=fn.__name__
                        for value in result if isinstance(result,tuple) else (result,):
                            if id(value) in family and value is not current:choices[id(value)]=value
                if terminal is not None:
                    terminals.append((device.ref,current.ref,terminal))
                    # Native Event handles clear by detaching the observer,
                    # retaining its step. None would make Flow.send invalid.
                    saga.event.detach(device)
                    model.setdefault('listeners',{})[('prop',device.ref)]=False
                    break
                if len(choices)!=1:break
                candidate=next(iter(choices.values()))
                if id(candidate) in visited:break
                current=candidate
            device.step=current
            states[device.ref]=getattr(current,'ref',None)
        model['device_states']=states
        model['acquired_terminals']=terminals

    def _ssct_completion_cycles(model, steps):
        """Identify implemented childbirth endings from native reset/return code."""
        import dis
        catalogues = _ssct_completion_catalogues()
        cycles = []
        for node in steps:
            if not node.ref.endswith('_baby_post'):
                continue
            post = next((entry[0] for entry in getattr(node, 'pool', ())
                         if getattr(entry[0], '__name__', '') == 'post'), None)
            if post is None or not hasattr(post, '__code__'):
                continue
            if not {'baby', 'reset'}.issubset(set(post.__code__.co_names)):
                continue
            endings = []
            ins = list(dis.get_instructions(post))
            for index, op in enumerate(ins):
                if op.opname == 'RETURN_VALUE' and index:
                    value, unused = _ssct_completion_expression(ins, index-1, post.__globals__, {})
                    if value is not None and getattr(value, 'ref', '').endswith('_level1'):
                        endings.append(value)
            if len(endings) != 1:
                raise ValueError('Unresolved native maternity ending: ' + node.ref)
            level = endings[0]
            mother = getattr(catalogues['cast'], level.ref[:-len('_level1')], None)
            if mother is None or not hasattr(mother, 'baby'):
                raise ValueError('Missing native maternity actor: ' + node.ref)
            # An unimplemented relationship must not inherit another release's ending.
            if not mother > 'sex':
                continue
            prefix = node.ref[:-len('post')]
            home = getattr(catalogues['step'], prefix + 'home', None)
            stages = ((home,) if home is not None else ()) + (node,)
            extra = _ssct_completion_model([], steps=(), extra_contexts=((mother, stages),))
            for key in ('memo', 'listeners', 'deliveries', 'fields', 'diaries', 'device_tags', 'prop_tags'):
                for target, value in extra[key].items():
                    if key == 'diaries':model[key].setdefault(target, set()).update(value)
                    else:
                        model[key][target] = value
                        if key=='fields':model['deleted_fields'].discard(target)
            for target in extra['deleted_fields']:
                model['fields'].pop(target,None)
                model['deleted_fields'].add(target)
            for key in ('sources', 'dynamic', 'inspected_callbacks', 'unclassified_fields', 'unsupported_callbacks'):
                model[key].extend(extra[key])
            # Reset only the registered cycle; normal future conception remains enabled.
            mother.baby.reset()
            mother.babies = max(getattr(mother, 'babies', 0), 1)
            state = mother if hasattr(mother, 'step') else getattr(catalogues['flow'], mother.ref)
            state.step = level
            chat = getattr(state, 'chat', None)
            if chat is not None:
                state.chat -= {value for value in chat if str(value).startswith('baby.')}
            for active in steps:
                if active.ref.startswith(prefix):
                    saga.event.detach(active)
                    model['listeners'][('step', active.ref)] = False
            cycles.append({'actor': mother.ref, 'post': node.ref, 'level': level.ref,
                           'babies': mother.babies})
        if cycles:
            total = sum(row['babies'] for row in cycles)
            saga.cast.anon.babies = max(getattr(saga.cast.anon, 'babies', 0), total)
            board = getattr(saga.prop, 'lucy_board', None)
            if board is not None and hasattr(board, 'count'):
                board.count = total
        model['maternity'] = cycles

    def _ssct_completion_apply(model, steps):
        import re
        def resolve(target):
            return getattr(_ssct_completion_catalogues()[target[0]], target[1])
        for (catalogue, ref, flag), present in model['memo'].items():
            entity = resolve((catalogue, ref))
            if present:
                entity.put(flag)
            else:
                entity.remove(flag)
        for (catalogue, ref, flag), present in model.get('device_tags', {}).items():
            entity = resolve((catalogue, ref))
            if present:entity.add(flag)
            else:entity.remove(flag)
        for (catalogue, ref, flag), present in model.get('prop_tags', {}).items():
            entity = resolve((catalogue, ref))
            if present:entity.add(flag)
            else:entity.remove(flag)
        for catalogue, ref, field in model.get('deleted_fields', ()):
            entity=resolve((catalogue,ref))
            if field in getattr(entity,'__dict__',{}):delattr(entity,field)
        for (catalogue, ref, field), value in model['fields'].items():
            setattr(resolve((catalogue, ref)), field, value)
        for ref, grade in model['grades'].items():
            getattr(_ssct_completion_catalogues()['flow'], ref).grade = grade
        for target, destination in model['deliveries'].items():
            resolve(target).move(resolve(destination))
        for target, entries in model['diaries'].items():
            for entry in sorted(entries):
                resolve(target).write(entry)
        for target, attached in model['listeners'].items():
            # Numbered one-shot nodes/quests already finish in the route model.
            if target[0] == 'step' and re.match(r'^[a-z]+[0-9]+_', target[1]):
                continue
            if target[0] == 'flow' and _ssct_perfect_stages(resolve(target),steps):
                continue
            if attached:
                saga.event.attach(resolve(target))
            else:
                saga.event.detach(resolve(target))

    def _ssct_completion_validate(model):
        import re
        failures = []
        checked = 0
        def expect(ok, detail):
            nonlocal checked
            checked += 1
            if not ok:
                failures.append(detail)
        def resolve(target):
            return getattr(_ssct_completion_catalogues()[target[0]], target[1])
        for (catalogue, ref, flag), present in model['memo'].items():
            entity = resolve((catalogue, ref))
            expect((flag in getattr(entity, 'memo', getattr(entity, 'tags', ()))) == present, 'memo:' + ref + ':' + flag)
        for (catalogue, ref, flag), present in model.get('device_tags', {}).items():
            expect((flag in resolve((catalogue, ref)).tags) == present, 'device-tag:' + ref + ':' + flag)
        for (catalogue, ref, flag), present in model.get('prop_tags', {}).items():
            expect((flag in resolve((catalogue, ref)).tags) == present, 'prop-tag:' + ref + ':' + flag)
        for catalogue, ref, field in model.get('deleted_fields', ()):
            expect(field not in getattr(resolve((catalogue,ref)),'__dict__',{}), 'deleted-field:' + ref + ':' + field)
        for ref,number,frequency in model.get('tv_accounts',()):
            device=resolve(('prop',ref))
            expect(frequency in device.hdd and device.tuner[number].freq.auto is True,
                   'tv-account:' + ref + ':' + str(number))
        for ref,state in model.get('device_states',{}).items():
            expect(getattr(getattr(resolve(('prop',ref)),'step',None),'ref',None)==state,'device-state:'+ref)
        for target, destination in model['deliveries'].items():
            expect(resolve(target).where is resolve(destination), 'delivery:' + target[1])
        for ref, grade in model['grades'].items():
            expect(getattr(_ssct_completion_catalogues()['flow'], ref).grade == grade, 'grade:' + ref)
        for target, attached in model['listeners'].items():
            entity = resolve(target)
            if target[0] == 'step' and re.match(r'^[a-z]+[0-9]+_', target[1]):
                expect(entity not in saga.event.crowd, 'one-shot:' + target[1])
            elif target[0] == 'flow' and _ssct_perfect_stages(entity,_ssct_completion_catalogues()['step']):
                continue
            else:
                expect((entity in saga.event.crowd) == attached, 'listener:' + target[1])
        for (catalogue, ref, field), value in model['fields'].items():
            expect(getattr(resolve((catalogue, ref)), field) == value, 'field:' + ref + ':' + field)
        for cycle in model.get('maternity', ()):
            mother = getattr(saga.cast, cycle['actor'])
            expect(mother.babies == cycle['babies'] and not mother.baby
                   and mother.womb.normal and mother > 'baby', 'maternity:' + mother.ref)
        if failures:
            raise ValueError('Completion postconditions failed: ' + ', '.join(failures[:12]))
        return {'checked': checked, 'source_effects': len(model['sources']),
                'callbacks_inspected': len(model['inspected_callbacks']),
                'initial_repeat_states': model['initial_repeat_states'],
                'repeat_states': model.get('repeat_states',{}),
                'device_states': model.get('device_states',{}),
                'acquired_terminals': model.get('acquired_terminals',[]),
                'device_tags': [list(key) + [value] for key, value in model.get('device_tags', {}).items()],
                'prop_tags': [list(key) + [value] for key, value in model.get('prop_tags', {}).items()],
                'deleted_fields': [list(key) for key in sorted(model.get('deleted_fields',()))],
                'tv_accounts': [[ref,number,frequency.ref] for ref,number,frequency in model.get('tv_accounts',())],
                'greetings': model.get('greetings',()),
                'unclassified_fields': model['unclassified_fields'],
                'unsupported_callbacks': model['unsupported_callbacks'],
                'maternity': model.get('maternity', ()),
                'dynamic_effects': model['dynamic'], 'failures': failures}
