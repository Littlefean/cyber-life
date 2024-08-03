"""
类似上帝，指挥控制着缸内所有物体的进展与迭代变化

"""
from typing import List

import psutil

from cyber_life.computer_info.manager import SYSTEM_INFO_MANAGER
from cyber_life.life.ball import LifeBall
from cyber_life.life.bubble_flow import LifeBubbleFlow
from cyber_life.life.fish.guppy_fish import GuppyFish
from cyber_life.life.food import Food
from cyber_life.life.plant import LifePlant
from cyber_life.life.tank import LIFE_TANK
from cyber_life.tools.singleton import SingletonMeta


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
        """
        更新所有的状态

        因为：
        1. 鱼的状态需要在食物更新之后更新——因为食物是否存在及其位置可能改变鱼的状态
        2. 鱼、食物、生物球、水草的状态需要在小鱼缸更新之后更新——因为小鱼缸中水面和沙子的高度会影向它们的位置
        3. 鱼的状态需要在水草更新之后更新——据设计草稿，后期可能添加鱼吃水草的特性

        所以，
        更新顺序：
        1. 小鱼缸
        2. 生物球
        3. 食物
        4. 水草
        5. 鱼
        6. 气泡流
        """
        # 1. 更新小鱼缸
        LIFE_TANK.tick()

        # 2. 更新生物球位置
        for ball, activity in zip(self.balls, SYSTEM_INFO_MANAGER.INSPECTOR_CPU.get_current_result()):  # 使用 zip 并行迭代
            ball.set_activity(activity)
            ball.tick()

        # 3. 更新食物
        for food in self.food_list:
            food.tick()
        self.food_list = list(filter(lambda x: not x.is_deleted, self.food_list))  # 清理食物

        # 4. 更新水草
        self.plant.tick()

        # 5. 更新鱼
        for fish in self.fish_list:
            fish.tick()

        # 6. 更新气泡流
        self.bubble_flow.tick()

    def is_food_in_water(self):
        """
        专门为鱼提供，判断水中是否有食物
        :return:
        """
        return any(food.location.y >= LIFE_TANK.division[0] for food in self.food_list)

    def choice_food_in_water(self):
        """
        专门为鱼提供，随机选择水中食物
        :return:
        """
        return next(food for food in self.food_list if food.location.y >= LIFE_TANK.division[0])

    def add_food(self, x: float):
        self.food_list.append(Food(x))

    def paint(self, painter):
        """
        绘制鱼缸内的所有内容
        """

        # 1. 绘制气泡流
        self.bubble_flow.paint(painter)

        # 2. 绘制生物球
        for ball in self.balls:
            ball.paint(painter)

        # 3. 绘制鱼
        for fish in self.fish_list:
            fish.paint(painter)

        # 4. 绘制生长植物
        self.plant.paint(painter)

        # 5. 绘制食物
        for food in self.food_list:
            food.paint(painter)

        # 6. 绘制小鱼缸
        LIFE_TANK.paint(painter)
