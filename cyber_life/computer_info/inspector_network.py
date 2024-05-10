import time

import psutil

from .inspector_abc import Inspector


class NetworkSpeed:
    """单独写一个类，只是为了有type hint"""

    def __init__(self, sent_speed, recv_speed):
        self.sent_speed = sent_speed
        self.recv_speed = recv_speed


class InspectorNetwork(Inspector):
    INSPECTION_INTERVAL = 1

    def __init__(self):
        super().__init__()
        self.network_speeds = NetworkSpeed(0, 0)
        self.inspect()

    def get_current_result(self) -> NetworkSpeed:
        return self.network_speeds

    def inspect(self):
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
        for k, v in network_speeds.items():
            self.network_speeds.sent_speed += v['sent_speed']
            self.network_speeds.recv_speed += v['recv_speed']
