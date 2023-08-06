# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import AbstractEventLoop

from .base import CoroOrFunction, ArgsTypes, KwargsTypes
from .executor import TaskExecutor
from .factory import TaskFactory


def executor(coro_or_func: CoroOrFunction, *, eloop: AbstractEventLoop = None, max_workers: int = None):
    return TaskExecutor(coro_or_func, eloop=eloop, max_workers=max_workers)


def creat_task(coro_or_func: CoroOrFunction,
               *,
               eloop: AbstractEventLoop = None,
               max_workers: int = None,
               args: ArgsTypes = None,
               kwargs: KwargsTypes = None):
    return TaskFactory(
        coro_or_func, eloop=eloop, max_workers=max_workers,
        args=args, kwargs=kwargs
    ).create()
