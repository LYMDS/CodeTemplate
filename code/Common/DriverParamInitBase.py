from abc import ABCMeta,abstractmethod
from Common.DriverParamInitMeta import DriverParamInitMeta
class DirverParamInitBase(metaclass=DriverParamInitMeta):
    __abstract__ = True  # 标记为抽象基类

    # __registered_map = {}

    @property
    @abstractmethod
    def DriverName(self):
        pass

    @property
    @abstractmethod
    def GuideName(self):
        pass

    @abstractmethod
    def CreateBaseParam(self, *args, **kwargs):
        pass

    @abstractmethod
    def CreateExecParam(self, *args, **kwargs):
        pass
