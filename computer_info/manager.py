from threading import Thread

import time
from typing import List, Callable
from tools.singleton import SingletonMeta
from .inspector_abc import Inspector
from .inspector_cpu import InspectorCpu
from .inspector_memory import InspectorMemory
from .inspector_disk import InspectorDisk
from .inspector_screen import InspectorScreen
from .inspector_network import InspectorNetwork


class _SystemInfoManager(metaclass=SingletonMeta):
    """
    管理系统信息的各个模块，包括CPU、内存、磁盘、屏幕、网络等，并提供统一的接口
    """
    INSPECTOR_CPU = InspectorCpu()
    INSPECTOR_MEMORY = InspectorMemory()
    INSPECTOR_DISK = InspectorDisk()
    INSPECTOR_SCREEN = InspectorScreen()
    INSPECTOR_NETWORK = InspectorNetwork()

    def __init__(self):
        self.interval_functions: List[Callable] = []
        pass

    def start(self):
        """
        让自身的每一个监测者开始监测
        :return:
        """
        # 先初始化所有监测者的线程调用函数
        for attr in dir(self):
            if attr.startswith('INSPECTOR_'):
                instance = getattr(self, attr)
                if isinstance(instance, Inspector):
                    self.interval_functions.append(
                        self.get_interval_function(
                            instance.inspect,
                            instance.INSPECTION_INTERVAL,
                        )
                    )
        # 启动所有监测者的线程
        for function in self.interval_functions:
            Thread(target=function, daemon=True).start()

    @staticmethod
    def get_interval_function(inspect_function: Callable, interval=1):
        """获取定时器函数"""

        def timer_function():
            while True:
                inspect_function()
                time.sleep(interval)

        return timer_function

    def stop(self):
        # 暂时不做停止操作，因为没有必要
        pass


SYSTEM_INFO_MANAGER = _SystemInfoManager()
