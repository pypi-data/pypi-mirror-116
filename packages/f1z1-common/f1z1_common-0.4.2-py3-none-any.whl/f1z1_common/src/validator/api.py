# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .factory import ValidatorFactory


def check_function(value):
    validator = ValidatorFactory.create_func_validator(
        f"value need function or Callable, but got {type(value).__name__}"
    )
    return validator.is_validate(value)


def check_async_function(value):
    validator = ValidatorFactory.create_afunc_validator(
        f"value need async function, but got {type(value).__name__}"
    )
    return validator.is_validate(value)
