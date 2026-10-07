"""Read native SL2 syntax without executing defaults, Python, or actions."""
import ast


def screen_inventory(screens):
    rows, unknown = [], []
    for (name, variant), screen in screens.items():
        root = screen.function
        wrappers = set()
        while hasattr(root, '__wrapped__') and id(root) not in wrappers:
            wrappers.add(id(root))
            root = root.__wrapped__
        pending, seen = [(root, 'root')], set()
        while pending:
            node, path = pending.pop()
            if id(node) in seen:
                continue
            seen.add(id(node))
            fields = vars(node) if hasattr(node, '__dict__') else {}
            kind = type(node).__name__
            location = fields.get('location')
            base = dict(screen=name, variant=variant, node=kind, path=path,
                        location=list(location) if isinstance(location, tuple) else None,
                        status='inventory_only_not_validated')
            recognized = False
            children = fields.get('children')
            if isinstance(children, (list, tuple)):
                pending.extend((child, path+'/children/'+str(index)) for index, child in enumerate(children))
                recognized = True
            entries = fields.get('entries')
            if isinstance(entries, (list, tuple)):
                for index, entry in enumerate(entries):
                    if not isinstance(entry, tuple) or len(entry) != 2:
                        unknown.append(dict(base, reason='unrecognized_entries_schema'))
                        continue
                    expression, block = entry
                    if expression is not None:
                        rows.append(dict(base, kind='if', expression=str(expression)))
                    pending.append((block, path+'/entries/'+str(index)))
                recognized = True
            keywords = fields.get('keyword')
            if isinstance(keywords, (list, tuple)):
                for key, expression in keywords:
                    if key in ('sensitive', 'action', 'hovered', 'unhovered'):
                        rows.append(dict(base, kind=key, expression=str(expression)))
                recognized = True
            if 'expression' in fields:
                rows.append(dict(base, kind='local_expression', expression=str(fields['expression'])))
                recognized = True
            code = fields.get('code')
            source = getattr(code, 'source', None)
            if isinstance(source, str):
                try:
                    tree = ast.parse(source)
                except SyntaxError:
                    unknown.append(dict(base, reason='unparsed_screen_python'))
                else:
                    for statement in ast.walk(tree):
                        if isinstance(statement, (ast.If, ast.IfExp, ast.While, ast.Assert)):
                            condition = statement.test
                            rows.append(dict(base, kind='python_condition', expression=ast.unparse(condition),
                                             python_line=statement.lineno, requires_native_prior_effects=True))
                recognized = True
            if kind == 'SLUse':
                target = fields.get('target')
                rows.append(dict(base, kind='use', expression=str(target),
                                 requires_parent_binding=True))
                block = fields.get('block')
                if block is not None:
                    pending.append((block, path+'/block'))
                recognized = True
            if kind in ('SLTransclude', 'SLContinue', 'SLBreak', 'SLPass'):
                rows.append(dict(base, kind='parent_control', requires_parent_binding=True))
                recognized = True
            if not recognized:
                unknown.append(dict(base, fields=sorted(fields), reason='unrecognized_screen_node'))
    return dict(conditions=rows, unresolved_nodes=unknown,
                scope='SL2 declarations, including local expressions and actions; no native response proof')
