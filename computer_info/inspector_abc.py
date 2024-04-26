"""
这是一个抽象类，用于检测计算机信息。
"""
from abc import ABC, abstractmethod


class Inspector(ABC):
    """
    抽象类，用于检测计算机信息。
    每一个检测者都将会开启一个线程，每隔一段时间（INSPECTION_INTERVAL）检测一次。
    """
    INSPECTION_INTERVAL = 1  # 检测间隔，单位为秒

    @abstractmethod
    def inspect(self):
        """检测一次"""
        pass

    @abstractmethod
    def get_current_result(self):
        """获取检测结果"""
        pass
