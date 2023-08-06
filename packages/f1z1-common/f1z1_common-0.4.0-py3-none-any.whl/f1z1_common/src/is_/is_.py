# @Time     : 2021/8/12
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import iscoroutine, iscoroutinefunction, isfuture, Task
from collections.abc import Iterable, Callable
from enum import Enum
from operator import is_, is_not, not_
from pathlib import Path


class is_validate(object):
    PY_OBJ = (
        str,
        int, float,
        bool,
        dict,
        list, tuple
    )

    @staticmethod
    def is_string(value):
        return isinstance(value, str)

    @staticmethod
    def is_bstring(value):
        return isinstance(value, bytes)

    @staticmethod
    def is_bstring_array(value):
        return isinstance(value, bytearray)

    @staticmethod
    def is_any_string(value):
        return any([
            is_validate.is_string(value),
            is_validate.is_bstring(value)
        ])

    @staticmethod
    def is_boolean(value):
        return isinstance(value, bool)

    @staticmethod
    def is_list(value):
        return isinstance(value, list)

    @staticmethod
    def is_set(value):
        return isinstance(value, set)

    @staticmethod
    def is_tup(value):
        return isinstance(value, tuple)

    @staticmethod
    def is_dict(value):
        return isinstance(value, dict)

    @staticmethod
    def is_enum(value):
        return isinstance(value, Enum)

    @staticmethod
    def is_null(value):
        return is_(value, None)

    @staticmethod
    def is_not_null(value):
        return is_not(value, None)

    @staticmethod
    def is_int(value):
        return isinstance(value, int)

    @staticmethod
    def is_float(value):
        return isinstance(value, float)

    @staticmethod
    def is_number(value):
        return any([
            is_validate.is_int(value),
            is_validate.is_float(value)
        ])

    @staticmethod
    def is_path(value):
        return isinstance(value, Path)

    @staticmethod
    def is_iterable(value):
        return isinstance(value, Iterable)

    @staticmethod
    def is_function(value):
        return isinstance(value, Callable)

    @staticmethod
    def is_coroutine(value):
        return iscoroutine(value)

    @staticmethod
    def is_async_function(value):
        return iscoroutinefunction(value)

    @staticmethod
    def is_fut(value):
        return isfuture(value)

    @staticmethod
    def is_coroutine_task(value):
        return isinstance(value, Task)

    @staticmethod
    def is_py_empty(value):
        return not_(value)

    @staticmethod
    def is_py_obj(value):
        return isinstance(value, is_validate.PY_OBJ)
