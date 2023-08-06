# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from asyncio import Task
from typing import Callable, Coroutine, Dict, TypeVar, Tuple, Optional, Union

ArgsTypes = Optional[Tuple]
KwargsTypes = Optional[Dict]
CoroOrFunction = Union[Callable, Coroutine]
ReturnType = TypeVar("ReturnType")


class ITaskExecutor(metaclass=ABCMeta):

    @abstractmethod
    async def execute(self, *args, **kwargs) -> ReturnType:
        pass


class ITaskFactory(metaclass=ABCMeta):

    @abstractmethod
    def create(self) -> Task:
        pass
