from life.fish.state_enum import State
from life.gas_manager import GAS_MANAGER
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
        self.velocity = Vector(0, 0)

        self.time = 0
        self.animation_interval = 10  # 动画间隔（帧），越小越快

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
        self.animate_die_left = QPixmap(f"assert/die.png")  # 目前懒得搞动画，直接用一张死鱼图代替
        self.animate_die_right = QPixmap(f"assert/die.png").transformed(QTransform().scale(-1, 1))

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
        self.energy = 100  # 鱼的能量，鱼死亡时会变为0

        self.state = State.IDLE  # 有待写一个自动决策状态功能
        pass

    def tick(self):
        from life.fish.state import tick_surface, tick_idle, tick_sleep, tick_death
        self.time += 1
        self.update_state()
        # 更新动画
        if self.time % self.animation_interval == 0:
            self.img_index_swim = (self.img_index_swim + 1) % 10

        if self.state == State.IDLE:
            tick_idle(self)
        elif self.state == State.SURFACE:
            tick_surface(self)
        elif self.state == State.SLEEP:
            tick_sleep(self)
        elif self.state == State.DEAD:
            tick_death(self)
        else:
            print(f"tick: 未知的鱼状态 {self.state}")
            raise ValueError(f"未知的鱼状态 {self.state}")

    def update_state(self):
        """
        这里是自然条件下的更新状态，只能强制判定死亡。
        设计鱼的AI行为状态目的切换需要放在其他地方。
        :return:
        """
        if self.energy <= 0:
            self.state = State.DEAD
        # 缺氧
        if GAS_MANAGER.oxygen < self.o2_pre_request:
            self.state = State.DEAD
        # 物质耗尽
        if self.fixed_carbon <= 0:
            self.state = State.DEAD

        return self.state

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
        if self.state == State.DEAD:
            painter.setOpacity(0.8)
        painter.drawPixmap(
            round(self.location.x - self.width / 2),
            round(self.location.y - self.height / 2),
            pixmap
        )
        painter.setOpacity(1)

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
        elif self.state == State.SLEEP:
            if self.is_face_to_left():
                return self.animate_swim_left[self.img_index_swim]
            else:
                return self.animate_swim_right[self.img_index_swim]
        elif self.state == State.DEAD:
            if self.is_face_to_left():
                return self.animate_die_left
            else:
                return self.animate_die_right
        else:
            print(f"select_pixmap: 未知的鱼状态 {self.state}")
            raise ValueError(f"未知的鱼状态 {self.state}")
