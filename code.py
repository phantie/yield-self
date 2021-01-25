from functools import wraps
from types import FunctionType

__all__ = ('yield_self',)

class hybridstaticmethod:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, cls=None):
        if cls is None:
            cls = type(obj)
        def newfunc(*args):
            return self.f(cls if obj is None else obj, *args)
        return newfunc

class hybridclassmethod:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, cls=None):
        if cls is None:
            cls = type(obj)
        def newfunc(*args):
            return self.f(cls, cls if obj is None else obj, *args)
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
        return hybridclassmethod(wrap)
    elif isinstance(f, staticmethod):
        @wraps(f.__func__)
        def wrap(cls_or_inst, /, *args, **kwargs):
            f.__func__(*args, **kwargs)
            return cls_or_inst
        return hybridstaticmethod(wrap)
    else:
        raise RuntimeError('unknown argument type', type(f))