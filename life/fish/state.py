"""
这个代码中写鱼的各种状态
状态包括：

空闲状态
水面呼吸状态
睡眠状态
死亡状态

繁殖状态
寻找饲料状态
啃食水草状态
吞食幼崽状态

"""
import random

from life.fish.guppy_fish import GuppyFish
from life.tank import LIFE_TANK
from tools.vector import Vector


def tick_idle(fish: GuppyFish):
    """
    鱼处于空闲状态，不做任何事情，较小能量消耗
    :param fish:
    :return:
    """
    fish.speed = 0.1
    fish.o2_pre_request = 0.1
    fish.animation_interval = 10

    # 鱼游泳
    if fish.location_goal is None:
        fish.location_goal = fish.get_random_location()
    if fish.location.distance(fish.location_goal) < 10:
        new_goal = fish.get_random_location()
        fish.location_goal.x = new_goal.x
        fish.location_goal.y = new_goal.y
    fish.location += (fish.location_goal - fish.location).normalize() * fish.speed
    fish.breath()


def tick_surface(fish: GuppyFish):
    """
    在水中感觉缺少氧气，鱼会进入水面呼吸状态
    但这个模式的缺点是不能去水中觅食以及其他活动，只能在水面呼吸
    :param fish:
    :return:
    """
    fish.speed = 0.1
    fish.o2_pre_request = 0  # 因为呼吸的是水以外的氧气，所以这里是0
    fish.animation_interval = 5

    margin = 5  # 实际上是让鱼的中心与水面对齐，但再往下压一段距离，让鱼的头部与水面对齐
    head_y = fish.location.y - margin

    if head_y > LIFE_TANK.water_level_height:
        # 鱼还没到水面，往水面走
        fish.location.y -= 0.5
        fish.breath()
    elif head_y < LIFE_TANK.water_level_height:
        # 可能是因为水面突然下降，导致鱼悬在空中，所以鱼会回到水面
        fish.location.y = LIFE_TANK.water_level_height + margin
    else:
        # 鱼已经在水面上了，在水面上随机一个目标移动过去
        if fish.location.distance(fish.location_goal) < 50:
            fish.location_goal = Vector(random.randint(0, LIFE_TANK.width), fish.location.y)
        # 向水面上的目标移动
        fish.location += (fish.location_goal - fish.location).normalize() * fish.speed


def tick_sleep(fish: GuppyFish):
    """
    鱼睡眠状态，进入低功耗，增加精力的状态
    :param fish:
    :return:
    """
    # fish.speed = 0.1
    fish.o2_pre_request = 0.01
    fish.animation_interval = 20

    drag_down_distance = fish.height / 2 - 5  # 让鱼与地面接触

    # 判断当前是否沉底
    if fish.location.y + drag_down_distance < LIFE_TANK.sand_surface_height:
        # 还在水中，向下走
        fish.location.y += 0.5
    elif fish.location.y + drag_down_distance > LIFE_TANK.sand_surface_height:
        # 被埋了，回到陆地上
        fish.location.y = LIFE_TANK.sand_surface_height - drag_down_distance
    else:
        # 已经沉底，开始睡觉
        pass
    fish.breath()


def tick_death(fish: GuppyFish):
    """
    鱼死亡状态
    :param fish:
    :return:
    """
    fish.speed = 0
    fish.o2_pre_request = 0
    fish.animation_interval = 10

    # 尸体开始漂浮在水面上
    if fish.location.y > LIFE_TANK.water_level_height:
        # 在水里
        fish.velocity += Vector(0, -0.001)
    elif fish.location.y < LIFE_TANK.water_level_height:
        # 在水面以上
        fish.velocity += Vector(0, 0.01)
    else:
        # 已经浮到水面上，开始死亡动画
        pass
    fish.location += fish.velocity
