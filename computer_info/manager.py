from threading import Thread

import psutil

import time
from typing import List, Callable
from PIL import ImageGrab
from random import randint

from .inspector_abc import Inspector
from .inspector_cpu import InspectorCpu
from .inspector_memory import InspectorMemory
from .inspector_disk import InspectorDisk
from .inspector_screen import InspectorScreen
from .inspector_network import InspectorNetwork


class _SystemInfoManager:
    """
    单例模式 + 外观模式 + 策略模式
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


def get_memory_usage_percent() -> float:
    """获取内存使用率"""
    mem_info = psutil.virtual_memory()
    return mem_info.percent / 100.0


COMPUTER_INFO = {
    "memory": get_memory_usage_percent(),
    "physical_memory": {
        "total": psutil.virtual_memory().total,
        "percent": psutil.virtual_memory().percent / 100.0
    },
    "swap_memory": {
        "total": psutil.swap_memory().total,
        "percent": psutil.swap_memory().percent / 100.0
    },
    "cpu": [0.0 for _ in range(psutil.cpu_count())],
    "c_disk_usage": psutil.disk_usage('C:').percent / 100,
    "screen_light": 0.0,
    "network_speed": {
        "sent_speed": 0.0,
        "recv_speed": 0.0
    }
}


def update_computer_info():
    # 内存
    COMPUTER_INFO["memory"] = get_memory_usage_percent()
    COMPUTER_INFO["physical_memory"]["percent"] = psutil.virtual_memory().percent / 100.0
    COMPUTER_INFO["swap_memory"]["percent"] = psutil.swap_memory().percent / 100.0

    # CPU
    new_cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
    for i in range(len(new_cpu_percent)):
        COMPUTER_INFO["cpu"][i] = new_cpu_percent[i] / 100.0
    # 磁盘
    COMPUTER_INFO["c_disk_usage"] = psutil.disk_usage('C:').percent / 100

    # 屏幕亮度
    # 通过PIL截图，随机抽取一些像素点，来判断当前屏幕内容的亮度
    try:  # 因为发现休眠后会因为捕捉不到屏幕而报错，线程终止，无法更新系统信息
        im = ImageGrab.grab()
        width, height = im.size
        for i in range(100):
            x = randint(0, width - 1)
            y = randint(0, height - 1)
            r, g, b = im.getpixel((x, y))
            COMPUTER_INFO["screen_light"] += (r + g + b) / 3.0 / 255.0
        COMPUTER_INFO["screen_light"] /= 100.0
    except OSError:
        print('screen grab failed')

    # 网络速度
    network_speeds = get_network_speed()
    COMPUTER_INFO["network_speed"] = network_speeds['WLAN']


def get_network_speed(interval=1.0):  # 时间间隔单位为秒
    first_stats = psutil.net_io_counters(pernic=True)

    time.sleep(interval)  # 等待指定时间间隔

    second_stats = psutil.net_io_counters(pernic=True)

    network_speeds = {}
    for interface in set(first_stats.keys()).intersection(second_stats.keys()):
        sent_diff = second_stats[interface].bytes_sent - first_stats[interface].bytes_sent
        recv_diff = second_stats[interface].bytes_recv - first_stats[interface].bytes_recv

        network_speeds[interface] = {
            'sent_speed': sent_diff / interval,
            'recv_speed': recv_diff / interval,
        }

    return network_speeds


def update_computer_info_timer():
    """更新的定时器，用于其他子线程调用"""
    while True:
        update_computer_info()
        time.sleep(2)
