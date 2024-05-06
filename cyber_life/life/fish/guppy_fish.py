from PyQt5.QtCore import QRect, Qt

from cyber_life.life.fish.state_enum import State
from cyber_life.life.food import Food
from cyber_life.life.gas_manager import GAS_MANAGER
from cyber_life.tools.progress_bar import ProgressFloat
from cyber_life.tools.vector import Vector
from PyQt5.QtGui import QPainter, QPixmap, QTransform, QColor, QFont

from cyber_life.life.life_mixin.breathable_mixin import BreathableMixin
from cyber_life.life.tank import LIFE_TANK
from random import randint, uniform
from cyber_life.service.settings import SETTINGS


class GuppyFish(BreathableMixin):
    """
    孔雀鱼
    继承 BreathableMixin 类
    """

    def __init__(self):
        super().__init__()
        # 鱼的位置坐标，其位置是贴图的中心点
        self.location = Vector(
            randint(30, LIFE_TANK.width - 30),
            randint(
                round(LIFE_TANK.water_level_height),
                round(LIFE_TANK.sand_surface_height),
            ),
        )
        self.velocity = Vector(0, 0)

        self.time = 0
        self.animation_interval = 10  # 动画间隔（帧），越小越快

        # 动画序列图
        self.animate_swim_left = [QPixmap(self._get_assert_path(f"fish_{i}.png")) for i in range(10)]

        self.animate_swim_right = [
            QPixmap(self._get_assert_path(f"fish_{i}.png")).transformed(QTransform().scale(-1, 1))
            for i in range(10)
        ]
        self.animate_surface_left = [
            QPixmap(self._get_assert_path(f"fish_{i}.png")).transformed(QTransform().rotate(45))
            for i in range(10)
        ]
        self.animate_surface_right = [
            QPixmap(self._get_assert_path(f"fish_{i}.png")).transformed(
                QTransform().scale(-1, 1).rotate(45)
            )
            for i in range(10)
        ]
        self.animate_die_left = QPixmap(
            self._get_assert_path(f"die.png")
        )  # 目前懒得搞动画，直接用一张死鱼图代替
        self.animate_die_right = QPixmap(self._get_assert_path(f"die.png")).transformed(
            QTransform().scale(-1, 1)
        )

        # 当前游泳状态的动画 帧索引
        self.img_index_swim = 0
        # 大小就是图片的宽高
        self.width = 33
        self.height = 33
        # 移动的目标位置，用于IDLE状态
        self.location_goal: Vector = self.get_random_location()
        # 移动速度
        self.speed = 0.1

        # idea: 可能将呼吸光合作用以组合的方式实现，比继承好一点

        self.fixed_carbon = 1000
        self.o2_pre_request = (
            0.1  # 有待调整，目前鱼的呼吸作用还没有什么意义，因为还没有做进食功能
        )
        self.energy = ProgressFloat(1000, 1000)  # 鱼的能量，鱼死亡时会变为0

        self.energy_pre_cost = 0.1
        self.state = State.FIND_FOOD  # 有待写一个自动决策状态功能
        self.oxygen_inner = ProgressFloat(1000, 1000)
        # 必须要让鱼有一个内部氧气，以保证在水中没有氧气的情况下
        # 能够时不时的切换成水面呼吸模式，呼吸一次，充满内部氧气，然后再进行进食和其他动作

        self.have_food_goal = False
        self.target_food: Food | None = None

        # debug
        self._is_show_debug_info = False
        pass

    @staticmethod
    def _get_assert_path(file_name):
        return f":/{file_name}"

    def breath(self):
        """
        鱼呼吸，这个呼吸在不同的状态下调用会有不同的效果
        :return:
        """
        if self.state == State.DEAD:
            return

        if self.o2_pre_request > self.fixed_carbon:
            # 呼吸不了了，没有足够的碳，或许只能死了
            self.state = State.DEAD
            return
        if self.oxygen_inner < self.o2_pre_request:
            # 体腔内没有足够的氧气
            self.state = State.DEAD
            return
        if self.state == State.SURFACE:
            # 鱼在水面，可以直接呼吸
            self.oxygen_inner += 1  # 这个是在水面呼吸的补充内部氧气速度，暂定在这里
            return

        # 在水中正常呼吸的情况
        carbon_request = self.o2_pre_request
        self.fixed_carbon -= carbon_request
        self.energy += self.o2_pre_request

        # 优先消耗体腔内的氧气，再从外部补充到体腔内
        self.oxygen_inner -= self.o2_pre_request
        if GAS_MANAGER.oxygen > self.o2_pre_request:
            GAS_MANAGER.reduce_oxygen(self.o2_pre_request)
            self.oxygen_inner += self.o2_pre_request

        GAS_MANAGER.add_carbon_dioxide(self.o2_pre_request)
        pass

    def cost_energy(self):
        """
        鱼消耗能量
        :return:
        """
        self.energy -= self.energy_pre_cost

    def tick(self):
        from cyber_life.life.fish.state import (
            tick_surface,
            tick_idle,
            tick_sleep,
            tick_death,
            tick_find_food,
        )
        from cyber_life.life.fish.fake_ai import get_best_state

        self.time += 1
        self.update_state()
        # 更新动画
        if self.time % self.animation_interval == 0:
            self.img_index_swim = (self.img_index_swim + 1) % 10
        self.cost_energy()

        # idea: 应该写一个功能，根据状态来获取对应的函数
        self.state = get_best_state(self)

        if self.state == State.IDLE:
            tick_idle(self)
        elif self.state == State.SURFACE:
            tick_surface(self)
        elif self.state == State.SLEEP:
            tick_sleep(self)
        elif self.state == State.DEAD:
            tick_death(self)
        elif self.state == State.FIND_FOOD:
            tick_find_food(self)
        else:
            print(f"tick: 未知的鱼状态 {self.state}")
            raise ValueError(f"未知的鱼状态 {self.state}")

    def update_state(self):
        """
        这里是自然条件下的更新状态，只能强制判定死亡。
        设计鱼的AI行为状态目的切换需要放在其他地方。
        :return:
        """
        # 能量耗尽
        if self.energy <= 0:
            self.state = State.DEAD
        # 缺氧
        if self.oxygen_inner < self.o2_pre_request:
            self.state = State.DEAD
        # 物质耗尽
        if self.fixed_carbon <= 0:
            self.state = State.DEAD

        return self.state

    @staticmethod
    def get_random_location():
        try:
            x = uniform(30, LIFE_TANK.width - 30)
            y = uniform(
                LIFE_TANK.water_level_height + 30, LIFE_TANK.sand_surface_height - 30
            )
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
            pixmap,
        )
        painter.setOpacity(1)
        if SETTINGS.is_fish_info_visible:
            # 设置字体颜色
            painter.setPen(QColor(255, 255, 255))
            # 设置字体大小和字体类型
            font = QFont('Arial', 5)  # Arial字体，大小为12
            painter.setFont(font)
            rect = QRect(
                round(self.location.x),
                round(self.location.y - 50),
                200,
                100
            )  # 宽度为200，高度为100的矩形区域
            painter.drawText(
                rect,
                Qt.AlignLeft | Qt.TextWordWrap,
                f"E:{self.energy}\nC:{self.fixed_carbon}\nO₂:{self.oxygen_inner}"
            )

    def select_pixmap(self):
        """
        选择当前鱼的动画序列图
        :return:
        """
        if (
                self.state == State.IDLE
                or self.state == State.FIND_FOOD
                or self.state == State.SLEEP
        ):
            if self.is_face_to_left():
                return self.animate_swim_left[self.img_index_swim]
            else:
                return self.animate_swim_right[self.img_index_swim]
        elif self.state == State.SURFACE:
            if self.is_face_to_left():
                return self.animate_surface_left[self.img_index_swim]
            else:
                return self.animate_surface_right[self.img_index_swim]
        elif self.state == State.DEAD:
            if self.is_face_to_left():
                return self.animate_die_left
            else:
                return self.animate_die_right
        else:
            print(f"select_pixmap: 未知的鱼状态 {self.state}")
            raise ValueError(f"未知的鱼状态 {self.state}")
