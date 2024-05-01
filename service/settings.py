from tools.singleton import SingletonMeta


class SettingsObject(metaclass=SingletonMeta):
    def __init__(self):
        # 是否显示小鱼
        self.is_fish_visible = True
        # 水草是否生长
        self.is_plant_growing = True
        # 设置水草增长速度
        self.plant_growth_speed = 100
        # 交换内存高度固定
        self.is_swap_memory_fixed = False
        self.swap_memory_height_rate = 0.125
        # 检测开关
        self.is_cpu_detectable = True
        self.is_disk_detectable = True
        self.is_memory_detectable = True
        self.is_network_detectable = True


SETTINGS = SettingsObject()
