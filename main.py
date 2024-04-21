import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
import random
import psutil

from vector import Vector
from computer_info import COMPUTER_INFO, get_memory_usage_percent, update_computer_info, update_computer_info_timer

from life_ball import LifeBall
from life_plant_node import LifePlantNode
from life_tank import LIFE_TANK
from life_bubble_flow import LifeBubbleFlow
from life_fish import LifeFish


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口的基本属性
        self.setWindowTitle("赛博像素生态缸")
        # 将背景设置为透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            # 无边框
            Qt.FramelessWindowHint |
            # 始终置顶
            Qt.WindowStaysOnTopHint
        )
        # 设置icon
        self.setWindowIcon(QIcon('icon.ico'))
        # 设置大小
        self.resize(300, LIFE_TANK.height + 1)

        # 设置窗口大小和位置
        self.setGeometry(10, 10, 300, LIFE_TANK.height + 1)
        self.move(
            QApplication.desktop().screenGeometry().width() - self.width() - 100,
            QApplication.desktop().screenGeometry().height() - self.height() - 200
        )

        # 窗口是否被拖动
        self.m_drag = False
        # 窗口被拖动的位置
        self.m_DragPosition = None
        self.life_data = {
            "balls": [LifeBall() for _ in range(psutil.cpu_count())],
            "plants": [LifePlantNode.get_root_node()],
            "bubble_flows": [LifeBubbleFlow(LIFE_TANK.width / 2)],
            "fish": [LifeFish()]
        }
        # 生长植物节点
        for plant_root in self.life_data["plants"]:
            current_node = plant_root
            for i in range(3):
                current_node.add_child(
                    LifePlantNode(
                        random.randint(0, LIFE_TANK.width - 1),
                        random.randint(0, LIFE_TANK.height - 1),
                        True,
                    )
                )
                current_node = current_node.next_node
        pass

    def mousePressEvent(self, event):
        """重写mousePressEvent方法，用于拖动窗口"""
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            print(self.m_DragPosition)
            event.accept()

    def mouseMoveEvent(self, event):
        """重写mouseMoveEvent方法，用于拖动窗口"""
        if Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        """重写mouseReleaseEvent方法，用于拖动窗口"""
        self.m_drag = False

    def paintEvent(self, event):
        """重写paintEvent方法，用于绘制窗口内图像"""
        # 在这里使用 QPainter 进行像素颗粒度的绘制
        painter = QPainter(self)
        # 背景颜色
        painter.fillRect(event.rect(), QColor(20, 20, 20, 200))

        # 绘制气泡流
        for bubble_flow in self.life_data["bubble_flows"]:
            bubble_flow.paint(painter)
        # 绘制生物球
        for ball in self.life_data["balls"]:
            ball.paint(painter)
        # 绘制鱼
        for fish in self.life_data["fish"]:
            fish.paint(painter)
        # 绘制生长植物
        for plant_root_node in self.life_data["plants"]:
            current_node = plant_root_node
            while current_node is not None:
                current_node.paint(painter)
                current_node = current_node.next_node
        # 绘制生态缸
        LIFE_TANK.paint(painter)

    def tick(self):
        """更新窗口内图像"""
        # 更新鱼
        for fish in self.life_data["fish"]:
            fish.tick()
        # 更新生物球位置
        for i, ball in enumerate(self.life_data["balls"]):
            ball.set_activity(COMPUTER_INFO["cpu"][i])
            ball.tick()
        # 更新生态缸
        LIFE_TANK.tick()
        # 更新水草
        for plant_root_node in self.life_data["plants"]:
            current_node = plant_root_node
            while current_node is not None:
                current_node.tick()
                current_node = current_node.next_node
        # 更新气泡流
        for bubble_flow in self.life_data["bubble_flows"]:
            bubble_flow.tick()
        self.update()


def main():
    from threading import Thread
    Thread(target=update_computer_info_timer, daemon=True).start()

    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    # interval 设置为 10 表示每 10ms 刷新一次窗口
    timer = QTimer(interval=10, timeout=main_window.tick)  # FPS
    timer.start()

    # QTimer(interval=10, timeout=update_computer_info).start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
