# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Union

from f1z1_common.src.time_ import UnitOfTime
from f1z1_common.src.task import CoroOrFunction, ArgsTypes, KwargsTypes
from f1z1_async_runner.src import create_runner, start

from .base import IWorker
from .builder import Int2E16, CounterWorkerBuilder, TimeoutWorkerBuilder
from .factory import WorkerGroupFactory, WorkerMasterFactory

IntOrFloat = Union[int, float]


def is_worker(value):
    return isinstance(value, IWorker)


def counter_worker(
        coro_or_func: CoroOrFunction,
        args: ArgsTypes = None,
        kwargs: KwargsTypes = None,
        thread_workers: int = None
):
    return CounterWorkerBuilder(
        coro_or_func, args=args, kwargs=kwargs, thread_workers=thread_workers
    )


def timeout_worker(
        coro_or_func: CoroOrFunction,
        args: ArgsTypes = None,
        kwargs: KwargsTypes = None,
        thread_workers: int = None
):
    return TimeoutWorkerBuilder(
        coro_or_func, args=args, kwargs=kwargs, thread_workers=thread_workers
    )


def create_group(count: int = Int2E16,
                 speed: IntOrFloat = 10,
                 speed_unit: UnitOfTime = UnitOfTime.MILLISECOND):
    return WorkerGroupFactory.create(count, speed, speed_unit)


def create_master(maxsize: int = None):
    return WorkerMasterFactory.create(maxsize)


def run(worker: IWorker):
    if not is_worker(worker):
        raise ValueError(
            f"worker need IWorker, but got {type(worker).__name__}"
        )
    runner = create_runner(worker.start())
    return start(runner)
