from PyQt5.QtWidgets import QDialog, QCheckBox, QSlider, QPushButton, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from cyber_life.service.settings import SETTINGS


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设置")
        self.setGeometry(400, 400, 400, 400)
        # 设置icon
        self.setWindowIcon(QIcon(":/icon.ico"))
        # 小鱼
        self.check_box_fish = QCheckBox("显示小鱼", self)
        self.check_box_fish.move(10, 10)
        self.check_box_fish.setChecked(SETTINGS.is_fish_visible)
        self.check_box_fish.stateChanged.connect(self.change_settings_display_fish)
        # 内存
        self.check_box_memory = QCheckBox("自定义交换内存高度", self)
        self.check_box_memory.move(10, 40)
        self.check_box_memory.setChecked(SETTINGS.is_swap_memory_fixed)
        self.check_box_memory.stateChanged.connect(self.change_settings_display_memory)
        # 一个滑动条组件，从0到100，可以设置交换内存的高度比例
        self.slider_memory = QSlider(Qt.Horizontal, self)
        self.slider_memory.setGeometry(10, 70, 380, 30)
        self.slider_memory.setMinimum(0)
        self.slider_memory.setMaximum(
            99
        )  # 最大值不要调100，顶部剩余距离为0导致程序崩溃
        self.slider_memory.setValue(int(SETTINGS.swap_memory_height_rate * 100))
        self.slider_memory.valueChanged.connect(self.change_memory_height)

        self.put_food_rate_label = QLabel("投喂食物概率：", self)
        self.put_food_rate_label.move(10, 120)

        # 一个滑动调组件，从0到100，设置投喂食物的概率
        self.slider_feed = QSlider(Qt.Horizontal, self)
        self.slider_feed.setGeometry(10, 150, 380, 30)
        self.slider_feed.setMinimum(0)
        self.slider_feed.setMaximum(100)
        self.slider_feed.setValue(int(SETTINGS.put_food_rate * 100))
        self.slider_feed.valueChanged.connect(self.change_feed_rate)

        # 显示小鱼信息
        self.check_box_fish = QCheckBox("显示小鱼信息", self)
        self.check_box_fish.move(10, 180)
        self.check_box_fish.setChecked(SETTINGS.is_fish_info_visible)
        self.check_box_fish.stateChanged.connect(self.change_settings_display_fish_info)

        # 底部的保存设置按钮
        self.button_save = QPushButton("保存设置", self)
        self.button_save.move(10, 400 - 50)
        self.button_save.clicked.connect(self.save_settings)

    @staticmethod
    def save_settings():
        SETTINGS.save_to_json()

        # 弹出保存成功的消息框
        msg_box = QMessageBox()
        msg_box.setWindowTitle("保存成功")
        msg_box.setWindowIcon(QIcon(":/icon.ico"))
        msg_box.setText("设置已成功保存。")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        pass

    @staticmethod
    def change_feed_rate(value: int):
        SETTINGS.put_food_rate = value / 100

    def change_settings_display_fish_info(self, state):
        if state == Qt.Checked:
            self.check_box_fish.setChecked(True)
            SETTINGS.is_fish_info_visible = True
        else:
            self.check_box_fish.setChecked(False)
            SETTINGS.is_fish_info_visible = False

    def change_settings_display_fish(self, state):
        if state == Qt.Checked:
            self.check_box_fish.setChecked(True)
            SETTINGS.is_fish_visible = True
        else:
            self.check_box_fish.setChecked(False)
            SETTINGS.is_fish_visible = False

    def change_settings_display_memory(self, state):
        if state == Qt.Checked:
            self.check_box_memory.setChecked(True)
            SETTINGS.is_swap_memory_fixed = True
        else:
            self.check_box_memory.setChecked(False)
            SETTINGS.is_swap_memory_fixed = False

    # 滑动条的槽函数
    @staticmethod
    def change_memory_height(value):
        SETTINGS.swap_memory_height_rate = (
                value / 100
        )  # 写入SETTINGS，在LIFE_TANK中判断，如果不将交换内存固定，则生效
