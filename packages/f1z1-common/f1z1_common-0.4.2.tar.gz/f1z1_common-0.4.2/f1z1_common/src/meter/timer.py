# @Time     : 2021/8/12
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import IntEnum

from ..time_ import UnitOfTime, TimeType
from ..time_.api import timestamp


class StartStates(IntEnum):
    """
    运行状态
    """
    UN_START = 0  # 停
    STARTED = 1  # 已开始
    PAUSE = 2  # 暂停


class IMeterTimer(metaclass=ABCMeta):
    """
    消息计时器
    """

    @property
    @abstractmethod
    def is_timeout(self) -> bool:
        """
        is_timeout
        :return:
        """
        pass

    @abstractmethod
    def current(self) -> float:
        """
        get current time
        :return:
        """
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def restart(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        stop timer
        :return:
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        clear timeout
        :return:
        """
        pass


class MeterTimer(IMeterTimer):

    def __init__(self, timeout: TimeType, unt: UnitOfTime):
        self._st: TimeType = 0  # 开始时间
        self._state: StartStates = StartStates.UN_START  # 状态

        self._timestamp = timestamp(unt)  # 时间单位
        self._timeout = timeout  # 超时时间

    @property
    def is_started(self) -> bool:
        return self._state == StartStates.STARTED

    @property
    def is_timeout(self) -> bool:
        return self._is_timeout()

    def current(self) -> float:
        return self._now_timestamp()

    def start(self) -> None:
        if self.is_started:
            return
        # update state, start time
        self._update_state(StartStates.STARTED)
        self._update_start(self.current())

    def restart(self) -> None:
        self._update_state(StartStates.STARTED)
        self._update_start(self.current())

    def stop(self) -> None:
        self._update_state(StartStates.PAUSE)

    def clear(self) -> None:
        self._update_state(StartStates.UN_START)
        self._update_start(0)

    def _update_start(self, st: TimeType):
        self._st = st

    def _update_state(self, state: StartStates):
        self._state = state

    def _now_timestamp(self):
        return datetime.now().timestamp()

    def _is_timeout(self):
        return self._timestamp.convert(self.current() - self._st) >= self._timeout

    def __str__(self):
        return f"{self.__class__.__name__}(timeout={self._timeout}, state={self._state})"
