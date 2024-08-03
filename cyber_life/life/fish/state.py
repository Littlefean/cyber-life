"""
这个代码中写鱼的各种状态
状态包括：

死亡状态       ✓

空闲状态       ✓
水面呼吸状态   ✓
睡眠状态       ✓
寻找饲料状态   ✓

繁殖状态       ×
啃食水草状态   ×
吞食幼崽状态   ×
"""

from cyber_life.life.fish.guppy_fish import GuppyFish
from cyber_life.life.tank import LIFE_TANK
from cyber_life.tools.vector import Vector


def tick_death(fish: GuppyFish):
    """
    鱼死亡状态
    """

    fish.energy_pre_cost = 0
    fish.o2_pre_request = 0
    fish.animation_interval = 10
    fish.speed = 0

    # 尸体开始漂浮

    # 水面以下
    if fish.location.y > LIFE_TANK.division[0]:

        if fish.location.y + fish.height / 2 > LIFE_TANK.division[1]:
            fish.velocity.y = -abs(fish.velocity.y / 2)  # 碰了一下地面，速度大小减半

        fish.velocity += Vector(0, -0.001)  # 浮力的体现
        fish.velocity.limit(2)  # 阻力的体现

    # 水面以上
    elif fish.location.y < LIFE_TANK.division[0]:
        # 在水面以上
        fish.velocity += Vector(0, 0.01)

    fish.location += fish.velocity


def tick_idle(fish: GuppyFish):
    """
    鱼处于空闲状态，不做任何事情，较小能量消耗
    """

    fish.energy_pre_cost = 0.01
    fish.o2_pre_request = 0.1
    fish.animation_interval = 10
    fish.speed = 0.1

    # 防止鱼浮出水面和进入沙子
    fish.location.y = max(LIFE_TANK.division[0], min(LIFE_TANK.division[1], fish.location.y))

    # 先把目标位置更新一下，防止水面变化导致目标无法到达
    fish.location_goal.y = max(LIFE_TANK.division[0] + 30, min(LIFE_TANK.division[1] - 30, fish.location_goal.y))

    # 鱼随机游动
    if fish.location.distance(fish.location_goal) < 10:  # 已经到达目标，再开一个
        fish.location_goal = fish.get_random_location()

    fish.location += (fish.location_goal - fish.location).normalize() * fish.speed  # 向着目标移动


def tick_surface(fish: GuppyFish):
    """
    在水中感觉缺少氧气，鱼会进入水面呼吸状态
    但这个模式的缺点是不能去水中觅食以及其他活动，只能在水面呼吸
    """

    fish.energy_pre_cost = 0.02
    fish.o2_pre_request = 0.1
    fish.animation_interval = 5
    fish.speed = 0.1

    # 吸气
    fish.oxygen += 1

    margin = 5  # 实际上是让鱼的中心与水面对齐，但再往下压一段距离，让鱼的头部与水面对齐
    # 往上浮，但不能超过水面
    fish.location.y = max(LIFE_TANK.division[0] + margin, fish.location.y - 0.5)


def tick_sleep(fish: GuppyFish):
    """
    鱼睡眠状态，进入低功耗，增加精力的状态
    """

    fish.energy_pre_cost = 0.001
    fish.o2_pre_request = 0.01
    fish.animation_interval = 20
    fish.speed = 0

    drag_down_distance = fish.height / 2 - 5  # 鱼贴图中心与底部的距离

    # 下沉，但不能进入沙子
    fish.location.y = min(LIFE_TANK.division[1] - drag_down_distance, fish.location.y + 0.5)

    # 已经沉底，开始睡觉
    if fish.location.y == LIFE_TANK.division[1] - drag_down_distance:
        fish.energy += 1


def tick_find_food(fish: GuppyFish):
    """
    鱼寻找食物状态
    """

    fish.speed = 0.4
    fish.o2_pre_request = 0.2
    fish.animation_interval = 5
    fish.energy_pre_cost = 0.05

    from cyber_life.life.life_manager import LifeManager
    from cyber_life.life.food import Food

    # idea: 单例模式的用法没有很好的统一，food 的封装性可能有待改进

    life_manager = LifeManager()

    # 鱼不能浮出水面和进入沙子
    fish.location.y = max(LIFE_TANK.division[0], min(LIFE_TANK.division[1], fish.location.y))

    # 还没有目标，开始寻找目标
    if fish.target_food is None:
        # 水中有食物，确定一个作为目标
        if life_manager.is_food_in_water():
            food: Food = life_manager.choice_food_in_water()
            fish.location_goal = food.location
            fish.target_food = food
        # 无法找到食物，开始焦虑，随机设置一个目标并前进
        else:
            if fish.location.distance(fish.location_goal) > 10:
                fish.location_goal.y = max(LIFE_TANK.division[0] + 30,
                                           min(LIFE_TANK.division[1] - 30, fish.location_goal.y))
                fish.location += (fish.location_goal - fish.location).normalize() * fish.speed
            else:
                fish.location_goal = fish.get_random_location()

    # 已经有目标，开始前进
    else:
        # 向着目标前进
        if fish.location.distance(fish.target_food.location) > 10:
            fish.location += (fish.target_food.location - fish.location).normalize() * fish.speed
        # 已经到达目标，开始吃食物
        else:
            fish.carbon += fish.target_food.carbon
            fish.target_food.is_deleted = True
            fish.target_food = None
