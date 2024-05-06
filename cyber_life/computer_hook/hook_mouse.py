from functools import lru_cache

from pynput.mouse import Listener
from PIL import ImageGrab

from cyber_life.service.settings import SETTINGS
from cyber_life.tools.singleton import SingletonMeta
from random import random


class MouseHook(metaclass=SingletonMeta):
    def __init__(self):
        print("MouseHook init")
        self.is_hooked = False
        self._life_manager = None
        print("MouseHook init end")

        pass

    @property
    @lru_cache(1)
    def screen_width(self):
        im = ImageGrab.grab()
        print('截屏获取了一次宽度')
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
            cyber_x = x / self.screen_width * 300
            if 0 < cyber_x < 300 and random() < SETTINGS.put_food_rate:  # 点击后只有一定概率产生食物
                self.life_manager.add_food(cyber_x)

    def start(self):
        if self.is_hooked:
            return
        with Listener(on_click=self._on_click) as listener:
            listener.join()
            self.is_hooked = True

    def stop(self):
        pass
