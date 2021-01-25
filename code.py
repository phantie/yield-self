__all__ = ('yield_self',)

class hybridmethod:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, cls=None):
        if cls is None:
            cls = type(obj)
        def newfunc(*args):
            return self.f(cls if obj is None else obj, *args)
        return newfunc

def yield_self(f):
    from functools import wraps
    if isinstance(f, classmethod):
        @wraps(f.__func__)
        def wrap(cls_or_inst, *args, **kwargs):
            f.__func__(cls_or_inst, *args, **kwargs)
            return cls_or_inst
        return classmethod(wrap)
    elif isinstance(f, staticmethod):
        @wraps(f.__func__)
        def wrap(cls_or_inst, *args, **kwargs):
            f.__func__(*args, **kwargs)
            return cls_or_inst
        return hybridmethod(wrap)
    else:
        @wraps(f)
        def wrap(self, *args, **kwargs):
            f(self, *args, **kwargs)
            return self
        return wrap
