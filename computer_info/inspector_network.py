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
            # self.network_speeds = NetworkSpeed(sent_diff / interval, recv_diff / interval)
            network_speeds[interface] = {
                'sent_speed': sent_diff / interval,
                'recv_speed': recv_diff / interval,
            }

        self.network_speeds = NetworkSpeed(**network_speeds["WLAN"])
