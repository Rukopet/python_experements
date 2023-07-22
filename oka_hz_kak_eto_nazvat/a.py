import functools

ENABLE_PROXY = True

class ProxyMeta(type):
    def __new__(cls, name, bases, dct):
        if ENABLE_PROXY:
            proxy_class = type('ProxyClass', (), {'ADDITIONAL_INFO': "This is the proxy class"})()
            for attr_name, attr_value in dct.items():
                if attr_name != 'ADDITIONAL_INFO':
                    setattr(proxy_class, attr_name, attr_value)
                if callable(attr_value) and not attr_name.startswith('__') and not attr_name.startswith('_'):
                    dct[attr_name] = cls.create_method_wrapper(proxy_class, attr_name, attr_value)
            dct['proxy_class'] = proxy_class
        return super().__new__(cls, name, bases, dct)

    @classmethod
    def create_method_wrapper(cls, proxy_class, method_name, method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            original_method = method
            original_method(self, *args, **kwargs)
            proxy_method = getattr(proxy_class, method_name)
            proxy_method(proxy_class, *args, **kwargs)
            return
        return wrapper

class MainClass(metaclass=ProxyMeta):
    ADDITIONAL_INFO = "This is the main class"

    def main_method(self):
        print(self.ADDITIONAL_INFO)

# Usage:
obj = MainClass()
obj.main_method()
