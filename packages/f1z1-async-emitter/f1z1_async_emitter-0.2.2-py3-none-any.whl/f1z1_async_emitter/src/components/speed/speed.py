# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import sleep
from collections.abc import Awaitable
from functools import lru_cache
from typing import Union

from f1z1_common.src import timeunt
from f1z1_common.src.time_ import UnitOfTime

from .base import IAwaitSpeed

IntOrFloat = Union[int, float]


class Speed(Awaitable, IAwaitSpeed):

    def __init__(self, int_or_float: IntOrFloat, speed_unt: UnitOfTime):
        self._speed = int_or_float
        self._timeunt = timeunt(speed_unt)

    def __await__(self):
        return self._await_impl().__await__()

    async def _await_impl(self):
        return await sleep(self._use_lru_cache())

    @lru_cache()
    def _use_lru_cache(self) -> float:
        return self._timeunt.convert(self._speed)

    def __str__(self):
        return f"{self.__class__.__name__}(speed={self._use_lru_cache()})"
