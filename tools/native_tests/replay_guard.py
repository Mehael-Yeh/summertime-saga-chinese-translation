"""Bound isolated replay waits; this module does not modify game state."""


def native_replay_start(case, baseline, interactions):
    """Reuse an ordinary-navigation checkpoint; never trust a device snapshot.

    Full input provenance is retained. Only its already saved prefix can be
    removed from replay, and that prefix must match exactly.
    """
    path = list(case.get('source_path', ()))
    if not interactions:
        return case['slot'], [], []
    anchor = case.get('replay_anchor')
    if anchor is None:
        return baseline, [], path
    if anchor.get('kind') != 'ordinary_navigation':
        raise ValueError('Unsupported native replay checkpoint')
    prefix = anchor.get('path')
    if not isinstance(prefix, list) or path[:len(prefix)] != prefix:
        raise ValueError('Native checkpoint prefix does not match input provenance')
    if not isinstance(anchor.get('slot'), str) or not anchor['slot']:
        raise ValueError('Native checkpoint slot missing')
    return anchor['slot'], list(prefix), path[len(prefix):]


def validate_python_blocks(path):
    import ast
    import textwrap
    from pathlib import Path
    blocks = []
    current = None
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if line and not line[0].isspace() and not line.startswith('#'):
            if current is not None:
                blocks.append(current)
                current = None
            if line.startswith('init ') and 'python' in line and line.endswith(':'):
                current = []
                continue
        if current is not None:
            current.append(line)
    if current is not None:
        blocks.append(current)
    for block in blocks:
        ast.parse(textwrap.dedent('\n'.join(block)), filename=str(path))
    return len(blocks)


def first_visible_hop(start, goal, neighbors, traversable=None):
    from collections import deque
    pending = deque([(start, None)])
    visited = {start}
    while pending:
        current, first = pending.popleft()
        for target in neighbors(current):
            hop = target if first is None else first
            if target == goal:
                return hop
            if target not in visited and (traversable is None or traversable(target)):
                visited.add(target)
                pending.append((target, hop))
    return None


def clock_button_allowed(gui_mode, focused, current, target):
    return gui_mode == 'nav' and not focused and target > current


def navigation_succeeded(kind, before_camera, before_focus, after_camera, after_focus, target):
    if kind == 'navigation':
        return target == after_camera or target == after_focus
    if kind == 'navigation_back':
        return (before_camera, before_focus) != (after_camera, after_focus)
    return False


def filter_key(signature):
    """Keep persisted attempt keys stable across Python hash randomization."""
    return tuple(sorted((name, repr(value)) for name, value in signature))


def native_choice_target(expression):
    """Read a literal native menu event without evaluating script code."""
    import ast
    try:
        tree=ast.parse(str(expression),mode='eval').body
    except (SyntaxError,ValueError):
        return None
    if not isinstance(tree,ast.Call) or ast.unparse(tree.func)!='saga.event.emit':
        return None
    fields={item.arg:item.value for item in tree.keywords}
    choice=fields.get('choice');who=fields.get('who')
    if not isinstance(choice,ast.Constant) or not isinstance(choice.value,str):return None
    if not isinstance(who,ast.Attribute) or ast.unparse(who.value)!='saga.cast':return None
    return choice.value,who.attr


def choose_unexplored(offered, visits, menu_key):
    """Return an enabled native choice, rotating away from repeated branches."""
    index = min(range(len(offered)),
                key=lambda index: visits.get((menu_key, index), 0))
    key = (menu_key, index)
    visits[key] = visits.get(key, 0) + 1
    return offered[index]


def stored_facts(entity, ignored=(), included=None):
    """Read data fields only, without evaluating native computed properties.

    This is a dependency observation, not a complete semantic model: unknown
    object values retain their type, and remain outside completion evidence.
    """
    import types
    fields = dict(getattr(entity, '__dict__', {}))
    for cls in type(entity).__mro__:
        for name, descriptor in vars(cls).items():
            if isinstance(descriptor, types.MemberDescriptorType):
                try:
                    fields[name] = descriptor.__get__(entity, type(entity))
                except AttributeError:
                    pass

    def freeze(value, seen):
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        identity = id(value)
        if identity in seen:
            return ('cycle', type(value).__name__)
        if isinstance(value, (dict, list, tuple, set, frozenset)):
            seen = seen | {identity}
            if isinstance(value, dict):
                return tuple(sorted(((freeze(key, seen), freeze(item, seen))
                                     for key, item in value.items()), key=repr))
            result = tuple(freeze(item, seen) for item in value)
            return tuple(sorted(result, key=repr)) if isinstance(value, (set, frozenset)) else result
        # Catalogue references are stable identifiers; don't walk object graphs.
        ref = getattr(value, '__dict__', {}).get('ref')
        if ref is None:
            descriptor = next((vars(cls).get('ref') for cls in type(value).__mro__
                               if isinstance(vars(cls).get('ref'), types.MemberDescriptorType)), None)
            if descriptor is not None:
                try:
                    ref = descriptor.__get__(value, type(value))
                except AttributeError:
                    pass
        return (type(value).__module__, type(value).__name__, ref)

    return tuple(sorted((name, freeze(value, {id(entity)})) for name, value in fields.items()
                        if name not in ignored and (included is None or name in included)))


