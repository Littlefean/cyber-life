"""
赛博小鱼缸
"""
import logging
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSystemTrayIcon, qApp, QMenu

# 引入assets文件夹中的资源文件
# 需要进入assets文件夹后在命令行输入指令 `pyrcc5 image.rcc -o assets.py` 来更新assets.py文件
from assets import assets
from cyber_life.computer_hook.manager import SYSTEM_HOOK_MANAGER
from cyber_life.computer_info.manager import SYSTEM_INFO_MANAGER
from cyber_life.gui.settings_dialog import SettingsDialog
from cyber_life.life.gas_manager import GAS_MANAGER
from cyber_life.life.life_manager import LifeManager
from cyber_life.life.tank import LIFE_TANK
from cyber_life.service.settings import SETTINGS
from cyber_life.static import TANK_SCREEN_WIDTH, LOG_FORMAT

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
lg = logging.getLogger(__name__)


class MainWindow(QWidget):
    INTERVAL = 10  # 刷新间隔（ms）

    def __init__(self):
        lg.debug('MainWindow 初始化')

        super().__init__()

        # 设置窗口的基本属性
        self.setWindowTitle("赛博小鱼缸")
        # 将背景设置为透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.FramelessWindowHint  # 无边框
            | Qt.WindowStaysOnTopHint  # 始终置顶
            | Qt.SplashScreen  # 只显示在通知栏
        )
        self.setWindowOpacity(SETTINGS.window_opacity)
        self.setCursor(Qt.OpenHandCursor)  # 鼠标指针改为手型
        # 设置icon
        self.setWindowIcon(QIcon(":/icon.ico"))
        # 设置大小
        self.resize(TANK_SCREEN_WIDTH, LIFE_TANK.height + 1)
        # 创建系统托盘（通知栏）图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(":/icon.ico"))
        self.tray_icon.setToolTip('赛博小鱼缸')
        self.tray_icon.show()

        # 创建托盘图标的上下文菜单
        self.menu = QMenu()
        self.show_action = self.menu.addAction("显示")
        self.hide_action = self.menu.addAction("隐藏")
        self.settings_action = self.menu.addAction("设置")
        self.exit_action = self.menu.addAction("退出")
        self.tray_icon.setContextMenu(self.menu)

        # 连接托盘图标的信号
        self.show_action.triggered.connect(self.showNormal)
        self.hide_action.triggered.connect(self.hide)
        self.settings_action.triggered.connect(self.showSettingsDialog)
        self.exit_action.triggered.connect(qApp.quit)

        # 设置窗口大小和位置
        self.setGeometry(10, 10, TANK_SCREEN_WIDTH, LIFE_TANK.height + 1)
        self.move(
            QApplication.desktop().screenGeometry().width() - self.width() - 100,
            QApplication.desktop().screenGeometry().height() - self.height() - 200,
        )

        # 窗口是否被拖动
        self.is_window_drag = False
        # 窗口被拖动的位置
        self.m_drag_position = None
        self.life_manager = LifeManager()

        # 悬浮提示文字
        font = QFont()
        font.setPointSize(7)
        self.hover_text_label = QLabel("...", self)
        self.hover_text_label.setStyleSheet("color: white;")
        self.hover_text_label.setFont(font)
        self.hover_text_label.setGeometry(10, 10, 150, self.height() - 20)
        self.hover_text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.hover_text_label.hide()

        # 创建设置对话框
        # 只创建一个实例，用的时候 exec_()，用完就 hide()
        # 而不是 destroy() 销毁，每次都创建新的实例并不好
        self.dialog = SettingsDialog(self)
        # 绑定到 self 上另一个目的：防止引用计数减为 0 而触发 GC 回收

    def __del__(self):
        lg.debug('MainWindow 析构')

    def enterEvent(self, event):
        """
        鼠标进入窗口
        """

        self.hover_text_label.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """
        鼠标离开窗口
        """

        self.hover_text_label.hide()
        super().leaveEvent(event)

    def showSettingsDialog(self):
        """
        显示设置对话框
        """

        # 已经做了相关处理，调用 exec_() 方法即可，不会卡住
        # 同时，exec_() 方法防止在设置界面中用户与 MainWindow 交互，更符合正常软件操作逻辑
        self.dialog.exec_()

    def mousePressEvent(self, event):
        """
        鼠标按下
        用于拖动窗口
        """

        if event.button() == Qt.LeftButton:
            self.is_window_drag = True
            self.m_drag_position = event.globalPos() - self.pos()
            self.setCursor(Qt.ClosedHandCursor)

        event.accept()

    def mouseMoveEvent(self, event):
        """
        鼠标移动
        用于拖动窗口
        """

        if Qt.LeftButton and self.is_window_drag:
            self.move(event.globalPos() - self.m_drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """
        鼠标释放
        用于拖动窗口
        """

        self.is_window_drag = False
        self.setCursor(Qt.OpenHandCursor)

    def tick(self):
        """
        更新窗口内图像
        """

        self.life_manager.tick()

        o2 = round(GAS_MANAGER.oxygen, 2)
        co2 = round(GAS_MANAGER.carbon_dioxide, 2)
        brightness = round(SYSTEM_INFO_MANAGER.INSPECTOR_SCREEN.get_current_result(), 2)
        self.hover_text_label.setText(f"O₂: {o2}\nCO₂: {co2}\nbright: {brightness}")

        self.update()  # 会调用 paintEvent

    def paintEvent(self, event):
        """
        重写paintEvent方法，用于绘制窗口内图像
        """

        # 在这里使用 QPainter 进行像素颗粒度的绘制
        painter = QPainter(self)

        # 背景颜色
        painter.fillRect(event.rect(), QColor(20, 20, 20, 255))
        self.life_manager.paint(painter)

    def closeEvent(self, event):
        """重写closeEvent方法，用于关闭窗口时释放资源"""
        SYSTEM_INFO_MANAGER.stop()
        SYSTEM_HOOK_MANAGER.stop()
        assets.qCleanupResources()  # 释放图像资源
        super().closeEvent(event)


def main():
    lg.info('赛博小鱼缸启动')

    try:
        # 启动系统信息管理器
        SYSTEM_INFO_MANAGER.start()
        lg.info('INFO_MANAGER 启动成功')
        # 启动钩子管理器
        SYSTEM_HOOK_MANAGER.start()
        lg.info('HOOK_MANAGER 启动成功')

        app = QApplication(sys.argv)

        main_window = MainWindow()
        main_window.show()

        # interval 设置为 10 表示每 10ms 刷新一次窗口
        timer = QTimer(interval=main_window.INTERVAL, timeout=main_window.tick)  # FPS
        timer.start()

        sys.exit(app.exec_())

    except Exception as e:
        # 实际上可能很难捕获到异常，Qt有点奇怪，有待深入研究
        lg.fatal(f'主程序异常: {e}')


if __name__ == "__main__":
    main()
