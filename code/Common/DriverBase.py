from abc import ABCMeta,abstractmethod
from Common.DriverMeta import DriverMeta
class DirverBase(metaclass=DriverMeta):
    __abstract__ = True  # 标记为抽象基类

    #__registered_map = {}

    @property
    @abstractmethod
    def DriverName(self):
        pass

    @property
    @abstractmethod
    def DriverDescribe(self):
        pass

    @property
    @abstractmethod
    def DriverParams(self):
        pass

    @abstractmethod
    def execute(self):
        pass