class DependencyScheduler:
    """Suspend unproductive goals until an observed prerequisite changes.

    Navigation is an implementation of a goal, not completion. Reminders and
    vetoed journeys cannot keep priority just because they are callable.
    """
    def __init__(self):
        self.waiting = {}
        self.journeys = {}

    def navigation_cycle(self, goal, revision, edge):
        """A repeated directed edge without prerequisite changes is a cycle.

        Successful intermediate movement is not proof that the destination
        can be reached. Do not impose a fixed journey length on valid paths.
        """
        if goal is None:return False
        known_revision,edges=self.journeys.get(goal,(revision,set()))
        if known_revision!=revision:edges=set()
        repeated=edge in edges
        edges.add(edge)
        self.journeys[goal]=(revision,edges)
        if repeated:self.waiting[goal]=revision
        return repeated

    def eligible(self, goal, revision):
        return self.waiting.get(goal) != revision

    def observe(self, goal, before, after, reached=True, navigation=False):
        if goal is None:
            return 'exploration'
        if navigation and reached:
            return 'journey'
        if not reached or before == after:
            self.waiting[goal] = after
            return 'await_prerequisite_change'
        self.waiting.pop(goal, None)
        return 'observed_state_change'


def catalogue_references(function, catalogues=None):
    """Extract direct native catalogue references without running a callback."""
    import dis
    import types
    found=set()
    def inspect(code):
        instructions=list(dis.get_instructions(code))
        for index,instruction in enumerate(instructions[:-1]):
            if instruction.opname!='LOAD_GLOBAL':continue
            owner=function.__globals__.get(instruction.argval)
            module=getattr(owner,'__name__','')
            catalogue=next((name for name,value in (catalogues or {}).items() if owner is value),None)
            if catalogue is None:
                if module not in ('saga.cast','saga.prop','saga.flow','saga.sets'):continue
                catalogue=module.rsplit('.',1)[1]
            following=instructions[index+1]
            if following.opname=='LOAD_ATTR':found.add((catalogue,following.argval))
        for value in code.co_consts:
            if isinstance(value,types.CodeType):inspect(value)
    code=getattr(function,'__code__',None)
    if code is not None:inspect(code)
    return tuple(sorted(found))


def catalogue_dependencies(function, catalogues):
    """Slice native data dependencies; visual timestamps aren't task facts.

    Actor comparisons and containment read encounter memory through their
    native protocols. Explicit attribute reads extend that protocol set.
    Unknown computed properties remain unsupported, never executed here.
    """
    import dis,types
    fields={key:set(('memo','step','where')) for key in catalogue_references(function,catalogues)}
    def inspect(code):
        instructions=list(dis.get_instructions(code))
        for index,op in enumerate(instructions):
            if op.opname!='LOAD_GLOBAL':continue
            owner=function.__globals__.get(op.argval)
            catalogue=next((name for name,value in catalogues.items() if owner is value),None)
            if catalogue is None or index+1>=len(instructions):continue
            target=instructions[index+1]
            if target.opname!='LOAD_ATTR':continue
            key=(catalogue,target.argval)
            fields.setdefault(key,set(('memo','step','where')))
            if index+2<len(instructions) and instructions[index+2].opname=='LOAD_ATTR':
                fields[key].add(instructions[index+2].argval)
        for child in code.co_consts:
            if isinstance(child,types.CodeType):inspect(child)
    if getattr(function,'__code__',None) is not None:inspect(function.__code__)
    return tuple((kind,ref,tuple(sorted(names))) for (kind,ref),names in sorted(fields.items()))


def catalogue_effect_fields(function, catalogues):
    """Add direct native writes for postconditions, not scheduler wake-ups."""
    import dis,types
    fields={(kind,ref):set(names) for kind,ref,names in catalogue_dependencies(function,catalogues)}
    def inspect(code):
        instructions=list(dis.get_instructions(code))
        for index,op in enumerate(instructions[:-2]):
            if op.opname!='LOAD_GLOBAL':continue
            owner=function.__globals__.get(op.argval)
            kind=next((name for name,value in catalogues.items() if owner is value),None)
            target,write=instructions[index+1:index+3]
            if kind is not None and target.opname=='LOAD_ATTR' and write.opname=='STORE_ATTR':
                fields.setdefault((kind,target.argval),set()).add(write.argval)
        for child in code.co_consts:
            if isinstance(child,types.CodeType):inspect(child)
    if getattr(function,'__code__',None) is not None:inspect(function.__code__)
    return tuple((kind,ref,tuple(sorted(names))) for (kind,ref),names in sorted(fields.items()))


