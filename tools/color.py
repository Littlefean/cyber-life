from PyQt5.QtGui import QColor
from colorsys import hsv_to_rgb, rgb_to_hsv


def get_color_by_linear_ratio(color_start: QColor, color_end: QColor, ratio: float) -> QColor:
    """
    线性过渡，获取一个颜色
    :param color_start: 开始颜色
    :param color_end: 终止颜色
    :param ratio: 0~1之间的小数，
    当值=0时，返回开始颜色，
    当值=1时，返回终止颜色，
    当值在0~1之间时，返回过渡颜色
    :return:
    """
    red = color_start.red() + (color_end.red() - color_start.red()) * ratio
    green = color_start.green() + (color_end.green() - color_start.green()) * ratio
    blue = color_start.blue() + (color_end.blue() - color_start.blue()) * ratio
    alpha = color_start.alpha() + (color_end.alpha() - color_start.alpha()) * ratio
    return QColor(
        round(red),
        round(green),
        round(blue),
        round(alpha),
    )


def get_color_by_hsv_ratio(color_start: QColor, color_end: QColor, ratio: float) -> QColor:
    """
    色彩空间过渡，获取一个颜色
    :param color_start:
    :param color_end:
    :param ratio:
    :return:
    """
    hsv_start = rgb_to_hsv(color_start.red() / 255, color_start.green() / 255, color_start.blue() / 255)
    hsv_end = rgb_to_hsv(color_end.red() / 255, color_end.green() / 255, color_end.blue() / 255)
    hsv_ratio = (hsv_end[0] - hsv_start[0]) * ratio + hsv_start[0]
    hsv_ratio = hsv_ratio % 1
    hsv_ratio = hsv_ratio if hsv_ratio >= 0 else 1 + hsv_ratio
    hsv_ratio = hsv_ratio if hsv_ratio <= 1 else 1 - hsv_ratio
    hsv_ratio = hsv_ratio if hsv_ratio >= 0 else 0
    hsv_ratio = hsv_ratio if hsv_ratio <= 1 else 1
    rgb_ratio = hsv_to_rgb(hsv_ratio, hsv_start[1], hsv_start[2])
    red = round(rgb_ratio[0] * 255)
    green = round(rgb_ratio[1] * 255)
    blue = round(rgb_ratio[2] * 255)
    alpha = color_start.alpha() + (color_end.alpha() - color_start.alpha()) * ratio
    return QColor(
        red,
        green,
        blue,
        round(alpha),
    )
