from PyQt5.QtGui import QColor


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
