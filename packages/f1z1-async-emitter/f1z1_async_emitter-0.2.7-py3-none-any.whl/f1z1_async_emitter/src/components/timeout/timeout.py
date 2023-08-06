# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from datetime import datetime
from typing import Union

from f1z1_common.src import timestamp
from f1z1_common.src.time_ import UnitOfTime

from .base import ITimeout


class Timeout(ITimeout):
    __slots__ = "_st", "_timeout", "_timestamp"

    def __init__(self,
                 int_or_float: Union[int, float],
                 unit: UnitOfTime):
        self._timeout = int_or_float
        self._timestamp = timestamp(unit)
        self._st = 0

    def start(self) -> None:
        self._st = self._current()

    def is_timeout(self) -> bool:
        return self._is_timeout()

    def _current(self):
        return datetime.now().timestamp()

    def _is_timeout(self):
        return self._timestamp.convert(self._current() - self._st) >= self._timeout

    def __str__(self):
        return f"{self.__class__.__name__}(timeout={self._timeout}, st={self._st})"
