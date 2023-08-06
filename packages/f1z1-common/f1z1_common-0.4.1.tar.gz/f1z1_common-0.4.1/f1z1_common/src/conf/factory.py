# @Time     : 2021/5/31
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from typing import Optional

from ..utils import PathUtil, PathTypes, EncodingType
from .base import AbstractConfReader
from .reader import IniReader, JsonReader


class IReaderFactory(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def create(cls, file: PathTypes, encoding: Optional[EncodingType] = None) -> AbstractConfReader:
        raise NotImplementedError("NotImplemented .create() -> AbstractConfReader")


class ReaderFactory(IReaderFactory):

    @classmethod
    def create(cls, file: PathTypes, encoding: Optional[EncodingType] = None):
        if cls.is_ini(file):
            return IniReader(file, encoding)
        elif cls.is_json(file):
            return JsonReader(file, encoding)
        else:
            raise ValueError(f"file ext name error, {file}")

    @staticmethod
    def is_json(file):
        return PathUtil.is_endswith_ext(file, [".json"])

    @staticmethod
    def is_ini(file):
        return PathUtil.is_endswith_ext(file, [".ini"])
