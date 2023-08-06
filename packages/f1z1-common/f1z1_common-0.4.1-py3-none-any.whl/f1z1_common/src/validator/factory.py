# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from functools import partial

from .base import AbstractValidator
from .func import FunctionValidator, AsyncFunctionValidator


class AbstractValidatorFactory(metaclass=ABCMeta):

    @classmethod
    def create_validator(cls, subclass: AbstractValidator, message: str, **kwargs) -> AbstractValidator:
        factory = cls._factory(subclass, message)
        return factory(**kwargs)

    @classmethod
    def _is_subclass(cls, klass):
        return issubclass(klass, AbstractValidator)

    @classmethod
    def _factory(cls, subclass: AbstractValidator, message: str):
        if not cls._is_subclass(subclass):
            raise ValueError(f"need a {AbstractValidator.__name__} subclass, but got {type(subclass).__name__}")
        return partial(subclass, message)

    @classmethod
    @abstractmethod
    def create_func_validator(cls, message: str) -> AbstractValidator:
        pass

    @classmethod
    @abstractmethod
    def create_afunc_validator(cls, message: str) -> AbstractValidator:
        pass


class ValidatorFactory(AbstractValidatorFactory):

    @classmethod
    def create_func_validator(cls, message: str) -> FunctionValidator:
        return cls.create_validator(
            FunctionValidator, message
        )

    @classmethod
    def create_afunc_validator(cls, message: str) -> AsyncFunctionValidator:
        return cls.create_validator(
            AsyncFunctionValidator, message
        )
