# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod


class AbstractValidator(metaclass=ABCMeta):

    def __init__(self, error_message: str):
        self._message = error_message

    @property
    def error_message(self):
        return self._message

    @abstractmethod
    def is_validate(self, value) -> bool:
        pass

    @abstractmethod
    def raise_error(self, message: str):
        pass

    def __call__(self, value, **kwargs):
        result = self.is_validate(value, **kwargs)
        if not result:
            self.raise_error(self.error_message)
        return result

    def __str__(self):
        return f"{self.__class__.__name__}(error_message={self.error_message})"
