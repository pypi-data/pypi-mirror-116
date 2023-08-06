# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Coroutine, Callable

from ..is_ import is_validate
from .base import ITaskExecutor, CoroOrFunction, ReturnType
from .fut import FutConvert


class CoroTaskExecutor(ITaskExecutor):

    def __init__(self, coro_or_func: Coroutine):
        self._coro = coro_or_func

    async def execute(self, *args, **kwargs) -> ReturnType:
        return await self._coro

    def __str__(self):
        return f"{self.__class__.__name__}(coro={self._coro})"


class CoroFunctionTaskExecutor(ITaskExecutor):

    def __init__(self, coro_or_func: Callable):
        self._afunc = coro_or_func

    async def execute(self, *args, **kwargs) -> ReturnType:
        return await self._afunc(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}(coro={self._afunc})"


class FunctionTaskExecutor(ITaskExecutor):

    def __init__(self,
                 coro_or_func: Callable, *,
                 loop: AbstractEventLoop = None,
                 max_workers: int = None):
        self._func = coro_or_func
        self._convert = FutConvert(
            loop, ThreadPoolExecutor(max_workers=max_workers)
        )

    async def execute(self, *args, **kwargs) -> ReturnType:
        # sync function to coroutine
        sync = self._get_coro_or_func(**kwargs)
        fut = self._to_future(sync, *args)
        return await fut

    def _to_future(self, sync, *args):
        return self._convert.convert(sync, *args)

    def _get_coro_or_func(self, **kwargs):
        """
        保留关键字参数
        :return:
        """
        return partial(self._func, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}(func={self._func}, convert={self._convert})"


class TaskExecutor(ITaskExecutor):

    def __init__(self,
                 coro_or_func: CoroOrFunction,
                 *,
                 eloop: AbstractEventLoop = None,
                 max_workers: int = None):

        if is_validate.is_coroutine(coro_or_func):
            self._executor = CoroTaskExecutor(coro_or_func)

        elif is_validate.is_async_function(coro_or_func):
            self._executor = CoroFunctionTaskExecutor(coro_or_func)

        elif is_validate.is_function(coro_or_func):
            self._executor = FunctionTaskExecutor(
                coro_or_func,
                eloop=eloop, max_workers=max_workers
            )
        else:
            raise ValueError(
                f"executed need Coroutine, Task, async function, or function, but got {type(coro_or_func).__name__}"
            )

    @property
    def executor(self):
        return self._executor

    async def execute(self, *args, **kwargs) -> ReturnType:
        return await self.executor.execute(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}(executor={self.executor})"
