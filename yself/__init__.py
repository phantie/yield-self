from functools import wraps
from types import FunctionType

__all__ = ('yield_self',)
__version__ = '1.0'

class specialstaticmethod:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, cls=None):
        def newfunc(*args, **kwargs):
            return self.f(
                (type(obj) if cls is None else cls) if obj is None else obj, 
                *args, 
                **kwargs)
        return newfunc

class specialclassmethod:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, cls=None):
        def newfunc(*args, **kwargs):
            return self.f(
                cls, 
                (type(obj) if cls is None else cls) if obj is None else obj, 
                *args, 
                **kwargs)

        return newfunc

def yield_self(f):
    if isinstance(f, FunctionType):
        @wraps(f)
        def wrap(self, *args, **kwargs):
            f(self, *args, **kwargs)
            return self
        return wrap
    elif isinstance(f, classmethod):
        @wraps(f.__func__)
        def wrap(cls, self, /, *args, **kwargs):
            f.__func__(cls, *args, **kwargs)
            return self
        return specialclassmethod(wrap)
    elif isinstance(f, staticmethod):
        @wraps(f.__func__)
        def wrap(cls_or_inst, /, *args, **kwargs):
            f.__func__(*args, **kwargs)
            return cls_or_inst
        return specialstaticmethod(wrap)
    else:
        raise RuntimeError('unknown argument type', type(f))