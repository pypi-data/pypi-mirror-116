# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import AbstractEventLoop, create_task
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from operator import not_

from ..is_ import is_validate
from .base import ITaskFactory, CoroOrFunction, ArgsTypes, KwargsTypes
from .fut import FutConvert


def _create_task(coro):
    if not is_validate.is_coroutine(coro):
        raise ValueError(
            f"coro need Coroutine, but got {type(coro).__name__}"
        )
    return create_task(coro)


class CoroTaskFactory(ITaskFactory):

    def __init__(self, coro_or_func: CoroOrFunction):
        self._coro = coro_or_func

    def create(self):
        return _create_task(self._coro)

    def __str__(self):
        return f"{self.__class__.__name__}(coro={self._coro})"


class CoroFunctionTaskFactory(ITaskFactory):

    def __init__(self, coro_or_func: CoroOrFunction, *, args: ArgsTypes, kwargs: KwargsTypes):
        self._afunc = coro_or_func
        self._args, self._kwargs = args, kwargs

    def create(self):
        """
        async function to task

        :return:
        """
        return _create_task(self._run_in_ctx())

    async def _run_in_ctx(self):
        """
        async function must be async context
        :return:
        """
        args, kwargs = self._args, self._kwargs
        return await self._afunc(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}(afunc={self._afunc})"


class FunctionTaskFactory(ITaskFactory):

    def __init__(self,
                 coro_or_func: CoroOrFunction,
                 *,
                 eloop: AbstractEventLoop,
                 max_workers: int = None,
                 args: ArgsTypes = None,
                 kwargs: KwargsTypes = None):
        self._func = coro_or_func
        self._args, self._kwargs = args, kwargs
        self._convert = FutConvert(
            eloop, ThreadPoolExecutor(max_workers=max_workers)
        )

    def create(self):
        """
        function to task
        :return:
        """
        return _create_task(self._run_in_ctx())

    async def _run_in_ctx(self):
        sync = self._get_sync_func()
        fut = self._to_future(sync)
        return await fut

    def _to_future(self, sync):
        return self._convert.convert(sync, *self._args)

    def _get_sync_func(self):
        return partial(self._func, **self._kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}(func={self._func})"


class TaskFactory(ITaskFactory):

    def __init__(self,
                 coro_or_func: CoroOrFunction,
                 *,
                 eloop: AbstractEventLoop,
                 max_workers: int = None,
                 args: ArgsTypes = None,
                 kwargs: KwargsTypes = None):
        _args = () if not_(args) else args
        _kwargs = {} if not_(kwargs) else kwargs

        if is_validate.is_coroutine(coro_or_func):
            self._factory = CoroTaskFactory(coro_or_func)

        elif is_validate.is_async_function(coro_or_func):
            self._factory = CoroFunctionTaskFactory(coro_or_func, args=_args, kwargs=_kwargs)

        elif is_validate.is_function(coro_or_func):
            self._factory = FunctionTaskFactory(
                coro_or_func,
                eloop=eloop, max_workers=max_workers,
                args=_args, kwargs=_kwargs
            )
        else:
            raise ValueError(
                f"coro_or_func need a Coroutine, async function or function, but got {type(coro_or_func).__name__}"
            )

    @property
    def factory(self):
        return self._factory

    def create(self):
        return self.factory.create()

    def __str__(self):
        return f"{self.__class__.__name__}(factory={self.factory})"
