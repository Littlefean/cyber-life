"""
类似上帝，指挥控制着缸内所有物体的进展与迭代变化

"""
from typing import List

import psutil

from computer_info.manager import SYSTEM_INFO_MANAGER
from life.ball import LifeBall
from life.bubble_flow import LifeBubbleFlow
from life.fish.guppy_fish import GuppyFish
from life.food import Food
from life.plant import LifePlant
from life.tank import LIFE_TANK
from tools.singleton import SingletonMeta


class LifeManager(metaclass=SingletonMeta):
    """
    管理小鱼缸的一切内容，包括生物球、小鱼缸、水草、气泡流、鱼等
    """

    def __init__(self):
        self.balls: List[LifeBall] = [LifeBall() for _ in range(psutil.cpu_count())]
        self.plant = LifePlant()
        self.bubble_flow = LifeBubbleFlow(LIFE_TANK.width / 2)
        self.fish_list: List[GuppyFish] = [GuppyFish()]
        self.food_list: List[Food] = []

    def tick(self):
        # 更新鱼
        for fish in self.fish_list:
            fish.tick()
        # 更新生物球位置
        for i, ball in enumerate(self.balls):
            ball.set_activity(SYSTEM_INFO_MANAGER.INSPECTOR_CPU.get_current_result()[i])
            ball.tick()
        # 更新小鱼缸
        LIFE_TANK.tick()
        # 更新水草
        self.plant.tick()
        # 更新气泡流
        self.bubble_flow.tick()
        # 更新食物
        for food in self.food_list:
            food.tick()
        # 清理食物
        self.food_list = [food for food in self.food_list if not food.is_deleted]
        pass

    def is_food_in_water(self):
        """
        专门为鱼提供，判断水中是否有食物
        :return:
        """
        return any(food.location.y >= LIFE_TANK.water_level_height for food in self.food_list)

    def choice_food_in_water(self):
        """
        专门为鱼提供，随机选择水中食物
        :return:
        """
        return next(food for food in self.food_list if food.location.y >= LIFE_TANK.water_level_height)

    def add_food(self, x: float):
        self.food_list.append(Food(x))

    def paint(self, painter):
        # 绘制气泡流
        self.bubble_flow.paint(painter)
        # 绘制生物球
        for ball in self.balls:
            ball.paint(painter)
        # 绘制鱼
        for fish in self.fish_list:
            fish.paint(painter)
        # 绘制生长植物
        self.plant.paint(painter)
        # 绘制食物
        for food in self.food_list:
            food.paint(painter)
        # 绘制小鱼缸
        LIFE_TANK.paint(painter)
