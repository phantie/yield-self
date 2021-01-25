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
        return classmethod(wrap)
    else:
        @wraps(f)
        def wrap(self, *args, **kwargs):
            f(self, *args, **kwargs)
            return self
        return wrap
