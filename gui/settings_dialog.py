from PyQt5.QtWidgets import QDialog, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from service.settings import SETTINGS


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设置")
        self.setGeometry(400, 400, 400, 400)
        # 设置icon
        self.setWindowIcon(QIcon('assert/icon.ico'))
        # 小鱼
        self.check_box_fish = QCheckBox("显示小鱼", self)
        self.check_box_fish.move(10, 10)
        self.check_box_fish.setChecked(SETTINGS.is_fish_visible)
        self.check_box_fish.stateChanged.connect(self.change_settings_display_fish)
        # 内存
        self.check_box_memory = QCheckBox("将交换内存固定在总高度的1/8", self)
        self.check_box_memory.move(10, 40)
        self.check_box_memory.setChecked(SETTINGS.is_swap_memory_fixed)
        self.check_box_memory.stateChanged.connect(self.change_settings_display_memory)
        pass

    def change_settings_display_fish(self, state):
        if state == Qt.Checked:
            print("""显示小鱼""")
            self.check_box_fish.setChecked(True)
            SETTINGS.is_fish_visible = True
        else:
            print("""不显示小鱼""")
            self.check_box_fish.setChecked(False)
            SETTINGS.is_fish_visible = False

    def change_settings_display_memory(self, state):
        if state == Qt.Checked:
            print("""将交换内存固定在总高度的1/8""")
            self.check_box_memory.setChecked(True)
            SETTINGS.is_swap_memory_fixed = True
        else:
            print("""不将交换内存固定在总高度的1/8""")
            self.check_box_memory.setChecked(False)
            SETTINGS.is_swap_memory_fixed = False
