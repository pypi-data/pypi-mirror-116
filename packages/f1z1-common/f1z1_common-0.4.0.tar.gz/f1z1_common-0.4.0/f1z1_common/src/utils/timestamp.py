# @Time     : 2021/8/12
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from typing import Union
from enum import IntEnum

IntOrFloat = Union[int, float]
_BASE = 10


class UnitOfTime(IntEnum):
    SECOND = _BASE ** 0  # 秒
    MILLISECOND = _BASE ** 3  # 毫秒
    MICROSECOND = _BASE ** 6  # 微秒


class ITimestampConvert(metaclass=ABCMeta):

    @abstractmethod
    def convert(self, timestamp: IntOrFloat) -> float:
        pass


class SecondTimestamp(ITimestampConvert):

    def convert(self, timestamp: IntOrFloat) -> float:
        return timestamp * UnitOfTime.SECOND.value


class MilliSecondTimestamp(ITimestampConvert):

    def convert(self, timestamp: IntOrFloat) -> float:
        return timestamp * UnitOfTime.MILLISECOND.value


class MicroSecondTimestamp(ITimestampConvert):

    def convert(self, timestamp: IntOrFloat) -> float:
        return timestamp * UnitOfTime.MICROSECOND.value


class Timestamp(ITimestampConvert):
    _map = {
        UnitOfTime.SECOND: SecondTimestamp(),
        UnitOfTime.MILLISECOND: MilliSecondTimestamp(),
        UnitOfTime.MICROSECOND: MicroSecondTimestamp()
    }

    def __init__(self, unit_of_time: UnitOfTime):
        self._unit_of_time = unit_of_time

    @property
    def unit_of_time(self):
        return self._unit_of_time

    @unit_of_time.setter
    def unit_of_time(self, value):
        if isinstance(value, UnitOfTime):
            self._unit_of_time = value

    def convert(self, timestamp: IntOrFloat) -> float:
        return self._get_convert().convert(float(timestamp))

    def __str__(self):
        return f"{self.__class__.__name__}(unit_of_time={self.unit_of_time})"

    def _get_convert(self):
        return self._map.get(self.unit_of_time, UnitOfTime.MILLISECOND)


def timestamp(unit_of_time: UnitOfTime = UnitOfTime.MILLISECOND):
    return Timestamp(unit_of_time)
