from colorsys import hsv_to_rgb, rgb_to_hsv

from PyQt5.QtGui import QColor


def get_color_by_hsv_ratio(color_start: QColor, color_end: QColor, ratio: float) -> QColor:
    """
    色彩空间过渡，获取一个颜色
    此代码由AI生成，还未经过测试
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
