# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from enum import IntEnum
from typing import Union

IntOrFloat = Union[int, float]
_B = 10


class UnitOfTime(IntEnum):
    SECOND = 1  # 秒
    MILLISECOND = _B ** 3  # 毫秒
    MICROSECOND = _B ** 6  # 微秒


class AbstractTimeConvert(metaclass=ABCMeta):

    def __init__(self, unit_of_time: UnitOfTime):
        self._unit_of_time = unit_of_time

    @property
    def unit_of_time(self):
        return self._unit_of_time

    @unit_of_time.setter
    def unit_of_time(self, value: UnitOfTime):
        if isinstance(value, UnitOfTime):
            self._unit_of_time = value

    def convert(self, value: IntOrFloat) -> float:
        return self._convert(value)

    @abstractmethod
    def _convert(self, value: IntOrFloat) -> float:
        pass

    def __str__(self):
        return f"{self.__class__.__name__}(unit_of_time={self.unit_of_time})"
