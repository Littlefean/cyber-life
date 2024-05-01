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
        # 一个勾选框，默认是勾选的状态
        self.checkBox = QCheckBox("显示小鱼", self)
        self.checkBox.move(10, 10)
        self.checkBox.setChecked(True)
        self.checkBox.stateChanged.connect(self.change_settings_display_fish)

        pass

    def change_settings_display_fish(self, state):
        if state == Qt.Checked:
            print("""显示小鱼""")
            self.checkBox.setChecked(True)
            SETTINGS.is_fish_visible = True
        else:
            print("""不显示小鱼""")
            self.checkBox.setChecked(False)
            SETTINGS.is_fish_visible = False
