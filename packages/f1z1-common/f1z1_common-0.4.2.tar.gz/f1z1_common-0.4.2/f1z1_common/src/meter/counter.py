# @Time     : 2021/8/12
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod

MIN = 0
EACH = 1


class IMeterCounter(metaclass=ABCMeta):
    """
    消息计数器
    """

    @abstractmethod
    def current(self) -> int:
        pass

    @abstractmethod
    def auto_increment(self) -> None:
        """
        auto_increment
        :return:
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        clear
        :return:
        """
        pass


class MeterTotal(IMeterCounter):

    def __init__(self, initial: int = 0):
        if initial <= 0:
            self._total = MIN
        else:
            self._total = initial

    def current(self) -> int:
        return self._total

    def auto_increment(self) -> None:
        self._increment(EACH)

    def clear(self) -> None:
        """
        clear count
        :return:
        """
        self._total = 0

    def _increment(self, value: int) -> None:
        self._total += value

    def __str__(self):
        return f"{self.__class__.__name__}(current={self.current()})"


class MeterCurrent(IMeterCounter):

    def __init__(self):
        self._current = 0

    def current(self) -> int:
        return self._current

    def auto_increment(self) -> None:
        self._increment(EACH)

    def clear(self) -> None:
        """
        clear count
        :return:
        """
        self._current = 0

    def _increment(self, value: int) -> None:
        self._current += value

    def __str__(self):
        return f"{self.__class__.__name__}(current={self.current()})"


class MeterCounter(IMeterCounter):

    def __init__(self, initial: int = 0):
        self._total = MeterTotal(initial)  # 累计
        self._current = MeterCurrent()  # 当前

    def current(self) -> int:
        return self._current.current()

    def total(self) -> int:
        return self._total.current()

    def auto_increment(self) -> None:
        self._total.auto_increment()
        self._current.auto_increment()

    def clear(self) -> None:
        self._current.clear()

    def __str__(self):
        return f"{self.__class__.__name__}(current={self._current}, total={self._total})"
