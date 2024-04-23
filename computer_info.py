import psutil

import time
from PIL import ImageGrab
from random import randint


def get_memory_usage_percent():
    mem_info = psutil.virtual_memory()
    return mem_info.percent / 100.0


COMPUTER_INFO = {
    "memory": get_memory_usage_percent(),
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

    # CPU
    new_cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
    for i in range(len(new_cpu_percent)):
        COMPUTER_INFO["cpu"][i] = new_cpu_percent[i] / 100.0
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
