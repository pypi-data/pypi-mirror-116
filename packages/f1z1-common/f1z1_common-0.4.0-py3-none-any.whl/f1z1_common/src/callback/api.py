# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .manager import ListCallbackManager, SyncCallbackManager, AsyncCallbackManager


def func_manager():
    return SyncCallbackManager(ListCallbackManager())


def afunc_manager():
    return AsyncCallbackManager(ListCallbackManager())
