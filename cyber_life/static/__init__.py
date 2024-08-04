import sys
from os import path

# BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

PROJECT_DIR = path.abspath(path.dirname(sys.argv[0]))
TANK_SCREEN_WIDTH = 300

# 调试效果：
# 1. 水体颜色迅速变化
# 2. 贪吃蛇移动动画加快
# 3. 贪吃蛇颜色变化加快
COLOR_DEBUG = False

# 调试信息的格式
LOG_FORMAT = '%(asctime)s [%(levelname)8s] [%(name)s] %(message)s'
