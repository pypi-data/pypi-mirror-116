# @Time     : 2021/8/11
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
PY_OBJ = (
    str,
    int, float,
    bool,
    dict,
    list, tuple,
    None
)


def is_py_object(value):
    return isinstance(value, PY_OBJ)
