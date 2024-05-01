"""
存放关于小鱼缸的数据
"""
from math import sin

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QLinearGradient
from PIL import ImageGrab

from computer_info.manager import SYSTEM_INFO_MANAGER
from life.sand_wave_flow import SandWaveFlow
from service.settings import SETTINGS
from tools.color import get_color_by_linear_ratio
from tools.singleton import SingletonMeta


class _LifeTank(metaclass=SingletonMeta):
    """
    存放关于小鱼缸的数据
    绘制水面、沙子表面层和深层、沙层中的震荡波，并进行更新
    """
    _COLOR_DEBUG = False

    def __init__(self, width: int):
        """
        初始化小鱼缸数据
        :param width: 界面大小宽度，px
        """
        self.width = int(width)
        # 获取屏幕的宽度和高度
        w, h = ImageGrab.grab().size
        self.height = int(self.width * (h / w))

        # 水位线高度线，y值
        self.water_level_height = 0
        # 底部沙子高度，y值，为固定值，不进行更新
        self.sand_base_height = 0

        # 小鱼缸颜色
        self.water_color_best = QColor(40, 100, 255, 40)
        # 将棕色作为最差颜色，不太好，容易和沙子颜色混淆
        # self.water_color_worst = QColor(200, 150, 50, 40)
        self.water_color_worst = QColor(22, 135, 67, 40)

        # 顶部灯光亮度 0 表示黑 1表示最亮
        self.light_brightness_target = 1
        self.light_brightness_current = 0

        # 震荡圆圈特效
        # 向外扩散的是写入磁盘的速度，向内扩散的是读取磁盘的速度
        # 因为扩散波像是某个东西掉入地上，成为了地面的一部分，可以代表写入
        # 实际上沙子地面代表了硬盘
        self.sand_wave_outer = SandWaveFlow(self.width / 2, 1)
        self.sand_wave_inner = SandWaveFlow(self.width / 2, -1)

        self.time = 0
        self.tick()  # 初始化的时候就将高度信息更新好

    @property
    def sand_surface_height(self):
        if SETTINGS.is_swap_memory_fixed:
            return self.height * (1 - SETTINGS.swap_memory_height_rate)
        else:
            memory_info = SYSTEM_INFO_MANAGER.INSPECTOR_MEMORY.get_current_result()
            return self.height * memory_info.physical_memory_total / (
                    memory_info.physical_memory_total + memory_info.swap_memory_total
            )

    def tick(self):
        """
        小鱼缸更新一次
        """
        # 更新内存信息
        memory_info = SYSTEM_INFO_MANAGER.INSPECTOR_MEMORY.get_current_result()

        # 水的深度表示物理内存剩余
        self.water_level_height = self.sand_surface_height * memory_info.physical_memory_percent

        # 沙子深层厚度表示交换内存剩余
        self.sand_base_height = self.sand_surface_height + (
                self.height - self.sand_surface_height
        ) * memory_info.swap_memory_percent
        # 更新亮度
        self.light_brightness_target = SYSTEM_INFO_MANAGER.INSPECTOR_SCREEN.get_current_result()
        self.light_brightness_current = self.light_brightness_target * 0.01 + self.light_brightness_current * 0.99
        self.time += 1
        # 更新震荡数据
        self.sand_wave_outer.set_frequency_by_disk_io(
            SYSTEM_INFO_MANAGER.INSPECTOR_DISK_IO.get_current_result().write_bytes
        )
        self.sand_wave_inner.set_frequency_by_disk_io(
            SYSTEM_INFO_MANAGER.INSPECTOR_DISK_IO.get_current_result().read_bytes
        )
        # 更新震荡圆圈列表
        self.sand_wave_outer.tick()
        self.sand_wave_inner.tick()

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
        if self._COLOR_DEBUG:
            # water_color_ratio = 0.5 * sin(self.time * 0.01) + 0.5
            water_color_ratio = (0.005 * self.time) % 1
        else:
            water_color_ratio = SYSTEM_INFO_MANAGER.INSPECTOR_DISK_USAGE.get_current_result()

        painter.setBrush(get_color_by_linear_ratio(
            self.water_color_best,
            self.water_color_worst,
            water_color_ratio
        ))
        # 绘制水面
        dx = 10
        x, x_next = -dx, 0  # 不知道为啥第一个和之后的颜色不一样，只好让第一个画不出来
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

        # 表层颜色应该更深，深层颜色应该更浅，因为表层是污染层，深层有石英石

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
        # 绘制波浪圆圈
        self.sand_wave_outer.paint(painter)
        self.sand_wave_inner.paint(painter)
        # 绘制小鱼缸边框
        painter.setPen(Qt.green)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, self.width - 1, self.height)
        painter.end()
        pass


LIFE_TANK = _LifeTank(300)
