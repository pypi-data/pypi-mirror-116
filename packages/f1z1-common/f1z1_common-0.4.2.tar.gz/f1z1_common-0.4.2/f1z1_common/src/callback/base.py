# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from operator import not_
from typing import Callable, Iterable


class AbstractCallbackManager(metaclass=ABCMeta):

    @property
    @abstractmethod
    def callbacks(self) -> Iterable[Callable]:
        pass

    @property
    @abstractmethod
    def length(self) -> int:
        pass

    def empty(self):
        return not_(self.length)

    @abstractmethod
    def add(self, function: Callable) -> int:
        pass

    @abstractmethod
    def remove(self, function: Callable) -> int:
        pass

    def to_list(self):
        if self.empty():
            return []
        return [cb for cb in self]

    def __iter__(self):
        if not self.empty():
            for _, cb in enumerate(self.callbacks):
                yield cb

    # def is_callback_manager(self, value):
    #     return isinstance(value, AbstractCallbackManager)

    def __str__(self):
        return f"{self.__class__.__name__}(callbacks={[item for item in self]})"
