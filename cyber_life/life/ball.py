from random import random, randint

from PyQt5.QtGui import QPainter, QColor, QPen

from cyber_life.tools.compute import lerp
from cyber_life.tools.vector import Vector
from .life_mixin.breathable_mixin import BreathableMixin
from .life_mixin.organism_mixin import OrganismMixin
from .tank import LIFE_TANK


class LifeBall(BreathableMixin, OrganismMixin):
    """
    生物球，用于反应CPU每个核的使用状态
    可以看作生物球是一个绿色植物细胞
    当CPU核处于运算状态时，生物球的呼吸作用会显著，颜色变黄，移动速度增加，体积变大，表示兴奋。
    当CPU核处于空闲状态时，生物球没有呼吸作用，光合作用主导，颜色变绿。
    """

    def __init__(self):
        super().__init__()
        x = randint(0, LIFE_TANK.width)
        y = randint(
            round(LIFE_TANK.division[0]),
            round(LIFE_TANK.division[1])
        )
        # 球心坐标
        self.location = Vector(x, y)
        self.radius = 4
        # 随机速度
        self.velocity = Vector(random() * 2 - 1, random() * 2 - 1).normalize() * 0.1
        self.acceleration = Vector(0, 0)

        # 活跃程度，越大越活跃 0 ~ 1.0
        self.activity = 0.0
        # 界定颜色变化的范围
        self.color_default = QColor(10, 150, 10)
        self.color_active = QColor(255, 255, 0)

        # 固定的碳
        self.fixed_carbon = 100
        self.o2_pre_request = 0.01
        self.co2_pre_request = 0.04

    def set_activity(self, activity):
        assert isinstance(activity, float)

        self.activity = activity
        # 让速度方向向垂直向上的方向旋转一定程度
        self.velocity = self.velocity.rotate(activity * 15)
        # 让活跃度和呼吸作用相关联
        self.o2_pre_request = 0.01 + self.activity

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
        if self.location.y < LIFE_TANK.division[0]:
            self.velocity.y = abs(self.velocity.y)
            self.location.y = LIFE_TANK.division[0]
        # 低于缸底，必须让球回到缸底
        if self.location.y > LIFE_TANK.division[1] - self.radius:
            self.velocity.y = -abs(self.velocity.y)
            self.location.y = LIFE_TANK.division[1] - self.radius

        # 光合优先于呼吸
        self.photosynthesis()
        self.breath()

    def paint(self, painter: QPainter):
        # 设置画笔颜色和线条宽度
        pen = QPen(QColor(23, 76, 23))
        pen.setWidth(2)  # 设置线条宽度为2像素
        painter.setPen(pen)

        # 设置画刷颜色和样式
        painter.setBrush(
            lerp(
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
