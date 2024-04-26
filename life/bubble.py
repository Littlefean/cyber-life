from tools.vector import Vector
from random import random
from .tank import LIFE_TANK
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


class LifeBubble:
    """
    单个气泡的类
    """

    def __init__(self, x):
        self.location = Vector(x, LIFE_TANK.sand_surface_height)
        self.velocity = Vector(0, 0)
        # 默认有一个向上的加速度，因为有浮力
        self.acceleration = Vector(0, -0.01)

        # 规定气泡大小的变化动态范围
        self.radius_min = 2
        self.radius_max = 4
        # 当气泡脱离生态缸时，气泡变为死亡状态
        self.is_alive = True

    @property
    def radius(self):
        """
        气泡的半径大小，由自身位置在生态缸中的位置决定
        因为越接近水面，压强越小，气泡的半径越大。
        """
        # 气泡到达水面的进度 0~1
        rate = (LIFE_TANK.sand_surface_height - self.location.y) / (
                    LIFE_TANK.sand_surface_height - LIFE_TANK.water_level_height)
        return self.radius_min + (self.radius_max - self.radius_min) * rate

    def tick(self):
        if self.location.y < LIFE_TANK.water_level_height:
            self.is_alive = False
        self.velocity += self.acceleration
        self.location += self.velocity
        # 增加气泡左右随机移动的效果
        self.location.x += (random() - 0.5) * 0.5

    def paint(self, painter: QPainter):
        painter.setPen(Qt.cyan)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(
            round(self.location.x - self.radius),
            round(self.location.y - self.radius),
            round(2 * self.radius),
            round(2 * self.radius)
        )
        pass
