# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ..is_ import is_validate
from ..error import NotFunctionError, NotAsyncFunctionError
from .base import AbstractValidator


class FunctionValidator(AbstractValidator):

    def is_validate(self, value) -> bool:
        return is_validate.is_function(value)

    def raise_error(self, message: str):
        raise NotFunctionError(message)


class AsyncFunctionValidator(AbstractValidator):

    def is_validate(self, value) -> bool:
        return is_validate.is_async_function(value)

    def raise_error(self, message: str):
        raise NotAsyncFunctionError(message)
