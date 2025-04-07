from abc import ABCMeta,abstractmethod
class GuideBase(metaclass=ABCMeta):

    @property
    @abstractmethod
    def GuideName(self):
        pass

    @property
    @abstractmethod
    def GuideDescribe(self):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass