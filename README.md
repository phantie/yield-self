# yield-self
yield-self decorator forces classmethods, staticmethods and normal methods return a class/value they are called on 

Example:

```python

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


```

Import:

    from yself import yield_self

Install:

    pip install git+https://github.com/phantie/yield-self.git