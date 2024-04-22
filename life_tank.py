"""
存放关于生态缸的数据
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QLinearGradient
from computer_info import COMPUTER_INFO
from PIL import ImageGrab
from math import sin


class _LifeTank:
    """
    单例模式，存放关于生态缸的数据
    """

    def __init__(self, width, capacity, level, status):
        self.width = int(width)
        # 获取屏幕的宽度和高度
        w, h = ImageGrab.grab().size
        # w =
        # h =
        self.height = int(self.width * (h / w))
        self.capacity = capacity
        self.level = level
        self.status = status

        # 水位线高度
        self.water_level_height = 0
        # 水位线颜色
        self.water_level_color = "blue"

        # 生态缸颜色
        self.water_color = get_water_color()
        # 顶部灯光亮度 0 表示黑 1表示最亮
        self.light_brightness_target = 1
        self.light_brightness_current = 0

        self.time = 0

    def tick(self):
        """
        生态缸更新一次
        """
        self.water_level_height = self.height * COMPUTER_INFO["memory"]
        self.light_brightness_target = COMPUTER_INFO["screen_light"]
        self.light_brightness_current = self.light_brightness_target * 0.01 + self.light_brightness_current * 0.99
        self.time += 1

    def get_wave_height(self, x, recv_speed):
        """
        获取波浪线高度，用于绘制sin型波浪水面
        :param x:
        :param recv_speed:
        :return:
        """
        # 波速度10为最快速度，1为最慢速度
        # 频率0.01 最长，0.1 最短
        if recv_speed < 1:
            wave_speed = 0
            wave_amplitude = 0
            wave_frequency = 0.01
        elif recv_speed < 100:
            wave_speed = 1
            wave_amplitude = 2
            wave_frequency = 0.01
        elif recv_speed < 1000:
            wave_speed = 1
            wave_amplitude = 2
            wave_frequency = 0.02
        elif recv_speed < 5000:
            wave_speed = 2
            wave_amplitude = 2
            wave_frequency = 0.04
        elif recv_speed < 1_0000:
            wave_speed = 6
            wave_amplitude = 4
            wave_frequency = 0.05
        elif recv_speed < 10_0000:
            wave_speed = 7
            wave_amplitude = 6
            wave_frequency = 0.05
        elif recv_speed < 50_0000:
            wave_speed = 8
            wave_amplitude = 8
            wave_frequency = 0.05
        elif recv_speed < 150_0000:
            wave_speed = 9
            wave_amplitude = 10
            wave_frequency = 0.06
        else:
            wave_speed = 10
            wave_amplitude = 10
            wave_frequency = 0.1

        return wave_amplitude * sin((x + self.time * wave_speed) * wave_frequency * 0.2)  # x 前面的参数才能改变频率

    def paint(self, painter: QPainter):
        # 绘制顶部灯光
        painter.setPen(Qt.NoPen)
        gradient = QLinearGradient(0, 0, 0, self.water_level_height)
        gradient.setColorAt(0.0, QColor(255, 255, 255, round(255 * self.light_brightness_current)))  # 开始颜色
        gradient.setColorAt(1.0, QColor(255, 255, 255, 0))  # 结束颜色
        # 绘制生态缸边框
        painter.setPen(Qt.green)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, self.width - 1, self.height)

        # 填充波浪形水，（定积分画法）
        painter.setPen(Qt.NoPen)
        painter.setBrush(get_water_color())
        dx = 10
        # x, x_next = 0, 10
        x, x_next = -dx, 0  # 不知道为啥第一个和之后的颜色不一样，只好让第一个画不出来
        recv_speed = COMPUTER_INFO["network_speed"]["recv_speed"]
        y, y_next = round(
            self.water_level_height + self.get_wave_height(x, recv_speed)
        ), 0
        while x < self.width:
            y_next = round(self.water_level_height + self.get_wave_height(x_next, recv_speed))
            painter.drawRect(
                x, y,
                dx, self.height - y
            )
            x, x_next = x_next, x + dx
            y, y_next = y_next, 0

        # 绘制矩形，使用渐变填充
        painter.fillRect(0, 0, self.width, self.height, gradient)

        painter.end()
        pass


def get_water_color() -> QColor:
    """
    获取生态缸水的颜色，采用线性插值计算，根据C盘使用率来确定颜色
    todo: 有待改成更改色相
    :return:
    """
    red_good = 40
    green_good = 100
    blue_good = 255
    red_bad = 200
    green_bad = 150
    blue_bad = 50
    c_disk_usage = COMPUTER_INFO["c_disk_usage"]
    red = int(red_good * c_disk_usage + (1 - c_disk_usage) * red_bad)
    green = int(green_good * c_disk_usage + (1 - c_disk_usage) * green_bad)
    blue = int(blue_good * c_disk_usage + (1 - c_disk_usage) * blue_bad)
    return QColor(red, green, blue, 40)


LIFE_TANK = _LifeTank(300, 1000, 0, "normal")