def task_priority(listed, todo):
    """Use native Notes metadata; don't infer tasks from translated wording."""
    if listed:
        return 0 if isinstance(todo,str) and todo.strip() else None
    return 1


def has_public_program_input(pool, entities):
    """Global programs may own player controls, not only actor observers.

    Native filters are frozen pairs. A who notification without a concrete
    choice is not player input; navigation infrastructure is planned separately.
    Visibility and sensitivity still need verification before dispatch.
    """
    for callback, signature, mutex, weight in pool:
        if getattr(callback, '__module__', '') in ('saga.logic.auto', 'saga.logic.gui'):
            continue
        fields = dict(signature)
        if fields.get('interact') in entities:
            return True
        if fields.get('who') in entities and fields.get('choice') is not None:
            return True
    return False


def declared_input_matches(actual, pending):
    """A missing key is not a declared None-valued player input."""
    return bool(pending) and all(name in actual and (actual[name] is value or actual[name] == value)
                                 for name, value in pending.items())


def window_input_state(ram):
    """PC app st is a presentation timer; content fields identify input state."""
    from collections.abc import Mapping
    if not isinstance(ram, Mapping):return None
    return tuple(sorted((ref,tuple(sorted((name,value) for name,value in data.items() if name!='st')))
                        for ref,data in ram.items() if isinstance(data,Mapping)))


def clock_navigation_places(function,catalogues):
    """Find direct protagonist/place membership branches without running them.

    Only simple false-jump branches are admitted. A positive membership whose
    body immediately returns None is an exclusion, not a navigation goal.
    """
    import dis
    code=getattr(function,'__code__',None)
    if code is None:return ()
    instructions=list(dis.get_instructions(code));found=set()
    for index in range(len(instructions)-6):
        a,b,c,d,contains,jump,body=instructions[index:index+7]
        if a.opname!='LOAD_GLOBAL' or function.__globals__.get(a.argval) is not catalogues.get('cast'):continue
        if b.opname!='LOAD_ATTR' or b.argval!='anon':continue
        if c.opname!='LOAD_GLOBAL' or function.__globals__.get(c.argval) is not catalogues.get('sets'):continue
        if d.opname!='LOAD_ATTR' or contains.opname!='CONTAINS_OP' or 'JUMP_IF_FALSE' not in jump.opname:continue
        early_none=body.opname=='RETURN_CONST' and body.argval is None
        if body.opname=='LOAD_CONST' and body.argval is None and index+7<len(instructions):
            early_none=instructions[index+7].opname=='RETURN_VALUE'
        if (contains.arg==0 and not early_none) or (contains.arg==1 and early_none):found.add(d.argval)
    return tuple(sorted(found))


def finite_endpoint_kind(ref, registered, done=False, hint=None, pool_count=None):
    """Classify an observed native frontier, not visited dialogue coverage."""
    import re
    if ref=='null':return 'native_null'
    match=re.fullmatch(r'([a-z]+)([0-9]+)_.+',str(ref))
    if match is None:return None
    numbers=[int(found.group(1)) for candidate in registered
        if (found:=re.fullmatch(re.escape(match.group(1))+r'([0-9]+)_.+',str(candidate)))]
    if (numbers and int(match.group(2))==max(numbers) and done is True
            and hint and pool_count==0):return 'native_future_placeholder'
    return None


def native_screen_query(expression):
    """Accept only a zero-argument query on the screen's native what object."""
    import ast
    try:tree=ast.parse(str(expression),mode='eval').body
    except (SyntaxError,ValueError):return None
    if (isinstance(tree,ast.Call) and not tree.args and not tree.keywords
            and isinstance(tree.func,ast.Attribute) and isinstance(tree.func.value,ast.Name)
            and tree.func.value.id=='what'):
        return tree.func.attr
    return None


class ReplayGuard:
    def __init__(self, idle_seconds=3.0, repeat_limit=24):
        self.idle_seconds = idle_seconds
        self.repeat_limit = repeat_limit
        self.progress = None
        self.fingerprint = None
        self.changed_at = None
        self.visits = {}

    def begin_interaction(self, now):
        """Exclude planning time from UI idle time, retaining cycle evidence."""
        self.changed_at = now

    def observe(self, now, fingerprint, progress):
        if progress != self.progress:
            self.progress = progress
            self.visits.clear()
        if fingerprint != self.fingerprint:
            self.fingerprint = fingerprint
            self.changed_at = now
            self.visits[fingerprint] = self.visits.get(fingerprint, 0) + 1
        if self.changed_at is None:
            self.changed_at = now
        if now - self.changed_at >= self.idle_seconds:
            return 'unchanged_interaction'
        if self.visits.get(fingerprint, 0) >= self.repeat_limit:
            return 'repeated_interaction_cycle'
        return None


if __name__ == '__main__':
    import sys
    print('Validated Python blocks:', validate_python_blocks(sys.argv[1]))
