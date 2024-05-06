class ProgressFloat:
    """
    进度条类，应用于各种表示有最大上限值的正数。
    此类内部会维护好，让当前值在0到最大值之间变化。
    """

    def __init__(self, current_value: float, max_value: float):
        self.max_value = max_value
        if current_value > max_value:
            current_value = max_value
        elif current_value < 0:
            current_value = 0
        self.current_value = current_value

    def is_max(self) -> bool:
        """
        判断当前值是否达到最大值。
        """
        return self.current_value >= self.max_value

    def is_zero(self) -> bool:
        """
        判断当前值是否为0。
        """
        return self.current_value == 0

    @property
    def rate(self):
        """
        计算当前值占总值的比例。
        """
        return self.current_value / self.max_value

    def __add__(self, other: float) -> 'ProgressFloat':
        """
        实现加法运算，返回一个新的ProgressFloat对象。
        """
        new_value = self.current_value + other
        if new_value > self.max_value:
            new_value = self.max_value
        return ProgressFloat(new_value, self.max_value)

    def __sub__(self, other: float) -> 'ProgressFloat':
        """
        实现减法运算，返回一个新的ProgressFloat对象。
        """
        new_value = self.current_value - other
        if new_value < 0:
            new_value = 0
        return ProgressFloat(new_value, self.max_value)

    # 实现 <=
    def __le__(self, other: float) -> bool:
        return self.current_value <= other

    # 实现 >=
    def __ge__(self, other: float) -> bool:
        return self.current_value >= other

    # 实现 <
    def __lt__(self, other: float) -> bool:
        return self.current_value < other

    # 实现 >
    def __gt__(self, other: float) -> bool:
        return self.current_value > other

    # 实现 ==
    def __eq__(self, other: float) -> bool:
        return self.current_value == other

    # 实现!=
    def __ne__(self, other: float) -> bool:
        return self.current_value != other

    # 实现 str()
    def __str__(self) -> str:
        return f"{round(self.current_value, 1)}/{round(self.max_value, 1)}"
