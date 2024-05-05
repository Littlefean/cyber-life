from threading import Thread

import time
from typing import List, Callable
from tools.singleton import SingletonMeta
from .inspector_abc import Inspector
from .inspector_cpu import InspectorCpu
from .inspector_memory import InspectorMemory
from .inspector_disk_usage import InspectorDiskUsage
from .inspector_screen import InspectorScreen
from .inspector_network import InspectorNetwork
from .inspector_disk_io import InspectorDiskIO


class _SystemInfoManager(metaclass=SingletonMeta):
    """
    管理系统信息的各个模块，包括CPU、内存、磁盘、屏幕、网络等，并提供统一的接口
    """
    INSPECTOR_CPU = InspectorCpu()
    INSPECTOR_MEMORY = InspectorMemory()
    INSPECTOR_DISK_USAGE = InspectorDiskUsage()
    INSPECTOR_SCREEN = InspectorScreen()
    INSPECTOR_NETWORK = InspectorNetwork()
    INSPECTOR_DISK_IO = InspectorDiskIO()

    def __init__(self):
        self.interval_functions: List[Callable] = []
        pass

    def start(self):
        """
        让自身的每一个监测者开始监测
        :return:
        """
        # 先初始化所有监测者的线程调用函数
        for attr in dir(self):  # 获取实例的属性、方法列表（字符串形式）
            if attr.startswith('INSPECTOR_'):  # 找到'INSPECTOR_'开头的属性和方法
                instance = getattr(self, attr)  # 得到实例'INSPECTOR_'开头的属性和方法（对象形式）
                if isinstance(instance, Inspector):  # 进一步确认是所需对象，即各个监控类的实例
                    self.interval_functions.append(
                        self._get_interval_function(  # 创建定时器，周期执行监控类实例的inspect方法
                            instance.inspect,
                            instance.INSPECTION_INTERVAL,
                        )
                    )
        # 启动所有监测者的线程
        for function in self.interval_functions:
            Thread(target=function, daemon=True).start()

    @staticmethod
    def _get_interval_function(inspect_function: Callable, interval=1):
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
