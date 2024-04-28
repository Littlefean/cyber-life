from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt


class SandWave:
    MAX_RADIUS = 300 / 2

    def __init__(self, x, y, radius, radius_variation):
        self.x = x
        self.y = y
        self.radius = radius
        self.radius_variation: float = radius_variation

    def tick(self):
        self.radius += self.radius_variation

    def is_expired(self):
        return self.radius >= self.MAX_RADIUS or self.radius <= 0

    def paint(self, painter: QPainter):
        alpha_rate = (self.MAX_RADIUS - self.radius) / self.MAX_RADIUS
        line_pen = QPen(QColor(224, 159, 0, round((255 - 50) * alpha_rate)))
        line_pen.setWidth(8)
        painter.setPen(line_pen)
        painter.setBrush(Qt.NoBrush)
        # 应该画一个下半圆

        painter.drawArc(
            round(self.x - self.radius),
            round(self.y - self.radius + 4),  # 下移动4像素，防止弧线边角看起来突出地面
            round(2 * self.radius),
            round(2 * self.radius),
            180 * 16,
            180 * 16,
        )
        pass