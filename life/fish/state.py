"""
这个代码中写鱼的各种状态
状态包括：

空闲状态
繁殖状态
睡眠状态
水面呼吸状态
死亡状态
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
