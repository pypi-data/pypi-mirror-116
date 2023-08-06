# @Time     : 2021/8/13
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import AbstractEventLoop

from .base import IRunner
from .arunner import AsyncRunner


def is_runner(value):
    return isinstance(value, IRunner)


def create_runner(coro_or_func, *,
                  eloop: AbstractEventLoop = None,
                  max_workers: int = None,
                  args=None,
                  kwargs=None):
    """
    runner factory
    :param coro_or_func:
    :param eloop:
    :param max_workers:
    :param args:
    :param kwargs:
    :return:
    """
    return AsyncRunner(
        coro_or_func,
        eloop=eloop,
        max_workers=max_workers,
        args=args,
        kwargs=kwargs
    )


def start(runner: IRunner):
    if not is_runner(runner):
        raise ValueError(f"runner need IRunner instance, but got {type(runner).__name__}")
    return runner.run()
