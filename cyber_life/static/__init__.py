import sys
from os import path

# BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

PROJECT_DIR = path.abspath(path.dirname(sys.argv[0]))
TANK_SCREEN_WIDTH = 300

# 调试效果：
# 1. 水体颜色迅速变化
# 2. 贪吃蛇风格的移动动画加快
COLOR_DEBUG = True
