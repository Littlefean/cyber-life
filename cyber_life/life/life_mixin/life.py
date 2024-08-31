from cyber_life.tools.progress_bar import ProgressFloat


class Life:
    def __init__(self):
        # 一开始的固定碳量
        self.carbon = 0.0
        # 一次光合作用请求量
        self.co2_pre_request = 0.0
        # 一次呼吸作用请求量
        self.o2_pre_request = 0.0
        # 能量，可以用于表示精力，睡眠可以更快速的增长能量
        self.energy = ProgressFloat(0, 1_0000)
