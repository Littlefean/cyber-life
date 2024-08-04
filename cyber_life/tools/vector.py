from math import cos, sin, pi, hypot, dist, radians
from random import uniform


class Vector:
    """
    向量类，可以用于存放一个点的x、y坐标信息，可以当作向量并进行操作
    可以进行向量间的加减乘、判断相等、计算距离
    可以对向量取模、旋转、归一化
    GUI普遍以左上角为坐标原点
    坐标轴：
    ┌─────────► x
    │
    ▼
    y

    >>> Vector(1, 2)
    Vector(1, 2)
    >>> Vector(1, 2) + Vector(3, 4)
    Vector(4, 6)
    >>> Vector(1, 2) - Vector(3, 4)
    Vector(-2, -2)
    >>> Vector(1, 2) * 3
    Vector(3, 6)
    >>> Vector(1, 2) / 2
    Vector(0.5, 1.0)
    >>> Vector(1, 2) == Vector(1, 2)
    True
    >>> abs(Vector(3, 4))
    5.0
    >>> Vector(1, 2).distance(Vector(3, 4))
    2.8284271247461903
    >>> Vector(3, 4).limit(2)
    Vector(0.6, 0.8)
    >>> Vector(1, 2).rotate(90)
    Vector(-2.0, 1.0)
    >>> Vector(1, 1).normalize()
    Vector(0.7071067811865475, 0.7071067811865475)
    """

    __slots__ = ('x', 'y')

    def __init__(self, x: int | float = 0, y: int | float = 0):
        assert isinstance(x, (int, float)) and isinstance(y, (int, float))
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """ Return str(self). """
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        """ Return repr(self). """
        return f'{self.__class__.__name__}({self.x}, {self.y})'

    def __add__(self, other: 'Vector') -> 'Vector':
        """ Return self + other. """
        assert isinstance(other, Vector)
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector') -> 'Vector':
        """ Return self - other. """
        assert isinstance(other, Vector)
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int | float) -> 'Vector':
        """ Return self * other. """
        assert isinstance(other, (int, float))
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other: int | float) -> 'Vector':
        """ Return self / other. """
        assert isinstance(other, (int, float))
        return Vector(self.x / other, self.y / other)

    def __eq__(self, other):
        """ Return self == other. """
        return isinstance(other, Vector) and (self.x, self.y) == (other.x, other.y)

    def __abs__(self) -> float:
        """ Return abs(self). """
        return hypot(self.x, self.y)

    def distance(self, other: 'Vector') -> float:
        """
        两个向量之间的距离
        """

        assert isinstance(other, Vector)
        return dist((self.x, self.y), (other.x, other.y))

    def limit(self, max_length: int | float) -> 'Vector':
        """
        将向量限制在最大长度范围内
        """

        if abs(self) > max_length:
            new_self = (self * max_length).normalize()
            self.x, self.y = new_self.x, new_self.y

        return self

    # 角度偏转
    def rotate(self, angle):
        """
        旋转向量
        :param angle: 使用角度制
        """

        theta = radians(angle)  # 转化为弧度制

        cos_val = round(cos(theta), 15)
        sin_val = round(sin(theta), 15)

        return Vector(self.x * cos_val - self.y * sin_val, self.x * sin_val + self.y * cos_val)

    @classmethod
    def random(cls, length: int | float = 1):
        """
        一个方向随机的指定长度的向量
        """

        theta = uniform(0, pi * 2)
        return Vector(cos(theta) * length, sin(theta) * length)

    def normalize(self):
        """
        长度归一化，变成单位向量
        零向量保持不变
        """

        try:
            return self / abs(self)
        except ZeroDivisionError:
            return self
