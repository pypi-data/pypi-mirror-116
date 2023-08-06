# @Time     : 2021/5/31
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ..utils import StringsUtil
from ..is_ import is_validate


class ReaderUtil(object):

    @staticmethod
    def to_int(value):
        if is_validate.is_int(value):
            return value
        elif is_validate.is_number(value):
            return int(value)
        else:
            raise ValueError(f"value need float or int, but got {type(value).__name__}")

    @staticmethod
    def to_float(value):
        if is_validate.is_float(value):
            return value
        elif is_validate.is_number(value):
            return float(value)
        else:
            raise ValueError(f"value need float or int, but got {type(value).__name__}")

    @staticmethod
    def to_string(value):
        if is_validate.is_string(value):
            return value
        elif is_validate.is_any_string(value):
            return StringsUtil.anystr_to_string(value)
        return str(value)
