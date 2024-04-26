"""
存放关于生态缸的数据
"""
from math import sin

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QLinearGradient
from PIL import ImageGrab

from computer_info.manager import COMPUTER_INFO, SYSTEM_INFO_MANAGER
from tools.color import get_color_by_linear_ratio


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

        # 水位线高度线，y值
        self.water_level_height = 0
        # 底部沙子高度，y值
        self.sand_surface_height = 0
        self.sand_base_height = 0

        # 生态缸颜色
        self.water_color_best = QColor(40, 100, 255, 40)
        self.water_color_worst = QColor(200, 150, 50, 40)

        # 顶部灯光亮度 0 表示黑 1表示最亮
        self.light_brightness_target = 1
        self.light_brightness_current = 0

        self.time = 0
        self.tick()  # 初始化的时候就将高度信息更新好

    def tick(self):
        """
        生态缸更新一次
        """
        # 更新内存信息
        # self.sand_surface_height = self.height * COMPUTER_INFO["physical_memory"]["total"] / (
        #         COMPUTER_INFO["physical_memory"]["total"] + COMPUTER_INFO["swap_memory"]["total"]
        # )
        memory_info = SYSTEM_INFO_MANAGER.INSPECTOR_MEMORY.get_current_result()
        self.sand_surface_height = self.height * memory_info.physical_memory_total / (
                memory_info.physical_memory_total + memory_info.swap_memory_total
        )
        # self.water_level_height = self.sand_surface_height * COMPUTER_INFO["physical_memory"]["percent"]
        self.water_level_height = self.sand_surface_height * memory_info.physical_memory_percent

        # self.sand_base_height = self.sand_surface_height + (
        #         self.height - self.sand_surface_height
        # ) * COMPUTER_INFO["swap_memory"]["percent"]

        self.sand_base_height = self.sand_surface_height + (
                self.height - self.sand_surface_height
        ) * memory_info.swap_memory_percent
        # 更新亮度
        # self.light_brightness_target = COMPUTER_INFO["screen_light"]
        self.light_brightness_target = SYSTEM_INFO_MANAGER.INSPECTOR_SCREEN.get_current_result()
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
        # x 前面的参数才能改变频率
        return wave_amplitude * sin((x + self.time * wave_speed) * wave_frequency * 0.2)

    def paint(self, painter: QPainter):
        # 绘制顶部灯光
        painter.setPen(Qt.NoPen)
        gradient = QLinearGradient(0, 0, 0, self.water_level_height)
        gradient.setColorAt(
            0.0,
            QColor(
                255,
                255,
                255,
                round(255 * self.light_brightness_current)
            )
        )  # 开始颜色
        gradient.setColorAt(
            1.0,
            QColor(255, 255, 255, 0)
        )  # 结束颜色

        # 填充波浪形水，（定积分画法）
        painter.setPen(Qt.NoPen)
        painter.setBrush(
            get_color_by_linear_ratio(
                self.water_color_best,
                self.water_color_worst,
                # COMPUTER_INFO["c_disk_usage"]
                SYSTEM_INFO_MANAGER.INSPECTOR_DISK.get_current_result()
            )
        )
        dx = 10
        # x, x_next = 0, 10
        x, x_next = -dx, 0  # 不知道为啥第一个和之后的颜色不一样，只好让第一个画不出来
        # recv_speed = COMPUTER_INFO["network_speed"]["recv_speed"]
        recv_speed = SYSTEM_INFO_MANAGER.INSPECTOR_NETWORK.get_current_result().recv_speed
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

        # 表层颜色应该更深，浅层颜色应该更浅，因为表层是污染层，深层有石英石

        # 绘制表面层
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(62, 53, 28))
        painter.drawRect(
            0,
            round(self.sand_surface_height),
            round(self.width),
            round(self.height - self.sand_surface_height),
        )
        # 绘制深层
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(92, 73, 36))
        painter.drawRect(
            0,
            round(self.sand_base_height) + 1,  # 加1是为了防止两层完全重合，表层看不到
            round(self.width),
            round(self.height - self.sand_base_height),
        )
        # 绘制生态缸边框
        painter.setPen(Qt.green)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, self.width - 1, self.height)
        painter.end()
        pass


LIFE_TANK = _LifeTank(300, 1000, 0, "normal")
