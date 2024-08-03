from PyQt5.QtGui import QColor

_SUPPORTED_NUMBER_TYPES = (int, float, complex)
_SUPPORTED_TYPES = int | float | complex | list | tuple | QColor


def lerp(
        start: _SUPPORTED_TYPES,
        end: _SUPPORTED_TYPES,
        rate: float
) -> _SUPPORTED_TYPES:
    """
    线行插值 (Linear Interpolation)，简称 lerp
    支持数字、元素是数字的序列、QColor

    :param start: 起始值
    :param end: 终止值
    :param rate: 插值比率

    >>> lerp(1., 2., 0.5)
    1.5
    >>> lerp(2, 2j, 0.5)
    (1+1j)
    >>> lerp([1, 3, 5], [2, 4, 6], 0.1)
    [1.1, 3.1, 5.1]
    >>> lerp((1, 3, 5), (2, 4, 6), 0.9)
    (1.9, 3.9, 5.9)
    >>> lerp(QColor(200, 0, 0, 255), QColor(0, 200, 0, 255), 0.5).getRgb()  # 这里只能 getRgb 一下，因为 QColor 不能直接显示
    (100, 100, 0, 255)
    """

    if isinstance(start, _SUPPORTED_NUMBER_TYPES):
        assert isinstance(end, _SUPPORTED_NUMBER_TYPES)
        return start + (end - start) * rate

    elif isinstance(start, (list, tuple)):
        assert (isinstance(end, (list, tuple))
                and all(isinstance(i, _SUPPORTED_NUMBER_TYPES) for i in start)
                and all(isinstance(i, _SUPPORTED_NUMBER_TYPES) for i in end)
                and len(start) == len(end))
        return start.__class__(lerp(a, b, rate) for a, b in zip(start, end))

    elif isinstance(start, QColor):
        assert isinstance(end, QColor)
        return QColor(*map(round, lerp(start.getRgb(), end.getRgb(), rate)))

    else:
        raise TypeError(f'不支持的类型：{type(start)}')
