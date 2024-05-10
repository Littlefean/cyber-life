from enum import Enum, unique

"""
State 类，存放鱼的状体类型
unique 是 Enum 的类装饰器，如果有任何重复的枚举值，它会引发 ValueError
"""


@unique
class State(Enum):
    DEAD = 0

    IDLE = 1
    SURFACE = 2
    SLEEP = 3
    FIND_FOOD = 4
