import random
from math import cos, sin


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
    """

    def __init__(self, x, y):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Vector components must be numerical")
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("unsupported operand type(s) for +: 'Vector' and '{}'".format(type(other).__name__))
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("unsupported operand type(s) for -: 'Vector' and '{}'".format(type(other).__name__))
        return Vector(self.x - other.x, self.y - other.y)

    def distance(self, other) -> float:
        return (self - other).__abs__()

    def limit(self, max_length):
        """
        将向量限制在最大长度范围内
        """

        if abs(self) > max_length:
            new_self = self.normalize() * max_length
            self.x = new_self.x
            self.y = new_self.y

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        else:
            raise TypeError("unsupported operand type(s) for *: 'Vector' and '{}'".format(type(other).__name__))

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    # 角度偏转
    def rotate(self, angle):
        """
        旋转向量
        :param angle: 单位：度
        """

        rad = angle * 3.141592653589793 / 180
        cos_val = round(cos(rad), 15)
        sin_val = round(sin(rad), 15)
        return Vector(self.x * cos_val - self.y * sin_val, self.x * sin_val + self.y * cos_val)

    @staticmethod
    def random():
        """获取一个随机单位长度向量"""
        return Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

    # 归一化
    def normalize(self):
        """
        将长度归一化，即变成单位向量
        """

        length = abs(self)
        if length == 0:
            return Vector(0, 0)
        return Vector(self.x / length, self.y / length)
