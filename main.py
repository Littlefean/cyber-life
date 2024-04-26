import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget
import psutil

from computer_info.manager import SYSTEM_INFO_MANAGER

from life.ball import LifeBall
from life.plant import LifePlant
from life.tank import LIFE_TANK
from life.bubble_flow import LifeBubbleFlow
from life.fish import LifeFish


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口的基本属性
        self.setWindowTitle("赛博生态缸")
        # 将背景设置为透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            # 无边框
            Qt.FramelessWindowHint |
            # 始终置顶
            Qt.WindowStaysOnTopHint
        )
        # 设置icon
        self.setWindowIcon(QIcon('assert/icon.ico'))
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
        self.m_drag_position = None
        # 有待集成在一个 life_manager 单例中
        self.life_data = {
            "balls": [LifeBall() for _ in range(psutil.cpu_count())],
            "plants": [LifePlant()],
            "bubble_flows": [LifeBubbleFlow(LIFE_TANK.width / 2)],
            "fish": [LifeFish()]
        }
        pass

    def mousePressEvent(self, event):
        """重写mousePressEvent方法，用于拖动窗口"""
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_drag_position = event.globalPos() - self.pos()
            print(self.m_drag_position)
            event.accept()

    def mouseMoveEvent(self, event):
        """重写mouseMoveEvent方法，用于拖动窗口"""
        if Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_drag_position)
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
        for plant in self.life_data["plants"]:
            plant.paint(painter)
            pass
        # 绘制生态缸
        LIFE_TANK.paint(painter)

    def tick(self):
        """更新窗口内图像"""
        # 更新鱼
        for fish in self.life_data["fish"]:
            fish.tick()
        # 更新生物球位置
        for i, ball in enumerate(self.life_data["balls"]):
            ball.set_activity(SYSTEM_INFO_MANAGER.INSPECTOR_CPU.get_current_result()[i])
            ball.tick()
        # 更新生态缸
        LIFE_TANK.tick()
        # 更新水草
        for plant in self.life_data["plants"]:
            plant.tick()
        # 更新气泡流
        for bubble_flow in self.life_data["bubble_flows"]:
            bubble_flow.tick()
        self.update()


def main():
    # 启动系统信息管理器
    SYSTEM_INFO_MANAGER.start()

    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    # interval 设置为 10 表示每 10ms 刷新一次窗口
    timer = QTimer(interval=10, timeout=main_window.tick)  # FPS
    timer.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
