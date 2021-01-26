from functools import wraps
from types import FunctionType

__all__ = ('yield_self',)
__version__ = '1.1.1'

class specialstaticmethod:
    def __init__(self, f): self.f = f

    def __get__(self, obj, cls=None):
        def newfunc(*args, **kwargs):
            return self.f(cls if obj is None else obj, *args, **kwargs)
        return newfunc

class specialclassmethod:
    def __init__(self, f): self.f = f

    def __get__(self, obj, cls=None):
        def newfunc(*args, **kwargs):
            return self.f(cls,  cls if obj is None else obj, *args, **kwargs)
        return newfunc

def yield_self(f):
    if isinstance(f, FunctionType):
        @wraps(f)
        def wrap(called_on, /, *args, **kwargs):
            f(called_on, *args, **kwargs)
            return called_on
        return wrap
    elif isinstance(f, classmethod):
        @wraps(f.__func__)
        def wrap(cls, called_on, /, *args, **kwargs):
            f.__func__(cls, *args, **kwargs)
            return called_on
        return specialclassmethod(wrap)
    elif isinstance(f, staticmethod):
        @wraps(f.__func__)
        def wrap(called_on, /, *args, **kwargs):
            f.__func__(*args, **kwargs)
            return called_on
        return specialstaticmethod(wrap)
    else:
        raise RuntimeError('unknown argument type', type(f))