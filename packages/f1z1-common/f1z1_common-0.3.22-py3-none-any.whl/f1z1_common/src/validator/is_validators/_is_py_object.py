# @Time     : 2021/8/11
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ._is_null import is_none

PY_OBJ = (
    str,
    int, float,
    bool,
    dict,
    list, tuple
)


def is_py_object(value):
    return any([
        isinstance(value, PY_OBJ),
        is_none(value)
    ])
