import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel

from computer_info.manager import SYSTEM_INFO_MANAGER

from life.life_manager import LifeManager
from life.gas_manager import GAS_MANAGER
from life.tank import LIFE_TANK

from gui.settings_dialog import SettingsDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口的基本属性
        self.setWindowTitle("赛博小鱼缸")
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
        self.is_window_drag = False
        # 窗口被拖动的位置
        self.m_drag_position = None
        self.life_manager = LifeManager()

        self.settings_button = QPushButton("settings", self)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: #333333; /* 按钮的背景颜色 */
                color: #FFFFFF;            /* 按钮的字体颜色 */
                /*border-radius: 10px;*/       /* 按钮边角的圆滑度 */
                border: 1px solid black;  /* 按钮边框 */
            }
            QPushButton:hover {
                background-color: #555555; /* 鼠标悬浮时按钮的背景颜色 */
            }
        """)
        self.settings_button.setGeometry(self.width() - 100 - 10, 10, 100, 40)
        self.settings_button.clicked.connect(self.showSettingsDialog)
        self.settings_button.hide()  # 默认隐藏设置按钮
        font = QFont()
        font.setPointSize(6)
        self.hover_text_label = QLabel("O₂: 0\nCO₂: 0", self)
        self.hover_text_label.setStyleSheet("color: white;")
        self.hover_text_label.setFont(font)
        self.hover_text_label.setGeometry(10, 10, 150, self.height() - 20)
        self.hover_text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.hover_text_label.hide()
        pass

    def enterEvent(self, event):
        self.settings_button.show()  # 鼠标进入窗口时显示设置按钮
        self.hover_text_label.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.settings_button.hide()  # 鼠标离开窗口时隐藏设置按钮
        self.hover_text_label.hide()
        super().leaveEvent(event)

    def showSettingsDialog(self):
        dialog = SettingsDialog()
        dialog.exec_()  # 显示对话框（为模式对话框，锁住程序直到用户关闭该对话框为止）

    def mousePressEvent(self, event):
        """重写mousePressEvent方法，用于拖动窗口"""
        if event.button() == Qt.LeftButton:
            self.is_window_drag = True
            self.m_drag_position = event.globalPos() - self.pos()
            print(self.m_drag_position)
            event.accept()

    def mouseMoveEvent(self, event):
        """重写mouseMoveEvent方法，用于拖动窗口"""
        if Qt.LeftButton and self.is_window_drag:
            self.move(event.globalPos() - self.m_drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """重写mouseReleaseEvent方法，用于拖动窗口"""
        self.is_window_drag = False

    def paintEvent(self, event):
        """重写paintEvent方法，用于绘制窗口内图像"""
        # 在这里使用 QPainter 进行像素颗粒度的绘制
        painter = QPainter(self)

        # 背景颜色
        painter.fillRect(event.rect(), QColor(20, 20, 20, 200))
        self.life_manager.paint(painter)

    def tick(self):
        """更新窗口内图像"""
        self.life_manager.tick()
        self.hover_text_label.setText(
            f"O₂: {round(GAS_MANAGER.oxygen, 2)}\nCO₂: {round(GAS_MANAGER.carbon_dioxide, 2)}"
        )
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
