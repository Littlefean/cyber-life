from life.fish.guppy_fish import GuppyFish
from life.fish.state_enum import State
from life.life_manager import LifeManager


def get_best_state(fish: GuppyFish) -> State:
    """
    一个假的AI，手动写一些逻辑，不用复杂的算法实现
    :param fish:
    :return:
    """
    from life.tank import LIFE_TANK
    from life.gas_manager import GAS_MANAGER
    if fish.state == State.DEAD:
        return State.DEAD

    # 如果当前不是水面呼吸状态并且体内氧气少，进入水面呼吸状态
    if fish.oxygen_inner.rate < 0.2 and fish.state != State.SURFACE:
        return State.SURFACE
    # 如果当前是水面呼吸状态并且还没补充满体内氧气，则继续呼吸
    if fish.state == State.SURFACE and not fish.oxygen_inner.is_max():
        return State.SURFACE

    # 如果饿了，进食状态
    if fish.fixed_carbon < 500:
        return State.FIND_FOOD

    # 如果能量不足，进入睡眠状态，但需要保证能量相对充足之后再醒来。
    if fish.energy.rate < 0.2 and fish.state != State.SLEEP:
        return State.SLEEP
    if fish.state == State.SLEEP and fish.energy.rate < 0.8:
        return State.SLEEP

    # 看环境
    life_manager = LifeManager()
    if life_manager.is_food_in_water():
        return State.FIND_FOOD

    return State.IDLE

# idea：让鱼缸的各种环境信息作为输入，各种状态作为输出，形成一个神经网络
# 使用遗传算法调整神经网络里的参数。将神经网络里每个线性层的权重作为基因，进行遗传算法的变异、交叉、突变等操作，
# 通过遗传算法不停的繁殖迭代，以存活时间作为评价标准，选择出最优的鱼缸参数。

# 太累了，先不做了。
