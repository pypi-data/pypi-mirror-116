# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .base import UnitOfTime
from .unit import Unt, MulOrTruediv
from .timestamp import Timestamp
from .timeunt import TimeUnt

DEFAULT = UnitOfTime.MILLISECOND


def second(mul_or_truediv: MulOrTruediv = MulOrTruediv.MUL):
    return Unt(UnitOfTime.SECOND, mul_or_truediv)


def microsecond(mul_or_truediv: MulOrTruediv = MulOrTruediv.MUL):
    return Unt(UnitOfTime.MICROSECOND, mul_or_truediv)


def millisecond(mul_or_truediv: MulOrTruediv = MulOrTruediv.MUL):
    return Unt(UnitOfTime.MILLISECOND, mul_or_truediv)


def timestamp(unit_of_time: UnitOfTime = DEFAULT):
    return Timestamp(unit_of_time)


def timeunt(unit_of_time: UnitOfTime = DEFAULT):
    return TimeUnt(unit_of_time)
