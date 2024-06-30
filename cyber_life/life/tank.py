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
from cyber_life.static import TANK_SCREEN_WIDTH
from cyber_life.tools.color import get_color_by_linear_ratio
from cyber_life.tools.compute import number_to_number
from cyber_life.tools.singleton import SingletonMeta


class _LifeTank(metaclass=SingletonMeta):
    """
    存放关于小鱼缸的数据
    绘制水面、沙子表面层和深层、沙层中的震荡波，并进行更新
    """
    _COLOR_DEBUG = False

    # 水面和地面渐变的比例系数
    # TODO: 调节这个系数，使得视觉效果更好
    ALPHA = 0.02

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
        # 三个数字分别是水面的、沙子表面层的、沙子底层的 y 值
        # 这三个值都是渐变的，每帧的位移（也就是速率）与 abs(x - x_target) 成正比，比例系数设为 ALPHA
        # 当某一个元素 x_target 突变后保持不变时，x 的变化类似指数衰减，收敛于 x_target
        self.division: list[float] = [0., self.height, self.height]  # 水面的、沙子表面层的、沙子底层的 y 值
        # 目标值，突变的
        # 由内存占用率计算得到
        self.division_target: list[float] = [0., 0., 0.]
        # 很抱歉，用 0 1 2 当索引牺牲了可读性，但用起来方便，而且变量名相对统一
        # 当然也可以写成字典

        # 小鱼缸颜色
        self.water_color_best = QColor(40, 100, 255, 40)
        # 将棕色作为最差颜色，不太好，容易和沙子颜色混淆
        # self.water_color_worst = QColor(200, 150, 50, 40)
        self.water_color_worst = QColor(22, 135, 67, 40)

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
        沙子表面层高度，y值
        保证显示时，上层高度代表物理内存，下层高度代表交换内存
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
        # 2. 第一条分界线：物理内存占用率
        self.division_target[0] = self.division_target[1] * memory_info.physical_memory_percent
        # 3. 第三条分界线：交换内存占用率
        self.division_target[2] = number_to_number(self.division_target[1],
                                                   self.height,
                                                   memory_info.swap_memory_percent)

        # 更新分界线的当前值，渲染用，做成渐变的
        self.division = [
            number_to_number(
                self.division[i],
                self.division_target[i],
                self.ALPHA
            ) for i in range(3)
        ]

        # 更新亮度
        self.light_brightness_target = SYSTEM_INFO_MANAGER.INSPECTOR_SCREEN.get_current_result()
        self.light_brightness_current = self.light_brightness_target * 0.01 + self.light_brightness_current * 0.99
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

    @staticmethod
    def get_wave_info_by_recv_speed(recv_speed: float) -> dict:
        """
        根据接收速度获取波动信息
        """
        # 波速度10为最快速度，1为最慢速度
        # 频率0.01 最长，0.1 最短
        if recv_speed < 1:
            amplitude = 0
            frequency = 0.01
            speed = 0
        elif recv_speed < 100:
            amplitude = 2
            frequency = 0.01
            speed = 1
        elif recv_speed < 1000:
            amplitude = 2
            frequency = 0.02
            speed = 1
        elif recv_speed < 5000:
            amplitude = 2
            frequency = 0.04
            speed = 2
        elif recv_speed < 1_0000:
            amplitude = 4
            frequency = 0.05
            speed = 6
        elif recv_speed < 10_0000:
            amplitude = 6
            frequency = 0.05
            speed = 7
        elif recv_speed < 50_0000:
            amplitude = 8
            frequency = 0.05
            speed = 8
        elif recv_speed < 150_0000:
            amplitude = 10
            frequency = 0.06
            speed = 9
        else:
            amplitude = 10
            frequency = 0.1
            speed = 10
        return {
            'amplitude': amplitude,
            'frequency': frequency,
            'speed': speed
        }

    def get_wave_height(self, x, wave_info: dict):
        """
        获取波浪线高度，用于绘制sin型波浪水面
        """
        # x 前面的参数才能改变频率
        # 机械波波函数：y(x, t) = Asin(ω(t+x/v)) = Asin((t/2π + 2πx/v) × f)
        # 系数全重置了

        return wave_info['amplitude'] * sin((x + self.time * wave_info['speed']) * wave_info['frequency'] * 0.2)

    def paint(self, painter: QPainter):
        # 绘制顶部灯光
        painter.setPen(Qt.NoPen)
        gradient = QLinearGradient(0, 0, 0, self.division[0])
        gradient.setColorAt(
            0.0,
            QColor(
                255,
                255,
                255,
                round(255 * self.light_brightness_current)
            )
        )  # 开始颜色
        gradient.setColorAt(
            1.0,
            QColor(255, 255, 255, 0)
        )  # 结束颜色

        # 填充波浪形水（定积分画法）
        painter.setPen(Qt.NoPen)
        if self._COLOR_DEBUG:
            # water_color_ratio = 0.5 * sin(self.time * 0.01) + 0.5
            water_color_ratio = (0.005 * self.time) % 1
        else:
            water_color_ratio = SYSTEM_INFO_MANAGER.INSPECTOR_DISK_USAGE.get_current_result()

        painter.setBrush(get_color_by_linear_ratio(
            self.water_color_best,
            self.water_color_worst,
            water_color_ratio
        ))

        # 绘制水面
        wave_info = self.get_wave_info_by_recv_speed(
            SYSTEM_INFO_MANAGER.INSPECTOR_NETWORK.get_current_result().recv_speed
        )
        dx = 10  # 一个小微元，即每次绘制细矩形的宽度
        x = 0  # 没搞懂为啥要用 x_next 和 y_next 那一套，这里优化直接用 x 就行了
        for _ in range(0, self.width, dx):
            y = round(self.division[0] + self.get_wave_height(x, wave_info))
            painter.drawRect(
                x, y,
                dx, self.height - y
            )
            x += dx
        # 对之前问题的说明：
        #     除了第一个矩形被绘制了 1 次外，后续的矩形都被绘制了 2 次
        #     所以第一个看起来比其他的*更透明*
        #     优化后每个矩形只绘制一次，颜色与之前的成品相去甚远
        # 所以...
        # TODO: 更改水体颜色

        # 绘制矩形，使用渐变填充
        painter.fillRect(0, 0, self.width, self.height, gradient)

        # 表层颜色应该更深，深层颜色应该更浅，因为表层是污染层，深层有石英石
        # 绘制表面层
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(62, 53, 28))
        painter.drawRect(
            0,
            round(self.division[1]),
            round(self.width),
            round(self.height - self.division[1]),
        )
        # 绘制深层
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(92, 73, 36))
        painter.drawRect(
            0,
            round(self.division[2]) + 1,  # 加1是为了防止两层完全重合，表层看不到
            round(self.width),
            round(self.height - self.division[2]),
        )

        # 绘制波浪圆圈
        self.sand_wave_outer.paint(painter)
        self.sand_wave_inner.paint(painter)

        # 绘制小鱼缸边框
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, self.width - 1, self.height)

        # 绘制贪吃蛇风格的边框
        draw_snake_style_border(painter, self.width, self.height)


