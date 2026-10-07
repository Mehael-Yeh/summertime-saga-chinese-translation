"""Observe executed native logic jumps; never evaluate or alter their operands."""
import dis
import hashlib
import json
import sys
import types


def code_identity(code):
    """Stable source and constant identity, including nested native code."""
    def constant(value):
        if isinstance(value, types.CodeType):
            return ['code', describe(value)]
        if isinstance(value, tuple):
            return ['tuple', [constant(item) for item in value]]
        if isinstance(value, frozenset):
            return ['frozenset', sorted((constant(item) for item in value), key=lambda item:json.dumps(item, sort_keys=True))]
        if isinstance(value, bytes):
            return ['bytes', value.hex()]
        return [type(value).__name__, repr(value)]
    def describe(value):
        return [value.co_filename, value.co_qualname, value.co_firstlineno,
                value.co_code.hex(), [constant(item) for item in value.co_consts],
                value.co_names, value.co_varnames, value.co_freevars, value.co_cellvars,
                value.co_flags, value.co_argcount, value.co_posonlyargcount,
                value.co_kwonlyargcount, getattr(value, 'co_exceptiontable', b'').hex()]
    return hashlib.sha256(json.dumps(describe(code), ensure_ascii=True, separators=(',', ':')).encode('ascii')).hexdigest()


def binding_snapshot(values):
    result = {}
    for key, value in values.items():
        if value is None or isinstance(value, (str, int, float, bool)):
            result[key] = value
        else:
            ref = getattr(value, '__dict__', {}).get('ref')
            if ref is None:
                for cls in type(value).__mro__:
                    descriptor = vars(cls).get('ref')
                    if isinstance(descriptor, types.MemberDescriptorType):
                        try:
                            ref = descriptor.__get__(value, type(value))
                        except AttributeError:
                            pass
                        break
            result[key] = {'type': type(value).__module__+'.'+type(value).__name__, 'ref': ref}
    return result


class NativeBranchTrace:
    def __init__(self, limit=10000):
        self.limit = limit
        self.cache = {}
        self.active = False

    def begin(self):
        if sys.gettrace() is not None:
            raise RuntimeError('An existing debugger trace must not be replaced')
        self.records, self.pending, self.calls, self.truncated = {}, {}, {}, False
        self.active = True
        # CPython 3.12 enables opcode events only when a frame requests them
        # at installation time. Seed the flag before settrace, then restore it.
        self.seed_frame = sys._getframe()
        self.seed_flag = self.seed_frame.f_trace_opcodes
        self.seed_frame.f_trace_opcodes = True
        sys.settrace(self.trace)

    def trace(self, frame, event, arg):
        if not self.active:
            return None
        if event == 'call':
            if not str(frame.f_globals.get('__name__', '')).startswith('saga.logic.'):
                return None
            code=frame.f_code
            if id(code) not in self.cache:
                operations=list(dis.get_instructions(code))
                self.cache[id(code)]=({op.offset:op for op in operations},
                    hashlib.sha256(code.co_code).hexdigest(),code_identity(code),code)
            identity=self.cache[id(code)][2]
            key=(frame.f_globals.get('__name__'),identity)
            if key not in self.calls:
                if len(self.calls)>=self.limit:self.truncated=True
                else:self.calls[key]={'module':key[0],'code_identity_sha256':identity,
                    'code':frame.f_code.co_qualname,'calls':0}
            if key in self.calls:self.calls[key]['calls']+=1
            frame.f_trace_opcodes, frame.f_trace_lines = True, False
            return self.trace
        if event == 'opcode':
            code = frame.f_code
            if id(code) not in self.cache:
                operations = list(dis.get_instructions(code))
                self.cache[id(code)] = ({op.offset:op for op in operations},
                                    hashlib.sha256(code.co_code).hexdigest(), code_identity(code), code)
            operations, digest, identity, retained_code = self.cache[id(code)]
            previous = self.pending.pop(id(frame), None)
            if previous is not None:
                op, bindings = previous
                jumped = frame.f_lasti == op.argval
                if 'IF_TRUE' in op.opname:
                    truth = jumped
                elif 'IF_FALSE' in op.opname:
                    truth = not jumped
                else:
                    truth = jumped  # IF_NONE/IF_NOT_NONE are their own predicates.
                key = (frame.f_globals.get('__name__'), identity, op.offset, truth)
                if key not in self.records:
                    if len(self.records) >= self.limit:
                        self.truncated = True
                    else:
                        self.records[key] = {'module':frame.f_globals.get('__name__'),
                            'code':code.co_qualname, 'filename':code.co_filename,
                            'first_line':code.co_firstlineno, 'bytecode_sha256':digest,
                            'code_identity_sha256':identity, 'bindings_scope':'First observed sample for this branch outcome',
                            'offset':op.offset, 'jump':op.opname, 'condition_truth':truth,
                            'jump_taken':jumped, 'bindings':bindings, 'visits':0}
                if key in self.records:
                    self.records[key]['visits'] += 1
            op = operations.get(frame.f_lasti)
            if op is not None and (op.opname.startswith('POP_JUMP') or op.opname.startswith('JUMP_IF')):
                self.pending[id(frame)] = (op, binding_snapshot(frame.f_locals))
        elif event in ('return', 'exception'):
            self.pending.pop(id(frame), None)
        return self.trace

    def finish(self):
        self.active = False
        sys.settrace(None)
        self.seed_frame.f_trace_opcodes = self.seed_flag
        self.seed_frame = None
        return {'observations':list(self.records.values()),'invocations':list(self.calls.values()), 'truncated':self.truncated,
                'scope':'Executed saga.logic conditional jumps during an actual native action; unvisited branches and semantic postconditions remain unverified'}
