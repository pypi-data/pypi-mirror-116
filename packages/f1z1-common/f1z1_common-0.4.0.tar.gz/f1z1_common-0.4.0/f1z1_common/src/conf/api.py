# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ..utils import PathTypes, EncodingType
from .factory import ReaderFactory


def conf_reader(file: PathTypes, encoding: EncodingType = None):
    return ReaderFactory.create(file, encoding)
