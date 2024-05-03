import random

from PyQt5.QtGui import QPainter

from life.plant_node import LifePlantNode
from life.tank import LIFE_TANK


class LifePlant:
    def __init__(self):
        """
        表示一束水草
        目前整个鱼缸里只有一个水草，至于后续是否会有多个，还需要考虑
        """

        self.x = random.randint(0, LIFE_TANK.width)
        # 存放水草节点的列表
        self.nodes: list[LifePlantNode] = []
        # 默认产生
        for i in range(2):
            self.grow_node()
        pass

    def grow_node(self):
        """
        产生一个新的水草节点
        """
        if not self.nodes:
            node = LifePlantNode(self.x, LIFE_TANK.sand_surface_height, False)
            self.nodes.append(node)
        else:
            # 获取最后一个节点，并在上面随机位置产生一个子节点
            last_node = self.nodes[-1]
            last_node_location = last_node.location
            node_y = random.randint(
                round(last_node_location.y - 10),
                round(last_node_location.y + 10),
            )
            node_x = random.randint(
                round(last_node_location.x - 10),
                round(last_node_location.x + 10),
            )
            node = LifePlantNode(
                node_x, node_y, True
            )
            last_node.add_child(node)
            self.nodes.append(node)
            pass

    def tick(self):
        """
        实现水草的生长
        """
        for node in self.nodes:
            node.tick()

        # 生长，大约控制在一个小时长一个节点
        # 长时间不关机会长的很茂盛，看上去有点臃肿，寓意提醒用户要注意休息，关机保护电脑
        if random.random() < 1 / (3600 * 20):
            print("grow")
            self.grow_node()

    def paint(self, painter: QPainter):
        for node in self.nodes:
            node.paint(painter)
        pass