def draw_snake_style_border(painter: QPainter, width: int, height: int):
    """
    绘制贪吃蛇风格的边框
    这个函数可以考虑移动到其他地方
    :param painter:
    :param width:
    :param height:
    :return:
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
    # progression = (self.time % 777) / 777  # 进度, 0-1

    # 设计思想：有四条蛇，同时从不同位置出发，分别沿着四条边运动，当运动到边缘时，蛇头与另一边的蛇头刚好相遇
    # 运动出界不会显示，从而好像一条蛇在绕圈
    # 四条蛇的运动周期都是60s，运动长度相同，从而速度相同
    # 但是第四条蛇与第一条蛇相遇时，第四条蛇的运动长度刚好用完，导致第四条蛇重新循环，从视野中消失
    # 所以添加第五条蛇，与第一条蛇直接在开始的时候蛇头在坐标原点相遇
    stage_1_head_x = number_to_number(0, perimeter, progression)  # 蛇头从0出发
    stage_1_tail_x = stage_1_head_x - snake_length
    stage_2_head_y = number_to_number(-width, perimeter - width, progression)
    stage_2_tail_y = stage_2_head_y - snake_length
    stage_3_head_x = number_to_number(perimeter - height, -height, progression)
    stage_3_tail_x = stage_3_head_x + snake_length
    stage_4_head_y = number_to_number(perimeter, 0, progression)
    stage_4_tail_y = stage_4_head_y + snake_length
    # 第五段是防止第四段结束时突然消失
    stage_5_tail_y = number_to_number(snake_length, -perimeter + snake_length, progression)
    stage_5_head_y = stage_5_tail_y - snake_length

    painter.setPen(get_stroke_color())
    painter.setBrush(Qt.NoBrush)
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


def get_stroke_color() -> QColor:
    """
    根据当前的时间来获取颜色
    :return: QColor
    """
    current_hour = datetime.now().hour

    if 5 <= current_hour < 7 or 18 <= current_hour < 19:
        # 早晨5点到6点以及傍晚6点到7点，返回深紫到石灰色
        return QColor('purple')
    elif 19 <= current_hour < 22:
        # 晚上7点到晚上10点，返回深蓝色
        return QColor('darkblue')
    elif 22 <= current_hour or current_hour < 5:
        # 晚上10点到早晨5点，接近纯黑色，但不完全黑色
        return QColor('gray')
    elif 7 <= current_hour < 10:
        # 早上7点到上午10点，清晨色
        return QColor('skyblue')
    elif 10 <= current_hour < 16:
        # 上午10点到下午4点，明亮的日光色
        return QColor('yellow')
    elif 16 <= current_hour < 18:
        # 下午4点到下午6点，夕阳色
        return QColor('orange')

    return QColor('gray')


LIFE_TANK = _LifeTank(TANK_SCREEN_WIDTH)
