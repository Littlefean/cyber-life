from random import random
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from vector import Vector

from life_tank import LIFE_TANK


class LifePlantNode:
    """水草节点类"""

    def __init__(self, x, y, can_move):
        self.location = Vector(x, y)
        self.velocity = Vector.random() * 0.1
        self.acceleration = Vector(0, 0)
        # 根节点不能自由移动，其他节点会移动，模拟悬浮效果
        self.next_node = None
        self.can_move = can_move

        # 节点间拉力生效范围半径
        self.pull_radius = 20
        # 节点间排斥力生效范围半径
        self.repel_radius = 10

        self.status_out_range = False
        self.status_in_range = False

        self.radius = 2
        self._show_range = False
        self._show_velocity = False

    @classmethod
    def get_root_node(cls):
        """获取根节点"""
        return cls(random() * LIFE_TANK.width, LIFE_TANK.height, False)

    def add_child(self, child):
        if not self.next_node and isinstance(child, LifePlantNode):
            self.next_node = child
        else:
            raise ValueError("节点只能有一个子节点")

    def tick(self):
        """
        更新节点状态
        首先会将自己的下一个节点拉向自己的位置，然后更新自己的位置和速度
        具体拉的原理就如同引力，但过近会有斥力
        :return:
        """
        if self.can_move:
            # 迭代位置
            self.velocity += self.acceleration
            self.location += self.velocity
            # 限制速度
            self.velocity.limit(10)

            # 遇到墙壁反弹
            # 左右边界检测
            if self.location.x < 0:
                self.velocity.x = abs(self.velocity.x)
            elif self.location.x > LIFE_TANK.width:
                self.velocity.x = -abs(self.velocity.x)
            # 上下边界检测
            # 高出水位线，必须让球掉入水中
            if self.location.y < LIFE_TANK.water_level_height:
                self.velocity.y = abs(self.velocity.y)
                return
            # 低于缸底，必须让球回到缸底
            if self.location.y > LIFE_TANK.height:
                self.velocity.y = -abs(self.velocity.y)
                return

        # 将下一个节点拉向自己
        if not self.next_node:
            return
        # 计算下一个节点与自己之间的距离
        distance = self.location.distance(self.next_node.location)

        if distance >= self.pull_radius:
            # 计算拉力
            force = (self.location - self.next_node.location).normalize() * 0.1
            self.next_node.velocity = force * 5
            self.next_node.acceleration = Vector(0, 0)
        if distance <= self.repel_radius:
            # 计算排斥力
            force = (self.next_node.location - self.location).normalize() * 0.1
            self.next_node.acceleration = Vector(0, 0)
            self.next_node.velocity = force * 5
        if self.repel_radius < distance < self.pull_radius:
            # 如果距离拉力边缘更近
            if distance - self.repel_radius < self.pull_radius - distance:
                # 排斥优先
                self.next_node.acceleration = (self.next_node.location - self.location).normalize()
            else:
                # 拉力优先
                self.next_node.acceleration = (self.location - self.next_node.location).normalize()
            # 随机偏转
            self.next_node.acceleration = self.next_node.acceleration.rotate(random() * 90) * 0.01

    def paint(self, painter: QPainter):
        """绘制节点"""
        # 绘制速度矢量
        if self._show_velocity:
            painter.setBrush(Qt.NoBrush)
            velocity_pen = QPen(Qt.blue)
            velocity_pen.setWidth(4)
            painter.setPen(velocity_pen)

            painter.drawLine(
                round(self.location.x),
                round(self.location.y),
                round(self.location.x + self.velocity.x * 50),
                round(self.location.y + self.velocity.y * 50)
            )
        # 绘制引力斥力范围
        if self._show_range:
            painter.setBrush(Qt.NoBrush)
            painter.setPen(Qt.red)
            painter.drawEllipse(
                round(self.location.x - self.pull_radius),
                round(self.location.y - self.pull_radius),
                round(self.pull_radius * 2),
                round(self.pull_radius * 2)
            )
            painter.drawEllipse(
                round(self.location.x - self.repel_radius),
                round(self.location.y - self.repel_radius),
                round(self.repel_radius * 2),
                round(self.repel_radius * 2)
            )
        # 绘制节点
        painter.setBrush(Qt.darkGreen)
        painter.setPen(Qt.darkGreen)
        painter.drawEllipse(
            round(self.location.x - self.radius),
            round(self.location.y - self.radius),
            round(self.radius * 2),
            round(self.radius * 2)
        )

        # 绘制与下一个节点之间的连线
        line_pen = QPen(Qt.darkGreen)
        line_pen.setWidth(3)
        painter.setPen(line_pen)
        if self.next_node:
            painter.drawLine(
                round(self.location.x),
                round(self.location.y),
                round(self.next_node.location.x),
                round(self.next_node.location.y)
            )
        # 绘制叶子
        if self.next_node:
            line_pen = QPen(Qt.darkGreen)
            line_pen.setWidth(1)
            painter.setPen(line_pen)
            # 张角 和速度有关
            edge = 10 * abs(self.velocity)
            length = 20
            for i in range(-5, 5 + 1):
                if i == 0:
                    continue
                line_vector = (self.next_node.location - self.location).normalize().rotate(i * edge) * length
                painter.drawLine(
                    round(self.location.x),
                    round(self.location.y),
                    round(self.location.x + line_vector.x),
                    round(self.location.y + line_vector.y)
                )

    pass
