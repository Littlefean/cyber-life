"""
类似上帝，指挥控制着缸内所有物体的进展与迭代变化

"""
from typing import List

import psutil

from computer_info.manager import SYSTEM_INFO_MANAGER
from life.ball import LifeBall
from life.bubble_flow import LifeBubbleFlow
from life.fish import LifeFish
from life.plant import LifePlant
from life.tank import LIFE_TANK


class LifeManager:
    def __init__(self):
        self.balls: List[LifeBall] = [LifeBall() for _ in range(psutil.cpu_count())]
        self.plant = LifePlant()
        self.bubble_flow = LifeBubbleFlow(LIFE_TANK.width / 2)
        self.fish_list: List[LifeFish] = [LifeFish()]

        # 假设10px是1cm，300px就是30cm
        # 水中氧气含量
        self.oxygen = 0
        # 水中二氧化碳含量
        self.carbon_dioxide = 0

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
        pass

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
        # 绘制小鱼缸
        LIFE_TANK.paint(painter)
