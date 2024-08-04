from random import randint, uniform

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QPixmap, QTransform, QColor, QFont

from cyber_life.life.fish.state_enum import State
from cyber_life.life.food import Food
from cyber_life.life.gas_manager import GAS_MANAGER
from cyber_life.life.life_mixin.breathable_mixin import BreathableMixin
from cyber_life.life.tank import LIFE_TANK
from cyber_life.service.settings import SETTINGS
from cyber_life.tools.progress_bar import ProgressFloat
from cyber_life.tools.vector import Vector


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
                round(LIFE_TANK.division[0]),
                round(LIFE_TANK.division[1]),
            ),
        )

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

        # 速度，是矢量，有大小有方向
        self.velocity = Vector(0, 0)
        # 移动速率，只有大小
        self.speed = 0.1
        # 移动的目标位置，用于 IDLE 状态
        self.location_goal: Vector = self.get_random_location()

        # 鱼的能量
        self.energy = ProgressFloat(1000, 1000)
        # 鱼的固定碳量
        self.carbon = 1000.
        # 鱼的体内氧气
        self.oxygen = ProgressFloat(1000, 1000)

        # 需要的氧气量
        self.o2_pre_request = 0.1
        # 需要的能量
        self.energy_pre_cost = 0.1

        # 鱼的状态
        self.state = State.IDLE

        # 目标食物
        self.target_food: Food | None = None

    @staticmethod
    def _get_assert_path(file_name):
        return f":/{file_name}"

    def breath(self):
        """
        鱼呼吸
        """

        self.carbon -= self.o2_pre_request
        self.energy += self.o2_pre_request * 0.1
        self.oxygen -= self.o2_pre_request
        # 优先消耗体腔内的氧气，再从外部补充到体腔内
        if GAS_MANAGER.oxygen > self.o2_pre_request:
            GAS_MANAGER.reduce_oxygen(self.o2_pre_request)
            self.oxygen += self.o2_pre_request
        # 呼吸产生二氧化碳
        GAS_MANAGER.add_carbon_dioxide(self.o2_pre_request)

    def cost_energy(self):
        """
        鱼消耗能量
        """

        self.energy -= self.energy_pre_cost

    def tick(self):
        from cyber_life.life.fish.state import (
            tick_death,
            tick_idle,
            tick_surface,
            tick_sleep,
            tick_find_food,
        )
        from cyber_life.life.fish.fake_ai import get_best_state

        self.time += 1

        self.breath()  # 鱼呼吸
        self.cost_energy()  # 鱼消耗能量

        self.die_if_improper()  # 如果面临逆境，则死亡
        self.state = get_best_state(self)  # 根据状态选择最佳行为

        {
            State.DEAD: tick_death,
            State.IDLE: tick_idle,
            State.SURFACE: tick_surface,
            State.SLEEP: tick_sleep,
            State.FIND_FOOD: tick_find_food,
        }[self.state](self)

        # 更新动画
        if self.time % self.animation_interval == 0:  # 每 10 帧更新一次动画
            self.img_index_swim += 1
            self.img_index_swim %= 10  # 动画只有 10 张

    def die_if_improper(self):
        """
        如果面临逆境，则死亡。
        设计鱼的 AI 行为状态目的切换需要放在其他地方。
        """

        # 能量耗尽、缺氧、物质耗尽
        if self.energy < self.energy_pre_cost or self.carbon < self.o2_pre_request or self.oxygen < self.o2_pre_request:
            self.state = State.DEAD

        return self.state

    @staticmethod
    def get_random_location():
        try:
            x = uniform(30, LIFE_TANK.width - 30)
            y = uniform(
                LIFE_TANK.division[0] + 30, LIFE_TANK.division[1] - 30
            )
        except Exception as e:
            print(f"鱼无法找到合适的位置 {e}")
            return
        return Vector(x, y)

    def is_face_to_left(self):
        """
        判断鱼面朝左边
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
            font = QFont('Arial', 6)  # Arial字体，大小为12
            painter.setFont(font)
            rect = QRect(
                round(self.location.x - 20),
                round(self.location.y - 30),
                200,
                100
            )  # 宽度为200，高度为100的矩形区域
            painter.drawText(
                rect,
                Qt.AlignLeft | Qt.TextWordWrap,
                f"E:{self.energy}\nC:{round(self.carbon, 1)}\nO₂:{self.oxygen}\nS:{self.state.name}"
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
