# @Time     : 2021/8/12
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from typing import Callable

from ..is_ import is_validate
from ..time_ import UnitOfTime, TimeType
from .counter import MeterCounter
from .timer import MeterTimer

Function = Callable
INITIAL = 0


class AbstractMeter(metaclass=ABCMeta):

    def __init__(self, timeout: TimeType, unt: UnitOfTime = UnitOfTime.MILLISECOND):
        self._counter = MeterCounter(INITIAL)
        self._timer = MeterTimer(timeout, unt)

    def is_timeout(self):
        return self._timer.is_timeout

    def start(self):
        self._timer.start()

    def restart(self):
        self._timer.restart()
        self._counter.clear()

    def auto_increment(self):
        self._counter.auto_increment()

    def trigger(self, cb: Function = None) -> None:
        if is_validate.is_function(cb):
            cb(self._counter)

    @abstractmethod
    def tracking(self, func: Function) -> Function:
        pass

    def __str__(self):
        return f"{self.__class__.__name__}(timer={self._timer}, counter={self._counter})"

    def __call__(self, fn: Function):
        return self.tracking(fn)
