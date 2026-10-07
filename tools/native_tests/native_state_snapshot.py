"""Read stored native state, including auxiliary objects, without properties."""
import types
import functools
import json
from enum import IntEnum


class NativeStateSnapshot:
    def __init__(self,catalogues,max_depth=12,max_values=50000):
        self.references={id(entity):(kind,entity.ref) for kind,catalogue in catalogues.items() for entity in catalogue}
        self.max_depth,self.max_values=max_depth,max_values

    def capture(self,catalogues):
        self.count=0
        self.unknown=[]
        facts={kind:{entity.ref:self.fields(entity,0,frozenset(),ignored=('view','when'))
            for entity in catalogue} for kind,catalogue in catalogues.items()}
        return {'facts':facts,'unknown':self.unknown,
            'scope':'Stored fields including native auxiliary objects; computed properties and presentation fields excluded'}

    def fields(self,value,depth,ancestors,ignored=()):
        try:data=object.__getattribute__(value,'__dict__')
        except AttributeError:data={}
        data=dict(data)
        # Member descriptors are storage slots, not executable properties.
        for cls in type(value).__mro__:
            for name,descriptor in vars(cls).items():
                if isinstance(descriptor,types.MemberDescriptorType) and name not in data:
                    try:data[name]=descriptor.__get__(value,type(value))
                    except AttributeError:pass
        return {key:self.read(item,depth+1,ancestors|{id(value)})
            for key,item in sorted(data.items()) if key not in ignored}

    def read(self,value,depth,ancestors):
        self.count+=1
        if self.count>self.max_values or depth>self.max_depth:
            self.unknown.append('snapshot_budget')
            return {'unknown':'snapshot_budget'}
        if isinstance(value,IntEnum):
            return {'enum':type(value).__module__+'.'+type(value).__qualname__,'member':value.name,'value':int(value)}
        if value is None or type(value) in (str,int,float,bool):return value
        if value is Ellipsis:return {'constant':'Ellipsis'}
        if id(value) in self.references:
            kind,ref=self.references[id(value)]
            return {'reference':[kind,ref]}
        if id(value) in ancestors:return {'cycle':type(value).__module__+'.'+type(value).__qualname__}
        if isinstance(value,functools.partial):
            next_ancestors=ancestors|{id(value)}
            return {'partial':self.read(value.func,depth+1,next_ancestors),
                'args':self.read(value.args,depth+1,next_ancestors),
                'keywords':self.read(value.keywords,depth+1,next_ancestors)}
        if isinstance(value,(types.FunctionType,types.MethodType,types.BuiltinFunctionType,type,types.ModuleType)):
            return {'definition':getattr(value,'__module__','')+'.'+getattr(value,'__qualname__',getattr(value,'__name__',''))}
        if isinstance(value,(tuple,list,set,frozenset)):
            items=[self.read(item,depth+1,ancestors|{id(value)}) for item in value]
            if isinstance(value,(set,frozenset)):items.sort(key=self.stable_key)
            return items
        if isinstance(value,dict):
            if not all(type(key) is str for key in value):
                # Preserve both typed keys and values, including native enum
                # child counters. String coercion would merge distinct keys.
                items=[{'key':self.read(key,depth+1,ancestors|{id(value)}),
                    'value':self.read(item,depth+1,ancestors|{id(value)})}
                    for key,item in value.items()]
                items.sort(key=lambda row:self.stable_key(row['key']))
                return {'mapping':items}
            return {key:self.read(item,depth+1,ancestors|{id(value)}) for key,item in sorted(value.items())}
        if type(value).__module__.startswith('saga.'):
            return {'type':type(value).__module__+'.'+type(value).__qualname__,
                'fields':self.fields(value,depth,ancestors)}
        self.unknown.append('unsupported_type:'+type(value).__module__+'.'+type(value).__qualname__)
        return {'unknown_type':type(value).__module__+'.'+type(value).__qualname__}

    @staticmethod
    def stable_key(value):
        return json.dumps(value,sort_keys=True,ensure_ascii=True,separators=(',',':'))
