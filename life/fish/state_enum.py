from enum import Enum, unique


@unique
class State(Enum):
    DEAD = 0

    IDLE = 1
    SURFACE = 2
    SLEEP = 3
