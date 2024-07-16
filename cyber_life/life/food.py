from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from cyber_life.life.tank import LIFE_TANK
from cyber_life.tools.vector import Vector


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
        self.carbon = 400  # 碳量
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

        # 当前是悬浮状态
        if self.float_remaining > 0:

            # 在水面以上，向下落
            if self.location.y < LIFE_TANK.division[0]:
                self.location.y = min(self.location.y + 2, LIFE_TANK.division[0])
            # 在水面以下，向上飘
            elif self.location.y < LIFE_TANK.division[1]:
                self.location.y = max(self.location.y - 0.1, LIFE_TANK.division[0])
            # 被沙子埋了，挤上来
            # 虽然不太可能，但是还是要有的
            else:
                self.location.y = LIFE_TANK.division[1]

            # 目前随机漂移效果还不太好做，先不动了
            # else:
            #     # 恰好在水面上，随机漂移

            #     self.location.x += uniform(-2, 2)
            #     if self.location.x < 0:
            #         self.location.x = 0
            #     elif self.location.x > LIFE_TANK.width:
            #         self.location.x = LIFE_TANK.width

        # 不是悬浮状态，i.e. 开始下沉
        else:

            # 在水面以上，向下落
            if self.location.y < LIFE_TANK.division[0]:
                self.location.y = min(self.location.y + 2, LIFE_TANK.division[0])
            # 正常下沉
            elif self.location.y < LIFE_TANK.division[1]:
                self.location.y = min(self.location.y + 0.1, LIFE_TANK.division[1])
            # 被沙子埋了，挤上来
            else:
                self.location.y = LIFE_TANK.division[1]

            self.carbon -= self.microbe_decompose_speed
