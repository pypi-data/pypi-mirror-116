# @Time     : 2021/5/26
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr, Union

from ..is_ import is_validate

StringOrBytesOrByteArray = Union[AnyStr, bytearray]
EncodingType = str


class Encoding:
    """
    默认编码方式
    """
    ASCII = "ascii"
    ISO_8859_1 = "ISO-8859-1"
    UTF_8 = "utf-8"


class StringsUtil(object):

    @classmethod
    def anystr_to_string(cls, str_or_bytes: AnyStr, encoding: EncodingType = None) -> str:
        """
        string or bytes to string
        :param str_or_bytes:
        :param encoding:
        :return:
        """
        string: str = ""
        if is_validate.is_string(str_or_bytes):
            string = str_or_bytes
        elif is_validate.is_bstring(str_or_bytes):
            string = str_or_bytes.decode(encoding=encoding)
        else:
            raise ValueError(f"need a string or bytes, but got {type(str_or_bytes).__name__}")
        return string

    @classmethod
    def anystr_to_bytes(cls, str_or_bytes_barray: StringOrBytesOrByteArray) -> bytes:
        """
        string, bytes, bytearray to bytes
        :param str_or_bytes_barray:
        :return:
        """
        bstring: bytes = b""
        if any([
            is_validate.is_bstring(str_or_bytes_barray),
            is_validate.is_bstring_array(str_or_bytes_barray)
        ]):
            bstring = str_or_bytes_barray
        elif is_validate.is_string(str_or_bytes_barray):
            bstring = str_or_bytes_barray.encode()
        else:
            raise ValueError(f"need string, bytes, bytearray, but got {type(str_or_bytes_barray).__name__}")
        return bstring
