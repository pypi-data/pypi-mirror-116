# @Time     : 2021/8/12
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from functools import wraps

from ..time_ import UnitOfTime, TimeType
from .base import Function, AbstractMeter


class AsyncMessageMeter(AbstractMeter):

    def __init__(self,
                 timeout: TimeType,
                 unit: UnitOfTime = UnitOfTime.MILLISECOND,
                 *,
                 callback: Function = None):
        super().__init__(timeout, unit)
        self._callback = callback

    @property
    def callback(self):
        return self._callback

    def tracking(self, func: Function) -> Function:
        meter = self

        @wraps(func)
        async def async_decorate(*args, **kwargs):
            meter.start()
            meter.auto_increment()
            result = await func(*args, **kwargs)
            if meter.is_timeout():
                meter.trigger(meter.callback)
                meter.restart()
            return result

        return async_decorate
