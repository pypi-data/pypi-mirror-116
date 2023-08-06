# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .base import AbstractTimeConvert, IntOrFloat
from .unit import UnitOfTime, MulOrTruediv, unt_map

TRUEDIV = MulOrTruediv.TRUEDIV


class TimeUnt(AbstractTimeConvert):
    _unt = unt_map(TRUEDIV)

    def __init__(self, unit_of_time: UnitOfTime):
        super().__init__(unit_of_time)

    def _convert(self, time: IntOrFloat) -> float:
        return self._get_unt().convert(float(time))

    def _get_unt(self):
        return self._unt.get(self.unit_of_time, UnitOfTime.MILLISECOND)
