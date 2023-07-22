import functools

class ProxyMetaException(Exception):
    ...


class ProxyMeta(type):
    def __new__(cls, name, bases, dct,
                enable_proxy: bool = True,
                proxy_class_params: dict = {},
                proxy_class: type = None,
                **proxy_class_init_kwargs: dict):

        if proxy_class and proxy_class_params:
            raise ProxyMetaException('Please specify only "proxy_class" or "proxy_class_params"')

        if enable_proxy:
            if not proxy_class:
                proxy_class_instance = type('ProxyClass', (), proxy_class_params)(**proxy_class_init_kwargs)
            else:
                proxy_class_instance = proxy_class(**proxy_class_init_kwargs)

            for attr_name, attr_value in dct.items():
                if attr_name not in proxy_class_params.keys():
                    setattr(proxy_class_instance, attr_name, attr_value)
                if callable(attr_value):
                    dct[attr_name] = cls.create_method_wrapper(proxy_class_instance, attr_name, attr_value)
            dct['proxy_class'] = proxy_class_instance
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

class MainClass(metaclass=ProxyMeta, enable_proxy=True, proxy_class_params={'ADDITIONAL_INFO': "This is the proxy class"}):
    ADDITIONAL_INFO = "This is the main class"

    def main_method(self):
        print(self.ADDITIONAL_INFO)

# Output:
# This is the main class
# This is the proxy class
# Usage:
obj = MainClass()
obj.main_method()
