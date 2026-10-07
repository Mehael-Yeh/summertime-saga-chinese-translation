# Repeat acquisition retains one native object and runs the native purchase UI.
default ssct_owned_cart = None
init 998 python:
    def _ssct_owned_active(item=None):
        return (getattr(store, 'ssct_perfect_template', None) == _ssct_perfect_id
                and (item is None or item.ref in (getattr(store, 'ssct_perfect_inventory', None) or ())))

    def _ssct_owned_container_sift(container, *args, **kwargs):
        result = list(_ssct_owned_native_sift(container, *args, **kwargs))
        if _ssct_owned_active() and (container is saga.prop.anon_bag or container is saga.cast.anon):
            pool = args[0] if args else kwargs.get('pool', ())
            for item in pool:
                if _ssct_owned_active(item) and item not in result:
                    result.append(item)
            if kwargs.get('sort', args[1] if len(args) > 1 else False):
                result.sort(key=lambda item: item.name)
        return tuple(result)

    def _ssct_owned_origin(item):
        entry = (getattr(store, 'ssct_perfect_displays', None) or {}).get(item.ref)
        if entry:
            catalogue, ref = entry
            return getattr(getattr(saga, catalogue), ref, None)

    def _ssct_owned_consume(item):
        if getattr(store, 'ssct_perfect_displays', None):
            store.ssct_perfect_displays.pop(item.ref, None)

    def _ssct_owned_move(item, where):
        # Catch native script/quest acquisitions too, rather than maintaining
        # separate handlers for each scene. Other native move protocols remain
        # responsible for replenishment and non-unique items.
        active = _ssct_owned_active(item)
        acquisition = active and (where is saga.camera.track
            or where is getattr(item, 'cart', None))
        previous = item.where
        origin = _ssct_owned_origin(item) if acquisition else None
        if origin is not None and previous is where:
            item.where = origin
        try:
            result = _ssct_owned_native_move(item, where)
        except Exception:
            item.where = previous
            raise
        if acquisition and item.where is where:
            _ssct_owned_consume(item)
        return result

    def _ssct_owned_zero_total(values, start=0):
        # Only the native price generator is free; an unrelated sum introduced
        # by a later engine retains its normal result.
        import builtins
        code = getattr(values, 'gi_code', None)
        if code is not None and code.co_names == ('cost',):
            tuple(values)  # preserve native property validation/errors
            return 0
        return builtins.sum(values, start)

    def _ssct_owned_nav_take(interact):
        if not _ssct_owned_active(interact):
            return _ssct_owned_native_nav_take(interact)
        origin = _ssct_owned_origin(interact)
        previous = interact.where
        # Restore the projected source for the actual native transfer, not for
        # rendering. Native move emits the real enter/leave acquisition events.
        if origin is not None:
            interact.where = origin
        try:
            result = _ssct_owned_native_nav_take(interact)
        except Exception:
            interact.where = previous
            raise
        if interact.where is saga.camera.track:
            _ssct_owned_consume(interact)
        return result

    def _ssct_owned_shop_take(interact):
        if not _ssct_owned_active(interact) or interact not in _ssct_owned_buyable:
            return _ssct_owned_native_shop_take(interact)
        origin = _ssct_owned_origin(interact)
        previous = interact.where
        if origin is not None:
            interact.where = origin
        try:
            result = _ssct_owned_native_shop_take(interact)
        finally:
            # Put-back / leave did not purchase or consume the projection.
            if origin is not None and interact.where is origin:
                interact.where = previous
        if interact.where is interact.cart:
            _ssct_owned_consume(interact)
            if store.ssct_owned_cart is None:
                store.ssct_owned_cart = renpy.revertable.RevertableDict()
            store.ssct_owned_cart.setdefault(interact.cart.ref,
                renpy.revertable.RevertableSet()).add(interact.ref)
            # Native move queues the insert callback. Also support direct calls
            # before the event dispatcher drains that queue.
            interact.cart.hide = False
            saga.gui.buy = interact.cart
        return result

    def _ssct_owned_paid_merchandise(items):
        return _ssct_owned_active() and any((getattr(item, 'cost', 0) or 0) > 0 for item in items)

    def _ssct_owned_checkout_caption():
        # Keep the native shared checkout and its Return blocks. A zero total
        # for merchandise is still a purchase; native zero-price loans remain
        # loans. This does not alter ordinary-save menu conditions.
        statement = renpy.game.script.namemap.get('shop.pay')
        while statement is not None and not isinstance(statement, renpy.ast.Menu):
            statement = statement.next
        if statement is None:
            return
        items = []
        for caption, condition, block in statement.items:
            if caption == 'Buy items for $[cash].':
                condition = '(' + str(condition) + ') or (not cash and _ssct_owned_paid_merchandise(what))'
            elif caption == 'Borrow [saga.gui.buy!lt].':
                condition = '(' + str(condition) + ') and not _ssct_owned_paid_merchandise(what)'
            items.append((caption, condition, block))
        statement.items = items

    def _ssct_owned_shop_pay(interact):
        if not _ssct_owned_active():
            return _ssct_owned_native_shop_pay(interact)
        cart = saga.gui.buy
        # Run the original checkout including its native transfers, rejection,
        # browsing and callbacks. Override only its price total; do not alter
        # catalogue prices or refund cash after a dialogue/save interruption.
        import types
        namespace = dict(_ssct_owned_native_shop_pay.__globals__)
        namespace['sum'] = _ssct_owned_zero_total
        checkout = types.FunctionType(_ssct_owned_native_shop_pay.__code__,
            namespace, _ssct_owned_native_shop_pay.__name__,
            _ssct_owned_native_shop_pay.__defaults__,
            _ssct_owned_native_shop_pay.__closure__)
        result = checkout(interact)
        if cart and getattr(store, 'ssct_owned_cart', None):
            remaining = {item.ref for item in cart.sift()}
            pending = store.ssct_owned_cart.get(cart.ref)
            if pending is not None:
                pending.intersection_update(remaining)
                if not pending:
                    store.ssct_owned_cart.pop(cart.ref, None)
        return result

    def _ssct_owned_shop_fence(area, interact):
        result = _ssct_owned_native_shop_fence(area, interact)
        if _ssct_owned_active() and getattr(store, 'ssct_owned_cart', None):
            for ref in tuple(store.ssct_owned_cart):
                cart = getattr(saga.prop, ref)
                if not cart.sift():
                    store.ssct_owned_cart.pop(ref, None)
        return result

    def _ssct_owned_replace(original, replacement):
        import sys, functools
        from saga import step
        functools.update_wrapper(replacement, original)
        for node in step:
            entries = getattr(node, 'pool', ())
            for index, entry in enumerate(entries):
                if entry[0] is original:
                    entries[index] = (replacement,) + entry[1:]
                elif getattr(entry[0], 'func', None) is original:
                    adapted = functools.partial(replacement, *entry[0].args, **(entry[0].keywords or {}))
                    adapted.__dict__.update(entry[0].__dict__)
                    entries[index] = (adapted,) + entry[1:]
        for name, module in tuple(sys.modules.items()):
            if not name.startswith('saga.logic.'):
                continue
            for key, value in tuple(vars(module).items()):
                if value is original:
                    setattr(module, key, replacement)

