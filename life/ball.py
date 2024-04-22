from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor

from tools.vector import Vector
from tools.color import get_color_by_linear_ratio
from random import random, randint
from .tank import LIFE_TANK


class LifeBall:
    """
    生物球，用于反应CPU每个核的使用状态
    可以看作生物球是一个绿色植物细胞
    当CPU核处于运算状态时，生物球的呼吸作用会显著，颜色变黄，移动速度增加，体积变大，表示兴奋。
    当CPU核处于空闲状态时，生物球没有呼吸作用，光合作用主导，颜色变绿。
    """

    def __init__(self):
        x, y = randint(0, LIFE_TANK.width), randint(0, LIFE_TANK.height)
        # 球心坐标
        self.location = Vector(x, y)
        self.radius = 4
        # 随机速度
        self.velocity = Vector(random() * 2 - 1, random() * 2 - 1).normalize() * 0.2
        self.acceleration = Vector(0, 0)

        # 活跃程度，越大越活跃 0 ~ 1.0
        self.activity = 0.0
        # 界定颜色变化的范围
        self.color_default = QColor(10, 150, 10)
        self.color_active = QColor(255, 255, 0)

    def set_activity(self, activity):
        if isinstance(activity, float):
            self.activity = activity
        else:
            print("Error: activity must be a float number.")
            raise TypeError

    def tick(self):
        self.velocity += self.acceleration
        self.location += self.velocity * (1 + self.activity * 50)
        # 左右边界检测
        if self.location.x - self.radius < 0:
            self.velocity.x = abs(self.velocity.x)
        elif self.location.x + self.radius > LIFE_TANK.width:
            self.velocity.x = -abs(self.velocity.x)
        # 上下边界检测
        # 高出水位线，必须让球掉入水中
        if self.location.y < LIFE_TANK.water_level_height:
            self.velocity.y = abs(self.velocity.y)
        # 低于缸底，必须让球回到缸底
        if self.location.y > LIFE_TANK.height - self.radius:
            self.velocity.y = -abs(self.velocity.y)

    def paint(self, painter: QPainter):
        # 画出球
        painter.setPen(Qt.NoPen)
        painter.setBrush(
            get_color_by_linear_ratio(
                self.color_default,
                self.color_active,
                self.activity
            )
        )
        painter.drawEllipse(
            round(self.location.x - self.radius),
            round(self.location.y - self.radius),
            round(self.radius * 2 + (self.activity * 20)),
            round(self.radius * 2 + (self.activity * 20))
        )
        pass
