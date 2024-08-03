from random import random

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor

from cyber_life.tools.vector import Vector
from .life_mixin.breathable_mixin import BreathableMixin
from .life_mixin.organism_mixin import OrganismMixin
from .tank import LIFE_TANK


class LifePlantNode(BreathableMixin, OrganismMixin):
    """
    水草节点类，由plant控制
    每个节点都类似 “V” 的样子，一节一节，构成链条状结构
    当前水草生长过高，会超越水面，飘到天空上，后续可能考虑优化
    """

    def __init__(self, x, y, can_move):
        super().__init__()
        self.location = Vector(x, y)
        self.velocity = Vector.random() * 0.1
        self.acceleration = Vector(0, 0)
        # 根节点不能自由移动，其他节点会移动，模拟悬浮效果
        self.next_node = None
        self.can_move = can_move

        # 节点间拉力生效范围半径
        self.pull_radius = 20
        # 节点间排斥力生效范围半径
        self.repel_radius = 5

        self.status_out_range = False
        self.status_in_range = False

        self.radius = 2

        self.o2_pre_request = 0.1
        self.co2_pre_request = 0.1
        self.fixed_carbon = 100  # todo：考虑该固定碳的量能反应在叶子数量和颜色上。

        # 调试用，显示节点的拉力、斥力范围
        self._show_range = False
        self._show_velocity = False

    @classmethod
    def get_root_node(cls):
        """
        获取根节点
        @classmethod：类方法，不需要实例化对象即可调用
        @staticmethod：静态方法，同样不需要实例化即可调用，但不适合写与类成员变量或成员函数有关的功能
        """

        return cls(random() * LIFE_TANK.width, LIFE_TANK.division[1], False)

    def add_child(self, child: 'LifePlantNode'):
        if not self.next_node and isinstance(child, LifePlantNode):
            self.next_node = child
        else:
            raise ValueError("节点只能有一个子节点")

    def tick(self):
        """
        更新节点状态
        首先会将自己的下一个节点拉向自己的位置，然后更新自己的位置和速度
        具体拉的原理就如同引力，但过近会有斥力
        如果在合适范围内，则随机漂浮
        """

        if self.can_move:
            # 遇到墙壁反弹
            # 左右边界检测
            if self.location.x < 0:
                self.velocity.x = abs(self.velocity.x)
            elif self.location.x > LIFE_TANK.width:
                self.velocity.x = -abs(self.velocity.x)
            # 上下边界检测
            # 高出水位线，必须让球掉入水中
            if self.location.y < LIFE_TANK.division[0]:
                self.velocity.y = abs(self.velocity.y)
                # return  # 不能return，否则不能更新下一个节点
            # 低于缸底，必须让球回到缸底
            if self.location.y > LIFE_TANK.division[1]:
                self.velocity.y = -abs(self.velocity.y)
                # return
            # 迭代位置，放在检测边界之后执行，否则检测边界后velocity值的更改会在下一轮引力、斥力生效时覆盖
            self.velocity += self.acceleration
            self.location += self.velocity
            # 限制速度
            self.velocity.limit(10)
        else:
            # 当前节点是根节点，可能要根据动态的surface_height来调整位置
            self.location.y = LIFE_TANK.division[1]

        # 将下一个节点拉向自己
        if not self.next_node:
            return
        # 计算下一个节点与自己之间的距离
        distance = self.location.distance(self.next_node.location)

        # 过远，直接将下一个节点拉过来
        if distance >= self.pull_radius:
            v = (self.location - self.next_node.location).normalize() * 0.1
            self.next_node.velocity = v * 5
            self.next_node.acceleration = Vector(0, 0)

        # 过近，排斥，但是只模拟相邻节点的排斥，不计算与周围其它节点的排斥，是粗糙的模拟
        if distance <= self.repel_radius:
            v = (self.next_node.location - self.location).normalize() * 0.1
            self.next_node.acceleration = Vector(0, 0)
            self.next_node.velocity = v * 5

        # 恰好在拉力和排斥力范围内，开始让自己的下一个节点随机漂移
        if self.repel_radius < distance < self.pull_radius:
            if distance - self.repel_radius < self.pull_radius - distance:
                # 如果距离斥力半径更近，获取斥力方向 单位向量
                self.next_node.acceleration = (self.next_node.location - self.location).normalize()
            else:
                # 如果距离拉力半径更近，获取拉力方向 单位向量
                self.next_node.acceleration = (self.location - self.next_node.location).normalize()
            # 将获取到的单位向量 随机偏转，并赋予到加速度上。
            self.next_node.acceleration = self.next_node.acceleration.rotate(random() * 90) * 0.01

        # 取消掉斥力，通过acceleration增加水草浮力
        self.next_node.acceleration += Vector(0, -0.01)

    def paint(self, painter: QPainter):
        """
        绘制节点
        """

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
        # 绘制引力、斥力范围
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
        painter.setBrush(QColor(69, 79, 56, 220))
        painter.setPen(QColor(69, 79, 56, 220))
        painter.drawEllipse(
            round(self.location.x - self.radius),
            round(self.location.y - self.radius),
            round(self.radius * 2),
            round(self.radius * 2)
        )

        # 绘制与下一个节点之间的连线
        line_pen = QPen(QColor(69, 79, 56, 220))
        line_pen.setWidth(3)
        painter.setPen(line_pen)
        if self.next_node:
            painter.drawLine(
                round(self.location.x),
                round(self.location.y),
                round(self.next_node.location.x),
                round(self.next_node.location.y)
            )
        # 绘制针状线，模拟叶子
        if self.next_node:
            line_pen = QPen(QColor(29, 156, 10, 200))
            line_pen.setWidth(1)
            painter.setPen(line_pen)
            # 张角 和速度有关
            edge = 10 * abs(self.velocity) + 5
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
