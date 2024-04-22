from tools.vector import Vector
from PyQt5.QtGui import QPainter, QPixmap, QTransform
from .tank import LIFE_TANK
from random import randint, uniform


class LifeFish:
    def __init__(self):
        # 鱼的位置坐标，其位置是贴图的中心点
        self.location = Vector(
            randint(30, LIFE_TANK.width - 30),
            randint(LIFE_TANK.water_level_height, LIFE_TANK.height - 30)
        )

        self.time = 0

        # 动画序列图
        self.img_list_swim_left = [QPixmap(f"assert/fish_{i}.png") for i in range(10)]

        self.img_list_swim_right = [
            QPixmap(f"assert/fish_{i}.png").transformed(QTransform().scale(-1, 1)) for i in range(10)
        ]

        # 当前游泳状态的动画 帧索引
        self.img_index_swim = 0
        # 大小就是图片的宽高
        self.width = 33
        self.height = 33
        # 移动的目标位置
        self.location_goal = self.get_random_location()
        # 移动速度
        self.speed = 0.1
        pass

    def tick(self):
        self.time += 1
        # 更新动画
        if self.time % 10 == 0:
            self.img_index_swim = (self.img_index_swim + 1) % 10
        # 鱼游泳
        if self.location_goal is None:
            self.location_goal = self.get_random_location()
        if self.location.distance(self.location_goal) < 10:
            print(f"""鱼{self.location}到达目标{self.location_goal}""")
            new_goal = self.get_random_location()
            self.location_goal.x = new_goal.x
            self.location_goal.y = new_goal.y
            print(f"""鱼{self.location}重新寻找目标""")
        self.location += (self.location_goal - self.location).normalize() * self.speed

    @staticmethod
    def get_random_location():
        try:
            x = uniform(30, LIFE_TANK.width - 30)
            y = uniform(LIFE_TANK.water_level_height + 30, LIFE_TANK.height - 30)
        except Exception as e:
            print(f"鱼无法找到合适的位置 {e}")
            return None
        return Vector(x, y)

    def is_face_to_left(self):
        """
        判断鱼面朝左边
        :return: bool
        """
        speed_vector = self.location_goal - self.location
        return speed_vector.x < 0

    def paint(self, painter: QPainter):
        # 判断鱼是否面向左边
        is_facing_left = self.is_face_to_left()
        if is_facing_left:
            pixmap = self.img_list_swim_left[self.img_index_swim]
        else:
            pixmap = self.img_list_swim_right[self.img_index_swim]
        painter.drawPixmap(
            round(self.location.x - self.width / 2),
            round(self.location.y - self.height / 2),
            pixmap
        )
