from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from life.tank import LIFE_TANK
from tools.vector import Vector


class Food:
    """
    鱼饲料
    鱼饲料必须在水面以上投喂，不能直接在水里出现。
    饲料会在水面上停留一段时间，然后开始下沉。
    当下沉到底部时，含碳量会逐渐减少，直到碳量为0。
    当为0时，饲料就相当于被微生物消耗完了。
    """
    # 微生物的分解速度 单位：碳/帧
    microbe_decompose_speed = 0.01
    radius = 2  # 半径

    def __init__(self, x: float):
        self.location = Vector(x, 0)
        self.float_remaining = 1000  # 饲料下沉倒计时
        self.carbon = 100  # 碳量
        self.is_deleted = False  # 是否被 应该被 删除

    def paint(self, painter: QPainter):
        painter.setPen(Qt.darkYellow)
        painter.setBrush(Qt.yellow)
        painter.drawEllipse(
            round(self.location.x - Food.radius),
            round(self.location.y - Food.radius),
            round(2 * Food.radius),
            round(2 * Food.radius)
        )

    def __repr__(self):
        # 调试用
        return f"Food({self.location.x}, {self.location.y}, {self.carbon})"

    def tick(self):
        self.float_remaining -= 1

        if self.carbon <= 0:
            self.is_deleted = True
            return

        if self.float_remaining > 0:
            # 目前是浮在水面上
            if self.location.y > LIFE_TANK.water_level_height:
                # 浮上来
                self.location.y -= 0.1
            elif self.location.y < LIFE_TANK.sand_surface_height:
                # 在空中，落到水面上
                self.location.y += 2
            # 目前随机漂移效果还不太好做，先不动了
            # else:
            #     # 恰好在水面上，随机漂移

            #     self.location.x += uniform(-2, 2)
            #     if self.location.x < 0:
            #         self.location.x = 0
            #     elif self.location.x > LIFE_TANK.width:
            #         self.location.x = LIFE_TANK.width
        else:
            # 目前是下沉状态
            if self.location.y > LIFE_TANK.sand_surface_height:
                # 被淹了，挤上来
                self.location.y -= 0.5
            else:
                # 下沉
                self.location.y += 0.1
            self.carbon -= self.microbe_decompose_speed
