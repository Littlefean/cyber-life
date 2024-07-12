from functools import lru_cache
from random import random

from PIL import ImageGrab
from pynput.mouse import Listener

from cyber_life.service.settings import SETTINGS
from cyber_life.static import TANK_SCREEN_WIDTH
from cyber_life.tools.singleton import SingletonMeta


class MouseHook(metaclass=SingletonMeta):
    """
    监听鼠标行为
    鼠标点击可能会投喂食物
    """

    def __init__(self):
        self.is_hooked = False
        self._life_manager = None

    @property  # 变为只读属性，调用时不加 ()
    @lru_cache(1)  # 缓存装饰器，1表示只缓存最近1次的结果，如果与已缓存参数相同，直接返回缓存结果
    def screen_width(self):
        im = ImageGrab.grab()
        width, _ = im.size
        return width

    @property
    def life_manager(self):
        """
        将life_manager作为一个懒加载调用，避免启动过慢
        :return:
        """
        if not self._life_manager:
            from cyber_life.life.life_manager import LifeManager  # 避免循环导入
            self._life_manager = LifeManager()
        return self._life_manager

    def _on_click(self, x, y, button, pressed):
        if button == button.left and pressed:
            # 将鼠标相对于屏幕的x位置转换为相对于小鱼缸窗口的位置
            cyber_x = x / self.screen_width * TANK_SCREEN_WIDTH
            if 0 < cyber_x < TANK_SCREEN_WIDTH and random() < SETTINGS.put_food_rate:  # 点击后只有一定概率产生食物
                self.life_manager.add_food(cyber_x)  # 按鼠标相对屏幕位置映射食物在鱼缸中出现位置

    def start(self):
        if self.is_hooked:
            return
        with Listener(on_click=self._on_click) as listener:
            listener.join()
            self.is_hooked = True

    def stop(self):
        pass
