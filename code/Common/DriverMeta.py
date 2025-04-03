from abc import ABCMeta, abstractmethod

class DriverMeta(ABCMeta):
    _registered_map = {}
    _registered_optionset = []

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        # 在类定义时自动注册非抽象子类
        if not attrs.get('__abstract__', False):
            driver_name = getattr(cls, 'DriverName', None)
            driver_describe = getattr(cls, 'DriverDescribe', None)
            if driver_name:
                mcs._registered_map[driver_name] = cls
                mcs._registered_optionset.append({
                    "name": driver_describe,
                    "value": driver_name
                })
        return cls

    @classmethod
    def all_registered(mcs):
        return dict(mcs._registered_map)

    @classmethod
    def get_driver(mcs, name):
        registered_map = mcs.all_registered()
        if name not in registered_map:
            raise KeyError(f"Driver {name} not found")
        return registered_map[name]

    @classmethod
    def get_driver_optionset(mcs):
        return mcs._registered_optionset