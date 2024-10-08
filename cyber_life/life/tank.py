"""
存放关于小鱼缸的数据
"""

from datetime import datetime, timedelta
from math import sin

from PIL import ImageGrab
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QLinearGradient

from cyber_life.computer_info.manager import SYSTEM_INFO_MANAGER
from cyber_life.life.sand_wave_flow import SandWaveFlow
from cyber_life.service.settings import SETTINGS
from cyber_life.static import COLOR_DEBUG
from cyber_life.static import TANK_SCREEN_WIDTH
from cyber_life.tools.compute import lerp, RangeDivider
from cyber_life.tools.singleton import SingletonMeta


class _LifeTank(metaclass=SingletonMeta):
    """
    存放关于小鱼缸的数据
    绘制水面、沙子表面层和深层、沙层中的震荡波，并进行更新
    """

    # 水面和地面渐变的比例系数
    # TODO: 调节这个系数，使得视觉效果更好
    ALPHA = 0.02

    # 由网络速度决定波动的大小，包括振幅、频率、周期
    WAVE_INFO_RD = RangeDivider(
        (1, 100, 1000, 5000, 1_0000, 10_0000, 50_0000, 150_0000),
        (
            (0, 0.01, 0),
            (2, 0.01, 1),
            (2, 0.02, 1),
            (2, 0.04, 2),
            (4, 0.05, 6),
            (6, 0.05, 7),
            (8, 0.05, 8),
            (10, 0.06, 9),
            (10, 0.1, 10)
        )
    )

    # 由时间决定颜色
    STROKE_COLOR_RD = RangeDivider(
        # 早晨5点到6点以及傍晚6点到7点，返回深紫到石灰色
        # 晚上7点到晚上10点，返回深蓝色
        # 晚上10点到早晨5点，接近纯黑色，但不完全黑色
        # 早上7点到上午10点，清晨色
        # 上午10点到下午4点，明亮的日光色
        # 下午4点到下午6点，夕阳色
        (5, 7, 10, 16, 18, 19, 22),
        ('gray', 'purple', 'skyblue', 'yellow', 'orange', 'purple', 'darkblue', 'gray')
    )

    def __init__(self, width: int):
        """
        初始化小鱼缸数据
        :param width: 界面大小宽度，px
        """

        self.width = int(width)
        # 获取屏幕的宽度和高度
        w, h = ImageGrab.grab().size
        self.height = int(self.width * (h / w))

        # 分界线
        # 三个数字分别是水面的、表层沙顶部、深层沙顶部的 y 值
        # 这三个值都是渐变的，每帧的位移（也就是速率）与 abs(x - x_target) 成正比，比例系数设为 ALPHA
        # 当某一个元素 x_target 突变后保持不变时，x 的变化类似指数衰减，收敛于 x_target
        self.division: list[float] = [0., self.height, self.height]  # 水面的、表层沙顶部、深层沙顶部的 y 值
        # 目标值，突变的
        # 由内存占用率计算得到
        self.division_target: list[float] = [0., 0., 0.]
        # 很抱歉，用 0 1 2 当索引牺牲了可读性，但用起来方便，而且变量名相对统一
        # 当然也可以写成字典

        # 小鱼缸颜色
        self.water_color_best = QColor(40, 80, 255, 80)
        # 将棕色作为最差颜色，不太好，容易和沙子颜色混淆
        # self.water_color_worst = QColor(200, 150, 50, 40)
        self.water_color_worst = QColor(22, 135, 67, 80)

        # 顶部灯光亮度 0 表示黑 1表示最亮
        self.light_brightness_target = 1
        self.light_brightness_current = 0

        # 震荡圆圈特效
        # 向外扩散的是写入磁盘的速度，向内扩散的是读取磁盘的速度
        # 因为扩散波像是某个东西掉入地上，成为了地面的一部分，可以代表写入
        # 实际上沙子地面代表了硬盘
        self.sand_wave_outer = SandWaveFlow(self.width / 2, 1)
        self.sand_wave_inner = SandWaveFlow(self.width / 2, -1)

        self.time = 0
        self.tick()  # 初始化的时候就将高度信息更新好

    def get_sand_surface_height_target(self):
        """
        沙子表面层高度，y值，坐标原点为左上角
        保证显示时，空气和水代表总物理内存，表层沙和深层沙代表总交换内存
        """

        # 开了自定义交换内存高度，根据这个设定值返回
        if SETTINGS.is_swap_memory_fixed:
            return self.height * (1 - SETTINGS.swap_memory_height_rate)
        # 否则根据系统内存占用率计算
        else:
            memory_info = SYSTEM_INFO_MANAGER.INSPECTOR_MEMORY.get_current_result()
            return self.height * memory_info.physical_memory_total / (  # 这个算的是物理内存占总内存的比例
                    memory_info.physical_memory_total + memory_info.swap_memory_total
            )

    def tick(self):
        """
        小鱼缸更新一次
        """

        # 更新内存信息
        memory_info = SYSTEM_INFO_MANAGER.INSPECTOR_MEMORY.get_current_result()

        # 更新分界线的目标值
        # 1. 第二条分界线：物理内存和交换内存的分界线
        self.division_target[1] = self.get_sand_surface_height_target()
        # 2. 第一条分界线：物理内存占用率，空气为已使用内存，水为未使用内存
        self.division_target[0] = self.division_target[1] * memory_info.physical_memory_percent
        # 3. 第三条分界线：交换内存占用率，表层沙为已使用内存，深层沙为未使用内存
        self.division_target[2] = lerp(self.division_target[1], self.height, memory_info.swap_memory_percent)

        # 更新分界线的当前值，渲染用，做成渐变的
        self.division = [
            lerp(self.division[i], self.division_target[i], self.ALPHA) for i in range(3)
        ]

        # 更新亮度
        self.light_brightness_target = SYSTEM_INFO_MANAGER.INSPECTOR_SCREEN.get_current_result()
        self.light_brightness_current = lerp(self.light_brightness_current, self.light_brightness_target, self.ALPHA)
        self.time += 1

        # 更新震荡数据
        self.sand_wave_outer.set_frequency_by_disk_io(
            SYSTEM_INFO_MANAGER.INSPECTOR_DISK_IO.get_current_result().write_bytes
        )
        self.sand_wave_inner.set_frequency_by_disk_io(
            SYSTEM_INFO_MANAGER.INSPECTOR_DISK_IO.get_current_result().read_bytes
        )

        # 更新震荡圆圈列表
        self.sand_wave_outer.tick()
        self.sand_wave_inner.tick()

    def get_wave_height(self, x, wave_info: tuple[float, float, float]):
        """
        获取波浪线高度，用于绘制sin型波浪水面
        """

        # x 前面的参数才能改变频率
        # 机械波波函数：y(x, t) = Asin(ω(t+x/v)) = Asin((t/2π + 2πx/v) × f)
        # 系数全重置了

        return wave_info[0] * sin((x + self.time * wave_info[2]) * wave_info[1] * 0.2)

    def paint(self, painter: QPainter):
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.NoBrush)
        # ---------------------------------------- 绘制顶部灯光 ----------------------------------------
        gradient = QLinearGradient(0, 0, 0, self.division[0])
        gradient.setColorAt(
            0.0,
            QColor(255, 255, 255, round(255 * self.light_brightness_current))  # 开始颜色
        )
        gradient.setColorAt(
            1.0,
            QColor(255, 255, 255, 0)  # 结束颜色
        )
        # 绘制矩形，使用渐变填充
        painter.fillRect(0, 0, self.width, self.height, gradient)

        # ---------------------------------------- 填充波浪形水（定积分画法） ----------------------------------------
        water_color_ratio = SYSTEM_INFO_MANAGER.INSPECTOR_DISK_USAGE.get_current_result()
        if COLOR_DEBUG:
            water_color_ratio = (0.005 * self.time) % 1

        painter.setBrush(lerp(
            self.water_color_best,
            self.water_color_worst,
            water_color_ratio
        ))

        # 绘制水面
        wave_info = self.WAVE_INFO_RD[
            SYSTEM_INFO_MANAGER.INSPECTOR_NETWORK.get_current_result().recv_speed
        ]
        dx = 10  # 一个小微元，即每次绘制细矩形的宽度
        for x in range(0, self.width, dx):
            y = round(self.division[0] + self.get_wave_height(x, wave_info))
            painter.drawRect(
                x, y,
                dx, self.height - y
            )

        # ---------------------------------------- 填充沙子 ----------------------------------------
        # 表层颜色应该更深，深层颜色应该更浅，因为表层是污染层，深层有石英石
        # 绘制表面层
        painter.setBrush(QColor(62, 53, 28))
        painter.drawRect(
            0,
            round(self.division[1]),
            round(self.width),
            round(self.height - self.division[1]),
        )
        # 绘制深层
        painter.setBrush(QColor(92, 73, 36))
        painter.drawRect(
            0,
            round(self.division[2]) + 1,  # 加1是为了防止两层完全重合，表层看不到
            round(self.width),
            round(self.height - self.division[2]),
        )

        # ---------------------------------------- 绘制波浪圆圈 ----------------------------------------
        self.sand_wave_outer.paint(painter)
        self.sand_wave_inner.paint(painter)

        # ---------------------------------------- 绘制小鱼缸边框 ----------------------------------------
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, self.width - 1, self.height)

        # ---------------------------------------- 绘制贪吃蛇风格的边框 ----------------------------------------
        self.draw_snake_style_border(painter, self.width, self.height)

    def draw_snake_style_border(self, painter: QPainter, width: int, height: int):
        """
        绘制贪吃蛇风格的边框
        """

        # 绘制贪吃蛇风格的边框
        snake_length = min(width, height)
        perimeter = (width + height) * 2  # 周长
        # 这里时从 left top 开始计算的，为了让起点从 top center 开始，需要将时间向后推移一点
        now = datetime.now()
        delay_seconds = (width / 2) / perimeter * 60  # 计算运动到上边框一半所需要秒数
        now += timedelta(seconds=delay_seconds)
        # 加上上面计算运动到上边框一半需要的时间，从而将蛇头平移到上边框的中央
        progression = (now.second + now.microsecond / 1000000) / 60  # 进度, 0-1
        # microsecond显示秒的六位小数，但是以整数的形式，上一行代码的作用是获得更精确的时间，从而使动画连贯
        # 秒本身0-59循环，所以上一行代码的结果是0-1，例如当0秒时进度为0

        # debug 用
        if COLOR_DEBUG:
            progression = (self.time % 500) / 500  # 进度, 0-1

        # 设计思想：有四条蛇，同时从不同位置出发，分别沿着四条边运动，当运动到边缘时，蛇头与另一边的蛇头刚好相遇
        # 运动出界不会显示，从而好像一条蛇在绕圈
        # 四条蛇的运动周期都是60s，运动长度相同，从而速度相同
        # 但是第四条蛇与第一条蛇相遇时，第四条蛇的运动长度刚好用完，导致第四条蛇重新循环，从视野中消失
        # 所以添加第五条蛇，与第一条蛇直接在开始的时候蛇头在坐标原点相遇
        stage_1_head_x = lerp(0, perimeter, progression)  # 蛇头从0出发
        stage_1_tail_x = stage_1_head_x - snake_length
        stage_2_head_y = lerp(-width, perimeter - width, progression)
        stage_2_tail_y = stage_2_head_y - snake_length
        stage_3_head_x = lerp(perimeter - height, -height, progression)
        stage_3_tail_x = stage_3_head_x + snake_length
        stage_4_head_y = lerp(perimeter, 0, progression)
        stage_4_tail_y = stage_4_head_y + snake_length
        # 第五段是防止第四段结束时突然消失
        stage_5_tail_y = lerp(snake_length, -perimeter + snake_length, progression)
        stage_5_head_y = stage_5_tail_y - snake_length

        painter.setPen(self.get_stroke_color())
        painter.drawLine(
            round(stage_1_tail_x),
            0,
            round(stage_1_head_x),
            0
        )
        painter.drawLine(
            round(width - 1),
            round(stage_2_tail_y),
            round(width - 1),
            round(stage_2_head_y)
        )
        painter.drawLine(
            round(stage_3_tail_x),
            round(height),
            round(stage_3_head_x),
            round(height)
        )
        painter.drawLine(
            0,
            round(stage_4_tail_y),
            0,
            round(stage_4_head_y)
        )
        painter.drawLine(
            0,
            round(stage_5_tail_y),
            0,
            round(stage_5_head_y)
        )

    def get_stroke_color(self) -> QColor:
        """
        根据当前的时间来获取颜色
        """

        current_hour = datetime.now().hour
        if COLOR_DEBUG:
            current_hour = (self.time // 10 % 24)

        return QColor(self.STROKE_COLOR_RD[current_hour])


LIFE_TANK = _LifeTank(TANK_SCREEN_WIDTH)
