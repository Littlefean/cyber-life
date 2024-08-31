import time

import psutil

from .inspector_abc import Inspector


class NetworkSpeed:
    """单独写一个类，只是为了有type hint"""

    def __init__(self, sent_speed, recv_speed):
        self.sent_speed = sent_speed
        self.recv_speed = recv_speed

    def reset(self):
        self.sent_speed = 0
        self.recv_speed = 0


class InspectorNetwork(Inspector):
    INSPECTION_INTERVAL = 1

    def __init__(self):
        super().__init__()
        self.network_speeds = NetworkSpeed(0, 0)
        self.inspect()

    def get_current_result(self) -> NetworkSpeed:
        return self.network_speeds

    def inspect(self):
        # 这是新的 inspect 方法
        # 旧的改名为 _old_inspect
        # 不确定新的是否在所有电脑上都能正常工作，所以保留旧的
        # TODO: 移除 _old_inspect 方法

        interval = 0.5  # 采样间隔

        # 采样网络信息

        # psutil.net_io_counters() 函数 pernic=False 表示获取所有网络接口的统计信息
        # 已经求和，无需遍历

        first_stats = psutil.net_io_counters()
        time.sleep(interval)  # 等待指定时间间隔
        second_stats = psutil.net_io_counters()

        # 更新网络速度
        self.network_speeds.sent_speed = (second_stats.bytes_sent - first_stats.bytes_sent) / interval
        self.network_speeds.recv_speed = (second_stats.bytes_recv - first_stats.bytes_recv) / interval

    def _old_inspect(self):
        interval = 0.5  # 采样间隔
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

        # 直接将字典中每一项累加
        # 这样网络信息可能来自无线，有线，以太网，所以需要遍历所有接口

        self.network_speeds.reset()  # 一定要先重置

        for k, v in network_speeds.items():
            self.network_speeds.sent_speed += v['sent_speed']
            self.network_speeds.recv_speed += v['recv_speed']
            print(k, v)
        print("\n" * 4)
