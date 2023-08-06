# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod


class IRunner(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass
