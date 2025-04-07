from abc import ABCMeta, abstractmethod

class DriverParamInitMeta(ABCMeta):
    _registered_map = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        # 在类定义时自动注册非抽象子类
        if not attrs.get('__abstract__', False):
            driver_name = getattr(cls, 'DriverName', None)
            guide_name = getattr(cls, 'GuideName', None)
            if driver_name:
                mcs._registered_map[(guide_name, driver_name)] = cls
        return cls

    @classmethod
    def all_registered(mcs):
        return dict(mcs._registered_map)

    @classmethod
    def get_driver_param_init(mcs, guide_name, driver_name):
        registered_map = mcs.all_registered()
        key = (guide_name, driver_name)
        if key not in registered_map:
            raise KeyError(f"Driver {key} not found")
        return registered_map[key]
