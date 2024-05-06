from typing import List

from .bubble import LifeBubble
from PyQt5.QtGui import QPainter
from cyber_life.computer_info.manager import SYSTEM_INFO_MANAGER


class LifeBubbleFlow:
    """
    气泡流类，由life_manager控制
    控制气泡生成和消失
    对气泡状态进行更新
    """

    def __init__(self, x):
        self.x = x
        self.bubbles: List[LifeBubble] = []
        self.time = 0

    @property
    def bubble_interval(self):
        """
        每隔多少帧生成一个新的气泡
        根据当前上传的网速来决定
        :return:
        """
        sent_speed = SYSTEM_INFO_MANAGER.INSPECTOR_NETWORK.get_current_result().sent_speed
        if sent_speed < 1:
            return 999999
        if sent_speed < 1000:
            return 100
        if sent_speed < 1_0000:
            return 50
        if sent_speed < 10_0000:
            return 20
        if sent_speed < 20_0000:
            return 10
        if sent_speed < 50_0000:
            return 5
        return 1

    def tick(self):
        """
        时间流逝
        """
        # 每隔一段时间，生成一个新的气泡
        if self.time % self.bubble_interval == 0:
            self.bubbles.append(LifeBubble(self.x))
        for bubble in self.bubbles:
            bubble.tick()
        # 移除消亡的气泡
        self.bubbles = [bubble for bubble in self.bubbles if bubble.is_alive]

        self.time += 1

    def paint(self, painter: QPainter):
        """
        绘制
        """
        for bubble in self.bubbles:
            bubble.paint(painter)
