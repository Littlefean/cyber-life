from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor

from vector import Vector
from random import random, randint
from life_tank import LIFE_TANK


class LifeBall:
    def __init__(self):
        x, y = randint(0, LIFE_TANK.width), randint(0, LIFE_TANK.height)
        self.location = Vector(x, y)
        self.radius = 4
        # 随机速度
        self.velocity = Vector(random() * 2 - 1, random() * 2 - 1).normalize() * 0.2
        self.acceleration = Vector(0, 0)

        # 活跃程度，越大越活跃 0 ~ 1.0
        self.activity = 0.0

    def set_activity(self, activity):
        if isinstance(activity, float):
            self.activity = activity
        else:
            print("""Error: activity must be a float number.""")
            self.activity = 0.0

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
        # 画出球，左上角为原点，宽度和高度
        painter.setPen(Qt.NoPen)
        painter.setBrush(get_color_by_activity(self.activity))
        painter.drawEllipse(
            round(self.location.x - self.radius),
            round(self.location.y - self.radius),
            round(self.radius * 2 + (self.activity * 20)),
            round(self.radius * 2 + (self.activity * 20))
        )
        pass


def get_color_by_activity(activity) -> QColor:
    """
    根据活跃度返回颜色，活跃度越大，颜色越黄，不活跃度越绿
    :param activity: 活跃度
    :return:
    """
    green: QColor = QColor(10, 150, 10)
    yellow: QColor = QColor(255, 255, 0)
    # 线性过渡
    r = (yellow.red() - green.red()) * activity + green.red()
    g = (yellow.green() - green.green()) * activity + green.green()
    b = (yellow.blue() - green.blue()) * activity + green.blue()
    return QColor(round(r), round(g), round(b))