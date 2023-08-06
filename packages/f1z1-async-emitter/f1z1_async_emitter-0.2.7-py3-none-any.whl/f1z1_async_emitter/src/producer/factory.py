# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common.src.time_ import UnitOfTime

from ..components.gather import AwaitBufferQueue, QueueGather, SetGather
from ..components.record import RecorderChain
from ..components.speed import Speed, IntOrFloat
from .base import IWorkerFactory
from .builder import Int2E16
from .worker import WorkerGroup
from .master import WorkerMaster


class WorkerGroupFactory(IWorkerFactory):
    """
    worker group factory
    """

    @classmethod
    def create(cls,
               count: int = Int2E16,
               speed: IntOrFloat = 10,
               speed_unit: UnitOfTime = UnitOfTime.MILLISECOND) -> WorkerGroup:
        less = cls._less_count(count)
        return WorkerGroup(
            AwaitBufferQueue(Speed(speed, speed_unit), less),
            QueueGather(less),
            RecorderChain()
        )

    @classmethod
    def _less_count(cls, count: int):
        return min(abs(count), Int2E16)


class WorkerMasterFactory(IWorkerFactory):
    """
    worker master factory
    """

    @classmethod
    def create(cls, maxsize: int = None) -> WorkerMaster:
        return WorkerMaster(SetGather(maxsize), RecorderChain())
