import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCloseEvent, QKeyEvent
from PyQt5.QtWidgets import QDialog, QCheckBox, QSlider, QPushButton, QLabel, QWidget

from cyber_life.gui.about_dialog import AboutDialog
from cyber_life.service.settings import SETTINGS

lg = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    WINDOW_SIZE = (400, 320)

    def __init__(self, master: QWidget):
        lg.debug('SettingsDialog 初始化')

        super().__init__()

        self.master = master

        self.setWindowTitle("设置")
        self.setGeometry(400, 400, *self.WINDOW_SIZE)
        # 设置窗口大小不可变
        self.setFixedSize(*self.WINDOW_SIZE)
        # 设置icon
        self.setWindowIcon(QIcon(":/icon.ico"))

        # 显示小鱼
        self.check_box_fish = QCheckBox("显示小鱼", self)
        self.check_box_fish.move(10, 10)  # 放置在窗口里
        self.check_box_fish.setChecked(SETTINGS.is_fish_visible)  # 初始状态
        self.check_box_fish.setToolTip("不显示鱼≠没有鱼，资源正常消耗")  # 提示信息
        self.check_box_fish.stateChanged.connect(self.change_display_fish)  # 状态改变时的槽函数
        # 显示小鱼信息
        self.check_box_fish_info = QCheckBox("显示小鱼信息", self)
        self.check_box_fish_info.move(200, 10)
        self.check_box_fish_info.setChecked(SETTINGS.is_fish_info_visible)
        self.check_box_fish_info.setEnabled(SETTINGS.is_fish_visible)
        self.check_box_fish_info.stateChanged.connect(self.change_display_fish_info)

        # 自定义交换内存高度
        self.check_box_memory = QCheckBox("自定义交换内存高度", self)
        self.check_box_memory.move(10, 40)
        self.check_box_memory.setChecked(SETTINGS.is_swap_memory_fixed)
        self.check_box_memory.stateChanged.connect(self.change_custom_memory)
        # 一个滑动条组件，从 0 到 99，可以设置交换内存的高度比例
        self.slider_memory = QSlider(Qt.Horizontal, self)
        self.slider_memory.setGeometry(10, 70, 380, 30)
        self.slider_memory.setMinimum(0)
        self.slider_memory.setMaximum(99)  # 最大值不要调100，顶部剩余距离为0导致程序崩溃
        self.slider_memory.setValue(int(SETTINGS.swap_memory_height_rate * 100))
        self.slider_memory.setEnabled(SETTINGS.is_swap_memory_fixed)
        self.slider_memory.valueChanged.connect(self.change_custom_memory_height)

        # 投喂食物概率
        self.label_feed = QLabel("投喂食物概率：", self)
        self.label_feed.move(10, 120)
        # 一个滑动调组件，从0到100，设置投喂食物的概率
        self.slider_feed = QSlider(Qt.Horizontal, self)
        self.slider_feed.setGeometry(10, 150, 380, 30)
        self.slider_feed.setMinimum(0)
        self.slider_feed.setMaximum(100)
        self.slider_feed.setValue(int(SETTINGS.put_food_rate * 100))
        self.slider_feed.valueChanged.connect(self.change_feed_probability)

        # 窗口不透明度
        self.label_opacity = QLabel("窗口不透明度：", self)
        self.label_opacity.move(10, 200)
        # 一个滑动调组件，从 1 到 100，设置窗口的不透明度
        self.slider_opacity = QSlider(Qt.Horizontal, self)
        self.slider_opacity.setGeometry(10, 230, 380, 30)
        self.slider_opacity.setMinimum(1)
        self.slider_opacity.setMaximum(100)
        self.slider_opacity.setValue(int(SETTINGS.window_opacity * 100))
        self.slider_opacity.valueChanged.connect(self.change_window_opacity)

        # 底部右下角的关于按钮
        self.button_about = QPushButton("关于", self)
        self.button_about.move(10, 280)
        self.button_about.clicked.connect(self.show_about)

        # 同 main.py 里 MainWindow.__init__() 里对 dialog 的处理，不再赘述
        self.msg_box = AboutDialog()

    def __del__(self):
        lg.debug('SettingsDialog 析构')

    def show_about(self):
        # 弹出关于信息框
        # 同 main.py 里 MainWindow.showSettingsDialog() 里对 dialog 的处理，不再赘述
        self.msg_box.exec_()

    @staticmethod
    def save_settings():
        SETTINGS.save_to_json()

        # 弹出保存成功的消息框
        # msg_box = QMessageBox()
        # msg_box.setWindowTitle("保存成功")
        # msg_box.setWindowIcon(QIcon(":/icon.ico"))
        # msg_box.setText("设置已成功保存。")
        # msg_box.setIcon(QMessageBox.Information)
        # msg_box.setStandardButtons(QMessageBox.Ok)
        # msg_box.exec_()

    def change_display_fish(self, state):
        """
        改变是否显示小鱼
        """

        is_button_checked = state == Qt.Checked

        SETTINGS.is_fish_visible = is_button_checked
        self.check_box_fish_info.setEnabled(is_button_checked)  # 显示小鱼时，显示小鱼信息也可用

        self.save_settings()

    def change_display_fish_info(self, state):
        """
        改变是否显示小鱼 *信息*
        """

        is_button_checked = state == Qt.Checked

        SETTINGS.is_fish_info_visible = is_button_checked

        self.save_settings()

    def change_custom_memory(self, state):
        """
        改变是否自定义交换内存
        """

        is_button_checked = state == Qt.Checked

        SETTINGS.is_swap_memory_fixed = is_button_checked
        self.slider_memory.setEnabled(is_button_checked)  # 自定义交换内存高度时，滑动条可用

        self.save_settings()

    def change_custom_memory_height(self, value):
        """
        改变交换内存的高度比例
        """

        SETTINGS.swap_memory_height_rate = (
                value / 100
        )  # 写入SETTINGS，在LIFE_TANK中判断，如果不将交换内存固定，则生效

        self.save_settings()

    def change_feed_probability(self, value: int):
        """
        改变投喂食物的概率
        """

        SETTINGS.put_food_rate = value / 100

        self.save_settings()

    def change_window_opacity(self, value: int):
        """
        改变窗口的不透明度
        """

        SETTINGS.window_opacity = value / 100
        self.master.setWindowOpacity(SETTINGS.window_opacity)

        self.save_settings()

    def closeEvent(self, event: QCloseEvent):
        """
        重写closeEvent方法
        """

        # 在不知明原因下，通知栏在关闭 settings 窗口时会连带着所有一起关闭，
        # 所以重新写一个关闭事件，隐藏窗口，并忽略关闭事件。

        # 这里其实挺玄乎的，明明无论用sys.exit()/sys.exit(self)/sys.exit(QDialog)/super().closeEvent(event)都直接关闭所有窗口,有待深入研究。

        self.hide()
        event.ignore()

    def keyPressEvent(self, event: QKeyEvent):
        """
        重写keyPressEvent方法，实现 ESC 键关闭设置窗口，而不是关闭程序
        """

        # 按下 ESC 键关闭设置窗口
        if event.key() == Qt.Key_Escape:
            self.close()
        # 其他按键传递给父类处理（似乎没啥用）
        else:
            super().keyPressEvent(event)
