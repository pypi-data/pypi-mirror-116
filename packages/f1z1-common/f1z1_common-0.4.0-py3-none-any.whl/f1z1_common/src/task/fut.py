# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from asyncio import Future, AbstractEventLoop, get_event_loop
from operator import not_
from typing import Callable


class AbstractFutConvert(metaclass=ABCMeta):

    def __init__(self, eloop: AbstractEventLoop = None):
        self._eloop = eloop

    @property
    def eloop(self):
        return self._eloop

    @property
    @abstractmethod
    def executor(self):
        pass

    def convert(self, sync: Callable, *args) -> Future:
        return self._to_fut(sync, *args)

    def _to_fut(self, sync: Callable, *args):
        eloop = self._get_event_loop()
        return eloop.run_in_executor(self.executor, sync, *args)

    def _get_event_loop(self):
        if not_(self._eloop):
            self._eloop = get_event_loop()
        return self._eloop

    def __str__(self):
        return f"{self.__class__.__name__}(loop={self._eloop}, exec={self.executor})"


class FutConvert(AbstractFutConvert):

    def __init__(self, eloop: AbstractEventLoop = None, executor=None):
        super().__init__(eloop)
        self._executor = executor

    @property
    def executor(self):
        return self._executor
