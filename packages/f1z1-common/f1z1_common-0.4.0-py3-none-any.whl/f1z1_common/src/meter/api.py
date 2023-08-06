# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ..time_ import UnitOfTime, TimeType
from .base import Function
from .meter import AsyncMessageMeter


def meter(timeout: TimeType, unt: UnitOfTime = UnitOfTime.MILLISECOND, *, callback: Function = None):
    return AsyncMessageMeter(timeout, unt, callback=callback)
