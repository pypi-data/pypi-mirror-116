# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum
from operator import mul, truediv

from .base import AbstractTimeConvert, UnitOfTime, IntOrFloat


class MulOrTruediv(Enum):
    MUL = "mul"
    TRUEDIV = "truediv"


class Unt(AbstractTimeConvert):
    _map = {MulOrTruediv.MUL: mul, MulOrTruediv.TRUEDIV: truediv}

    def __init__(self, unit_of_time: UnitOfTime, mul_or_truediv: MulOrTruediv):
        super().__init__(unit_of_time)
        self._mul_or_truediv = mul_or_truediv

    def _convert(self, value: IntOrFloat) -> float:
        _math = self._get_mul_or_truediv()
        # print(_math)
        return _math(value, self.unit_of_time.value)

    def _get_mul_or_truediv(self):
        return self._map.get(self._mul_or_truediv, MulOrTruediv.MUL)


def unt_map(mul_or_truediv: MulOrTruediv = MulOrTruediv.MUL):
    return {
        UnitOfTime.SECOND: Unt(UnitOfTime.SECOND, mul_or_truediv),
        UnitOfTime.MILLISECOND: Unt(UnitOfTime.MILLISECOND, mul_or_truediv),
        UnitOfTime.MICROSECOND: Unt(UnitOfTime.MICROSECOND, mul_or_truediv)
    }
