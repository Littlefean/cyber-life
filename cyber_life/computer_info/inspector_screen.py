from random import randint

from PIL import ImageGrab

from .inspector_abc import Inspector


class InspectorScreen(Inspector):
    INSPECTION_INTERVAL = 5

    def __init__(self):
        super().__init__()
        self.screen_brightness = 0.0

    def get_current_result(self) -> float:
        return self.screen_brightness

    def inspect(self):
        # 因为发现休眠后会因为捕捉不到屏幕而报错，线程终止，无法更新系统信息
        try:
            im = ImageGrab.grab()
            width, height = im.size
            screen_brightness = 0.0
            for i in range(100):
                x = randint(0, width - 1)
                y = randint(0, height - 1)
                r, g, b = im.getpixel((x, y))
                screen_brightness += (r + g + b) / 3.0 / 255.0
            screen_brightness /= 100.0
            self.screen_brightness = screen_brightness
        except OSError:
            # 捕捉不到屏幕，屏幕亮度为0
            print("捕捉不到屏幕")
            self.screen_brightness = 0.0
