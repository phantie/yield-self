from yself import yield_self

def test_from_readme():
    class A:
        x = y = 0

        @yield_self
        def set_x(self, x):
            self.x = x

        @yield_self
        @classmethod
        def set_cls_x(cls, x):
            cls.x = x

        @yield_self
        @staticmethod
        def random_side_effect():
            print('side effect')


    assert A().set_x(10).x == 10
    assert A.set_cls_x(20).x == 20
    assert A().x == 20

    # classmethods
    assert A.set_cls_x(30) is A and A.x == 30
    assert isinstance(A().set_cls_x(40), A) and A.x == 40

    # staticmethods
    assert isinstance(A().random_side_effect(), A)
    assert A.random_side_effect() is A

def test_collisions():
    class A:
        @yield_self
        def foo(this, cls, called_on): ...
        
        @yield_self
        @classmethod
        def bar(this, cls, called_on): ...
        
        @yield_self
        @staticmethod
        def baz(called_on): ...

    A().foo(cls=object, called_on=object())
    A().foo(object, object())
    A().foo(object, called_on=object())

    A().bar(cls=object, called_on=object())
    A().bar(object, object())
    A().bar(object, called_on=object())
    A.bar(cls=object, called_on=object())
    A.bar(object, object())
    A.bar(object, called_on=object())

    A().baz(called_on=object())
    A().baz(object())
    A.baz(called_on=object())
    A.baz(object())

