import functools

CHECK = True

class MetaProxy(type):
    def __new__(cls, name, bases, dct):

        if CHECK:
            # create an empthy class
            proxy_class = type('EmptyClass', (), {'SOMETHING': "it's class B"})()
            for attr_name, attr_value in dct.items():
                if attr_name not in ('SOMETHING'):
                    setattr(proxy_class, attr_name, attr_value)
                if callable(attr_value) and not attr_name.startswith('__') and not attr_name.startswith('_'):
                    dct[attr_name] = cls.create_method_wrapper(proxy_class, attr_name, attr_value)
            dct['proxy_class'] = proxy_class
        return super().__new__(cls, name, bases, dct)

    @classmethod
    def create_method_wrapper(cls, proxy_class, method_name, method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            method_a = method
            method_a(self, *args, **kwargs)
            method_b = getattr(proxy_class, method_name)
            method_b(proxy_class, *args, **kwargs)
            return
        return wrapper


class A(metaclass=MetaProxy):
    SOMETHING = "it's class A"

    def do(self):
        print(self.SOMETHING)


# output
# it's class A
# it's class B
a = A()
a.do()

