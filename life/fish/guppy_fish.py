from life.fish.state_enum import State
from tools.vector import Vector
from PyQt5.QtGui import QPainter, QPixmap, QTransform

from life.life_mixin.breathable_mixin import BreathableMixin
from life.tank import LIFE_TANK
from random import randint, uniform
from service.settings import SETTINGS


class GuppyFish(BreathableMixin):
    """
    孔雀鱼
    """

    def __init__(self):
        super().__init__()
        # 鱼的位置坐标，其位置是贴图的中心点
        self.location = Vector(
            randint(30, LIFE_TANK.width - 30),
            randint(
                round(LIFE_TANK.water_level_height),
                round(LIFE_TANK.sand_surface_height)
            )
        )

        self.time = 0

        # 动画序列图
        self.animate_swim_left = [QPixmap(f"assert/fish_{i}.png") for i in range(10)]

        self.animate_swim_right = [
            QPixmap(f"assert/fish_{i}.png").transformed(QTransform().scale(-1, 1)) for i in range(10)
        ]
        self.animate_surface_left = [
            QPixmap(f"assert/fish_{i}.png").transformed(QTransform().rotate(45)) for i in range(10)
        ]
        self.animate_surface_right = [
            QPixmap(f"assert/fish_{i}.png").transformed(QTransform().scale(-1, 1).rotate(45)) for i in range(10)
        ]

        # 当前游泳状态的动画 帧索引
        self.img_index_swim = 0
        # 大小就是图片的宽高
        self.width = 33
        self.height = 33
        # 移动的目标位置
        self.location_goal: Vector = self.get_random_location()
        # 移动速度
        self.speed = 0.1

        self.fixed_carbon = 100_0000
        self.o2_pre_request = 0.1  # 有待调整，目前鱼的呼吸作用还没有什么意义，因为还没有做进食功能

        self.state = State.SURFACE  # 有待写一个自动决策状态功能
        pass

    def tick(self):
        from life.fish.state import tick_surface, tick_idle
        self.time += 1
        # 更新动画
        if self.time % 10 == 0:
            self.img_index_swim = (self.img_index_swim + 1) % 10

        if self.state == State.IDLE:
            tick_idle(self)
        elif self.state == State.SURFACE:
            tick_surface(self)
        else:
            raise ValueError(f"未知的鱼状态 {self.state}")

    @staticmethod
    def get_random_location():
        try:
            x = uniform(30, LIFE_TANK.width - 30)
            y = uniform(LIFE_TANK.water_level_height + 30, LIFE_TANK.sand_surface_height - 30)
        except Exception as e:
            print(f"鱼无法找到合适的位置 {e}")
            return None
        return Vector(x, y)

    def is_face_to_left(self):
        """
        判断鱼面朝左边
        :return: bool
        """
        speed_vector = self.location_goal - self.location
        return speed_vector.x < 0

    def paint(self, painter: QPainter):
        if not SETTINGS.is_fish_visible:
            return
        # 判断鱼是否面向左边
        pixmap = self.select_pixmap()
        painter.drawPixmap(
            round(self.location.x - self.width / 2),
            round(self.location.y - self.height / 2),
            pixmap
        )

    def select_pixmap(self):
        """
        选择当前鱼的动画序列图
        :return:
        """
        if self.state == State.IDLE:
            if self.is_face_to_left():
                return self.animate_swim_left[self.img_index_swim]
            else:
                return self.animate_swim_right[self.img_index_swim]
        elif self.state == State.SURFACE:
            if self.is_face_to_left():
                return self.animate_surface_left[self.img_index_swim]
            else:
                return self.animate_surface_right[self.img_index_swim]
        else:
            raise ValueError(f"未知的鱼状态 {self.state}")