init 999 python:
    import saga.logic.nav as _ssct_owned_nav
    import saga.logic.shop as _ssct_owned_shop
    from saga.entity import Container as _ssct_owned_container, Moveable as _ssct_owned_moveable
    _ssct_owned_native_sift = _ssct_owned_container.sift
    _ssct_owned_native_move = _ssct_owned_moveable.move
    _ssct_owned_native_nav_take = _ssct_owned_nav.take
    _ssct_owned_native_shop_take = _ssct_owned_shop.take
    _ssct_owned_native_shop_pay = _ssct_owned_shop.pay
    _ssct_owned_native_shop_fence = _ssct_owned_shop._fence
    _ssct_owned_buyable = _ssct_owned_shop.buyable
    _ssct_owned_abort = _ssct_owned_shop.abort
    import functools
    functools.update_wrapper(_ssct_owned_container_sift, _ssct_owned_native_sift)
    _ssct_owned_container.sift = _ssct_owned_container_sift
    functools.update_wrapper(_ssct_owned_move, _ssct_owned_native_move)
    _ssct_owned_moveable.move = _ssct_owned_move
    _ssct_owned_replace(_ssct_owned_native_nav_take, _ssct_owned_nav_take)
    _ssct_owned_replace(_ssct_owned_native_shop_take, _ssct_owned_shop_take)
    _ssct_owned_replace(_ssct_owned_native_shop_pay, _ssct_owned_shop_pay)
    _ssct_owned_replace(_ssct_owned_native_shop_fence, _ssct_owned_shop_fence)
    _ssct_owned_checkout_caption()

translate zh_hans strings:
    old "Already-owned items incur no extra charge.{#ssct_perfect}"
    new "已拥有的物品不再扣款。{#ssct_perfect}"
