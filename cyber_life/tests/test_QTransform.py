"""
pyQt5 的 QTransform 变化不太了解，实操一下
"""
import sys
from math import sin, cos, pi

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTransform, QPainter, QPixmap
# 不建议用 * 导入。因为会导入一些不需要的模块，比如 QtCore里面的各种类 等，让IDE可能出现错误类型提示。
from PyQt5.QtWidgets import QApplication, QWidget

# noinspection PyUnresolvedReferences
from assets import assets


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口的基本属性
        self.setWindowTitle("赛博小鱼缸")
        self.setWindowFlags(
            # 始终置顶
            Qt.WindowStaysOnTopHint
        )

        # 设置icon
        self.setWindowIcon(QIcon(":/icon.ico"))
        # 设置大小
        self.resize(300, 300)

        # 设置窗口大小和位置
        self.setGeometry(10, 10, 300, 300)
        self.move(
            QApplication.desktop().screenGeometry().width() - self.width() - 100,
            QApplication.desktop().screenGeometry().height() - self.height() - 200,
        )

    def paintEvent(self, event):
        # 第一行为对照，提及指定鱼时按坐标命名，从（1，1）到（5，4）
        painter = QPainter(self)
        pixmap = QPixmap(f":/fish_0.png")
        painter.drawPixmap(20, 20, pixmap)
        pixmap = QPixmap(f":/fish_0.png")
        painter.drawPixmap(100, 20, pixmap)
        pixmap = QPixmap(f":/fish_0.png")
        painter.drawPixmap(180, 20, pixmap)
        pixmap = QPixmap(f":/fish_0.png")
        painter.drawPixmap(260, 20, pixmap)

        # 第二行
        pixmap = QPixmap(f":/fish_0.png")
        painter.drawPixmap(20, 80, pixmap)  # 第一个为对照
        pixmap = QPixmap(f":/fish_0.png").transformed(QTransform().rotate(45))
        painter.drawPixmap(100, 80, pixmap)  # 顺时针旋转45°
        pixmap = QPixmap(f":/fish_0.png").transformed(QTransform().rotate(45).scale(-1, 1))
        painter.drawPixmap(180, 80, pixmap)  # 顺时针旋转45°坐标轴，scale在新坐标轴上放缩，即在（2，2）的基础上x轴反向
        pixmap = QPixmap(f":/fish_0.png").transformed(QTransform().scale(-1, 1).rotate(45))
        painter.drawPixmap(260, 80, pixmap)  # scale使x轴反向，所以rotate旋转方向变了，后面探讨变的规则是啥

        # 第三行
        pixmap = QPixmap(f":/fish_0.png").transformed(QTransform().shear(2, 0))
        painter.drawPixmap(20, 140, pixmap)  # y轴坐标不变（因为第二个参数是0），x轴坐标为y轴坐标乘以第一个参数+x轴原本坐标
        pixmap = QPixmap(f":/fish_0.png").transformed(QTransform().rotate(45).scale(0.5, 1))
        painter.drawPixmap(100, 140, pixmap)  # 坐标轴旋转后放缩，与（3，3）对比
        pixmap = QPixmap(f":/fish_0.png").transformed(QTransform().scale(0.5, 1).rotate(45))
        painter.drawPixmap(180, 140, pixmap)  # 旋转和放缩先后顺序不同，结果可能不同
        pixmap = QPixmap(f":/fish_0.png").transformed(QTransform().scale(-1, 1))
        painter.drawPixmap(260, 140, pixmap)  # scale第一个参数是x轴方向放缩，第二个参数是y轴方向放缩

        # 第四行
        pixmap = QPixmap(f":/fish_0.png").transformed(QTransform().shear(2, 0).scale(0.5, 1))
        painter.drawPixmap(20, 200, pixmap)  # 与（3，1）对比，发现扭曲会改变坐标轴方向
        pixmap = QPixmap(f":/fish_0.png").transformed(QTransform().scale(0.5, 1).shear(2, 0))
        painter.drawPixmap(100, 200, pixmap)  # 与（4，1）对比，扭曲和放缩顺序不同，结果可能不同
        pixmap = QPixmap(f":/fish_0.png").transformed(QTransform().scale(0.5, 1))
        painter.drawPixmap(180, 200, pixmap)  # 与（3，3）对比，放缩后旋转，放缩会影响旋转的角度
        pixmap = QPixmap(f":/fish_0.png").transformed(QTransform().shear(2, 0).scale(-0.5, 1))
        painter.drawPixmap(260, 200, pixmap)  # 与（4，1）对比，根据两者沿y轴对称，可以判断y轴方向

        """
        查阅博客及帮助文档，QTransform 对象包含 3 x 3 矩阵
        对其进行scale、shear、rotate等均是在操作这个 3 x 3 矩阵
        m11 m12 m13
        m21 m22 m23
        m31 m32 m33
        其中scale的两个参数分别赋值给 m11 m22
        shear的两个参数分别赋值给 m21 m12
        translate的两个参数分别赋值给 m31 m32
        m13 m23 m33 的值一般分别为 0 0 1
        计算公式为：
        x' = m11*x + m21*y + dx
        y' = m22*y + m12*x + dy
        if (is not affine) {
            w' = m13*x + m23*y + m33
            x' /= w'
            y' /= w'
        }
        affine表示仿射变换
        x、y为图像中点变换前的坐标，x'、y'表示图像中点变换后的坐标
        如果连续变换，会进行矩阵乘法，例如按照 translate -> scale -> rotate 的顺序变换时，应写作：
        |cosα sinα 0 | |sx 0 0| |1 0 0  |
        |-sinα cosα 0|*|0 sy 0|*|0 1 0  |
        |0 0 1       | |0 0 1 | |dx dy 1|
        最终的矩阵为 QTransform 对象 3 x 3 矩阵并进行图像变换
        可以借助这篇文章进行理解：https://www.cnblogs.com/ITnoteforlsy/p/18148656
        """

        # 第五行 在上面基础上，可以理解shear和scale即使参数和rotate相同，但结果是矩阵相乘，故得到的矩阵还是和rotate的矩阵是不同的
        pixmap = QPixmap(f":/fish_0.png").transformed(
            QTransform().shear(-sin(pi / 4), sin(pi / 4)).scale(cos(pi / 4), cos(pi / 4)))
        painter.drawPixmap(20, 260, pixmap)
        pixmap = QPixmap(f":/fish_0.png").transformed(
            QTransform().scale(cos(pi / 4), cos(pi / 4)).shear(-sin(pi / 4), sin(pi / 4)))
        painter.drawPixmap(100, 260, pixmap)
        pixmap = QPixmap(f":/fish_0.png").transformed(
            QTransform().shear(-sin(pi / 3), sin(pi / 3)).scale(cos(pi / 3), cos(pi / 3)))
        painter.drawPixmap(180, 260, pixmap)
        pixmap = QPixmap(f":/fish_0.png").transformed(
            QTransform().scale(cos(pi / 3), cos(pi / 3)).shear(-sin(pi / 3), sin(pi / 3)))
        painter.drawPixmap(260, 260, pixmap)


def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
