# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from operator import not_
from typing import Callable, Iterable, List, Union, TypeVar

from ..is_ import is_validate
from .base import AbstractValidator

ValidatorTypes = Union[AbstractValidator, Callable]
ValidatorList = List[ValidatorTypes]
Validated = TypeVar("Validated")


class AbstractValidatorManager(metaclass=ABCMeta):

    @property
    @abstractmethod
    def validators(self) -> Iterable[ValidatorTypes]:
        pass

    @property
    @abstractmethod
    def length(self) -> int:
        pass

    @abstractmethod
    def add(self, validator: ValidatorTypes) -> int:
        pass

    @abstractmethod
    def remove(self, validator: ValidatorTypes) -> int:
        pass

    def empty(self):
        return not_(self.length)

    def is_validate(self, value: Validated) -> bool:
        results = []
        append = results.append
        for validator in self:
            append(results)
        return all(results)

    def __iter__(self):
        if not self.empty():
            for _, item in enumerate(self.validators):
                yield item


class ListValidatorManager(AbstractValidatorManager):

    def __init__(self):
        self._validators: ValidatorList = []

    @property
    def validators(self):
        return self._validators

    @property
    def length(self) -> int:
        return len(self.validators)

    def add(self, validator):
        if not self._is_validator(validator):
            return self.length

        if not self._is_exists(validator):
            self._validators.append(validator)

        return self.length

    def remove(self, validator):
        if self.empty():
            return self.length
        idx = self._find(validator)
        if idx > -1:
            self._validators.pop(idx)
        return self.length

    def _find(self, validator: ValidatorTypes) -> int:
        if not self._is_exists(validator):
            return -1
        return self._validators.index(validator)

    def _is_validator(self, value) -> bool:
        return any([
            is_validate.is_function(value),
            isinstance(value, AbstractValidator)
        ])

    def _is_exists(self, validator: ValidatorTypes) -> bool:
        if self.empty():
            return False
        return validator in self.validators
