import time
from threading import Thread, Event
from typing import List, Callable

from cyber_life.tools.singleton import SingletonMeta
from .inspector_abc import Inspector
from .inspector_cpu import InspectorCpu
from .inspector_disk_io import InspectorDiskIO
from .inspector_disk_usage import InspectorDiskUsage
from .inspector_memory import InspectorMemory
from .inspector_network import InspectorNetwork
from .inspector_screen import InspectorScreen


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
        self._interval_functions: List[Callable] = []
        self._is_running = False
        self._threads: List[Thread] = []
        self._event: Event = Event()

        # 先初始化所有监测者的线程调用函数
        for attr in dir(self):  # 获取实例的属性、方法列表（字符串形式）
            # 找到'INSPECTOR_'开头的属性和方法，并判断是否是Inspector类的实例
            if attr.startswith('INSPECTOR_') and isinstance(instance := getattr(self, attr), Inspector):
                self._interval_functions.append(
                    self._get_interval_function(  # 创建定时器，周期执行监控类实例的inspect方法
                        instance.inspect,
                        instance.INSPECTION_INTERVAL,
                    )
                )
        # 初始化线程列表
        for function in self._interval_functions:
            self._threads.append(Thread(target=function, daemon=True))

    def start(self):
        """
        让自身的每一个监测者开始监测
        :return:
        """
        if self._is_running:
            return

        # 启动所有监测者的线程
        for thread in self._threads:
            thread.start()
        self._is_running = True

    @staticmethod
    def _get_interval_function(inspect_function: Callable, interval=1):
        """获取定时器函数"""

        def timer_function():
            while True:
                inspect_function()
                time.sleep(interval)

        return timer_function

    def stop(self):
        if not self._is_running:
            return
        # 暂不需要，因为 daemon=True 的线程会自动结束


SYSTEM_INFO_MANAGER = _SystemInfoManager()
