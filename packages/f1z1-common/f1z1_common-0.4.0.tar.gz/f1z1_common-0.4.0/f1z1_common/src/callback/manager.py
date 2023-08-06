# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import abstractmethod
from operator import not_, indexOf
from typing import Callable, List
from .base import AbstractCallbackManager
from ..validator.api import check_function, check_async_function

ListFunction = List[Callable]


class ListCallbackManager(AbstractCallbackManager):

    def __init__(self):
        self._callbacks: ListFunction = []

    @property
    def callbacks(self):
        return self._callbacks

    @property
    def length(self) -> int:
        return len(self._callbacks)

    def add(self, function: Callable) -> int:
        # self.check(function)
        if not self._is_exits(function):
            self._callbacks.append(function)
        return self.length

    def remove(self, function: Callable) -> int:
        if self.empty():
            return self.length
        idx = self._find(function)
        if idx > -1:
            self._callbacks.pop(idx)
        return self.length

    def _is_exits(self, function: Callable) -> bool:
        if not_(self._callbacks):
            return False
        return function in self._callbacks

    def _find(self, function) -> int:
        try:
            return indexOf(self._callbacks, function)
        except ValueError:
            return -1


class CallbackManagerDecorate(AbstractCallbackManager):

    def __init__(self, manager: AbstractCallbackManager):
        self._manager = manager

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, manager: AbstractCallbackManager):
        if isinstance(manager, AbstractCallbackManager):
            self._manager = manager

    @property
    def callbacks(self):
        return self.manager.callbacks

    @property
    def length(self) -> int:
        return self.manager.length

    def add(self, function: Callable) -> int:
        self._check(function)
        return self.manager.add(function)

    def remove(self, function: Callable) -> int:
        return self.manager.remove(function)

    @abstractmethod
    def _check(self, function: Callable) -> bool:
        pass


class SyncCallbackManager(CallbackManagerDecorate):

    def __init__(self, manager: AbstractCallbackManager):
        super().__init__(manager)

    def _check(self, value):
        return check_function(value)


class AsyncCallbackManager(CallbackManagerDecorate):

    def __init__(self, manager: AbstractCallbackManager):
        super().__init__(manager)

    def _check(self, value):
        return check_async_function(value)
