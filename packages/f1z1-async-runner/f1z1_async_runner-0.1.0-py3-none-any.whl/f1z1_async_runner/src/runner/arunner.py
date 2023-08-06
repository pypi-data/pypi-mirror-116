# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import run, AbstractEventLoop
from operator import not_

from f1z1_common.src import executor
from f1z1_common.src.task import ArgsTypes, CoroOrFunction, KwargsTypes

from .base import IRunner


class AsyncRunner(IRunner):

    def __init__(self,
                 coro_or_func: CoroOrFunction,
                 *,
                 eloop: AbstractEventLoop = None,
                 max_workers: int = None,
                 args: ArgsTypes = None,
                 kwargs: KwargsTypes = None):
        self._coro_or_func = coro_or_func
        self._eloop = eloop
        self._max_workers = max_workers
        self._args = () if not_(args) else args
        self._kwargs = {} if not_(args) else kwargs

    def run(self):
        return run(self.main())

    async def main(self):
        execute = executor(
            self._coro_or_func,
            eloop=self._eloop,
            max_workers=self._max_workers
        )
        return await execute.execute(*self._args, **self._kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}(coro_or_func={self._coro_or_func})"
