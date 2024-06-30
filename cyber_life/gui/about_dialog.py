"""
关于界面
"""
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QFont, QDesktopServices, QCloseEvent, QKeyEvent
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView


class AboutDialog(QDialog):
    WINDOW_SIZE = (420, 640)

    def __init__(self, parent=None):
        # print('>>> \033[1;32m创建\033[0m AboutDialog')

        super(AboutDialog, self).__init__(parent)
        try:
            self.setWindowTitle("关于")
            self.resize(*self.WINDOW_SIZE)
            self.setFixedSize(*self.WINDOW_SIZE)
            self.setWindowIcon(QIcon(":/icon.ico"))

            # 布局管理器
            main_layout = QVBoxLayout()

            # 大居中标题
            self.label_title = QLabel("赛博小鱼缸", self)
            self.label_title.setAlignment(Qt.AlignCenter)
            font_title = QFont()
            font_title.setPointSize(24)  # 设置字体大小，根据需要调整
            self.label_title.setFont(font_title)
            main_layout.addWidget(self.label_title)

            # 第二行英文标题
            self.label_subtitle = QLabel("Cyber Life", self)
            self.label_subtitle.setAlignment(Qt.AlignCenter)
            font_subtitle = QFont()
            font_subtitle.setPointSize(12)  # 设置英文标题的字体大小，稍小于主标题
            self.label_subtitle.setFont(font_subtitle)
            main_layout.addWidget(self.label_subtitle)

            # 项目描述信息
            self.label_description = QLabel(
                "赛博小鱼缸是一款基于Python和PyQt5的开源桌面程序\n"
                "以一种生动的方式展示了CPU、内存、磁盘、网络等系统的运行状态\n"
                "同时还可以当成一个休闲软件，点击屏幕投喂饲料，维小鱼缸中的碳氧平衡\n",
                self
            )
            self.label_description.setAlignment(Qt.AlignCenter | Qt.AlignTop)
            main_layout.addWidget(self.label_description)

            self.table = self.get_table()
            main_layout.addWidget(self.table)

            # 提示信息
            self.label_copyright = QLabel("如果对赛博小鱼缸有任何建议或意见，可在b站或GitHub上留言", self)
            self.label_copyright.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(self.label_copyright)

            bottom_layout = QHBoxLayout()

            # 跳转到GitHub的链接按钮
            self.github_link_button = QPushButton("访问该项目的GitHub", self)
            self.github_link_button.clicked.connect(self.open_github)
            bottom_layout.addWidget(self.github_link_button)

            # 跳转到b站的链接按钮
            self.github_link_button = QPushButton("访问作者的b站", self)
            self.github_link_button.clicked.connect(self.open_bilibili)
            bottom_layout.addWidget(self.github_link_button)  # , alignment=Qt.AlignBottom | Qt.AlignRight

            main_layout.addLayout(bottom_layout)  # 这里不能用addWidget，否则会报错
            # 设置布局
            self.setLayout(main_layout)
        except Exception as e:
            print(e)

    @staticmethod
    def get_table():
        # 创建一个14行3列的表格
        element_dict = {
            "CPU物理核心数量": "绿色生物球数量",
            "CPU每核活跃程度": "绿色生物球的大小、颜色和移动速度",
            "剩余内存": "鱼缸中的水量",
            "交换内存": "土层高度",
            "使用的交换内存": "土层表面污染层的高度",
            "磁盘读频率": "土层向内收缩的震荡波频率",
            "磁盘写频率": "土层向外扩张的震荡波频率",
            "网络上传带宽": "鱼缸中心气泡的冒泡频率",
            "网络下载带宽": "鱼缸水面的波动频率与幅度",
            "C盘使用率": "水颜色的绿色程度",
            "秒": "贪吃蛇风格的边框蛇头位置",
            "一天中的大致时间": "贪吃蛇风格的边框颜色变化",
            "主屏幕大小": "鱼缸大小比例",
            "屏幕画面亮度": "鱼缸顶部灯光的亮度",
        }
        table = QTableWidget(len(element_dict), 2)
        table.setHorizontalHeaderLabels(['检测内容', '展示元素'])

        # 填充数据
        for i, (key, value) in enumerate(element_dict.items()):
            table.setItem(i, 0, QTableWidgetItem(key))
            table.setItem(i, 1, QTableWidgetItem(value))
        # 自适应列宽
        table.resizeColumnsToContents()

        # 设置表格为只读模式
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        # 禁止调整列宽和行高
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # 禁止选择单元格
        table.setSelectionMode(QTableWidget.NoSelection)

        # 添加到窗口布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(table)
        return table

    @staticmethod
    def open_github():
        QDesktopServices.openUrl(QUrl("https://github.com/Littlefean/cyber-life/"))

    @staticmethod
    def open_bilibili():
        QDesktopServices.openUrl(QUrl("https://space.bilibili.com/480804525/"))

    def closeEvent(self, event: QCloseEvent):
        """
        重写closeEvent方法
        """

        # 在不知明原因下，通知栏在关闭 settings 窗口时会连带着所有一起关闭，
        # 所以重新写一个关闭事件，隐藏窗口，并忽略关闭事件

        # 这里其实挺玄乎的，明明无论用sys.exit()/sys.exit(self)/sys.exit(QDialog)/super().closeEvent(event)都直接关闭所有窗口,有待深入研究。

        self.hide()
        event.ignore()

    def keyPressEvent(self, event: QKeyEvent):
        """
        重写keyPressEvent方法
        """

        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    # def __del__(self):
    #     print('>>> \033[1;31m销毁\033[0m AboutDialog')
