from numbers import Real
from typing import Literal

from PyQt5.QtGui import QColor

_SUPPORTED_NUMBER_TYPES = (int, float, complex)
_SUPPORTED_TYPES = int | float | complex | list | tuple | QColor


def lerp(
        start: _SUPPORTED_TYPES,
        end: _SUPPORTED_TYPES,
        rate: float
) -> _SUPPORTED_TYPES:
    """
    线性插值 (Linear Interpolation)，简称 lerp
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


class RangeDivider:
    """
    范围分割器，用于根据值范围划分标签

    每个区间左闭右开，区间数目 = 标签数目 + 1

    支持遍历查找和二分查找

    >>> RangeDivider([100, 200, 300, 400], ['a', 'b', 'c', 'd', 'e'])[360]
    'd'
    >>> RangeDivider([100, 200, 300, 400], ['a', 'b', 'c', 'd', 'e'])[100]
    'b'
    >>> RangeDivider([100, 200, 300, 400], ['a', 'b', 'c', 'd', 'e'])[400]
    'e'

    >>> RangeDivider([100, 200, 300, 400], ['a', 'b', 'c', 'd', 'e']).get_tag(360, mode='binary')
    'd'
    >>> RangeDivider([100, 200, 300, 400], ['a', 'b', 'c', 'd', 'e']).get_tag(100, mode='binary')
    'b'
    >>> RangeDivider([100, 200, 300, 400], ['a', 'b', 'c', 'd', 'e']).get_tag(400, mode='binary')
    'e'
    """

    __slots__ = ('_divisions', '_tags')

    def __init__(self, divisions: list | tuple, tags: list | tuple):
        """
        会对传入的 divisions 去重并排序

        :param divisions: 范围分割点
        :param tags: 标签
        """

        assert isinstance(divisions, (list, tuple)) and isinstance(tags, (list, tuple))
        assert all(isinstance(i, Real) for i in divisions)

        self._divisions = sorted(set(divisions))  # 去重并排序，副本
        self._tags = tags.copy() if isinstance(tags, list) else tags  # 副本

        assert 0 < len(self._divisions) == len(self._tags) - 1

    def get_tag(self, value: Real, mode: Literal['iter', 'binary'] = 'iter'):
        """
        获取某个位置的标签，支持遍历查找和二分查找。
        默认遍历查找，因为在数据量很小的时候，二分查找体现不出优势。

        :param value: 值
        :param mode: 遍历查找或二分查找，默认为 'iter'

        :return: 标签
        """

        assert isinstance(value, Real)

        # 遍历查找
        if mode == 'iter':
            for i, division in enumerate(self._divisions):
                if value < division:
                    return self._tags[i]
            return self._tags[-1]

        # 二分查找
        elif mode == 'binary':
            # 边界情况
            if value < self._divisions[0]:
                return self._tags[0]
            elif value >= self._divisions[-1]:
                return self._tags[-1]
            #
            left, right = 0, len(self._divisions) - 1  # 左闭右开
            while right - left > 1:
                mid = (left + right) >> 1
                if value < self._divisions[mid]:
                    right = mid
                else:
                    left = mid
            return self._tags[right]

        # 啥也不是
        else:
            raise ValueError(f'不支持的模式：{mode}')

    __getitem__ = get_tag  # 别名
    __call__ = get_tag  # 别名
