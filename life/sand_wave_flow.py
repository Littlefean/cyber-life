from typing import List

from PyQt5.QtGui import QPainter

from life.sand_wave import SandWave


class SandWaveFlow:
    """
    震荡波系列类，由tank类控制
    可以实例化为两种震荡波，分别向内和向外
    向外扩散的是写入磁盘的速度，向内扩散的是读取磁盘的速度
    """
    def __init__(self, x, wave_radius_speed):
        self.x = x
        self.sand_waves: List[SandWave] = []
        self.wave_radius_speed = wave_radius_speed

        # 波的频率，但实际代表的是每多少帧产生一个波，最小值=2，表示最密集
        self.frequency = 10
        self.time = 0

    def tick(self):
        self.time += 1
        # 让每一个波都更新
        for sand_wave in self.sand_waves:
            sand_wave.tick()
        # 移除过期的波
        self.sand_waves = [sand_wave for sand_wave in self.sand_waves if not sand_wave.is_expired()]
        # 产生新的波
        if self.time % self.frequency == 0:
            if self.wave_radius_speed > 0:
                init_radius = 0
            else:
                init_radius = SandWave.MAX_RADIUS
            self.sand_waves.append(SandWave(self.x, init_radius, self.wave_radius_speed))

    def set_frequency_by_disk_io(self, io_bytes: int):
        """
        根据磁盘IO的频率设置波的频率
        :param io_bytes:
        :return:
        """
        if io_bytes == 0:
            self.frequency = 999999999
            return

        # io_bytes 这个数太大了，需要获得这个数字有多少位

        # 假设 io_bytes = 1000000000，则有 10 位
        import math
        count_of_digits = int(math.log10(io_bytes))
        if count_of_digits <= 1:
            self.frequency = 100
        elif count_of_digits <= 2:
            self.frequency = 50
        elif count_of_digits <= 3:
            self.frequency = 40
        elif count_of_digits <= 4:
            self.frequency = 20
        elif count_of_digits <= 5:
            self.frequency = 15
        elif count_of_digits <= 6:
            self.frequency = 10
        elif count_of_digits <= 7:
            self.frequency = 6
        elif count_of_digits <= 8:
            self.frequency = 4
        else:
            self.frequency = 2

    def paint(self, painter: QPainter):
        for sand_wave in self.sand_waves:
            sand_wave.paint(painter)
