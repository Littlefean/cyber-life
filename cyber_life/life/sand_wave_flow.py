from math import inf
from typing import List

from PyQt5.QtGui import QPainter

from cyber_life.life.sand_wave import SandWave
from cyber_life.tools.compute import RangeDivider


class SandWaveFlow:
    """
    震荡波系列类，由tank类控制
    可以实例化为两种震荡波，分别向内和向外
    向外扩散的是写入磁盘的速度，向内扩散的是读取磁盘的速度
    """

    DISKIO_FREQ_RD = RangeDivider(
        (1, 4, 8, 12, 16, 20, 24, 28, 32),
        (inf, 100, 50, 40, 20, 15, 10, 6, 4, 2)
    )

    def __init__(self, x, wave_radius_speed):
        self.x = x
        self.sand_waves: List[SandWave] = []
        self.wave_radius_speed = wave_radius_speed

        # 波的周期（单位是帧），代表的是每多少帧产生一个波，最小值=2，表示最密集
        self.period = 10
        self.time = 0

    def tick(self):
        self.time += 1
        # 让每一个波都更新
        for sand_wave in self.sand_waves:
            sand_wave.tick()
        # 移除过期的波
        self.sand_waves = [sand_wave for sand_wave in self.sand_waves if not sand_wave.is_expired()]
        # 产生新的波
        if self.time % self.period == 0:
            if self.wave_radius_speed > 0:
                init_radius = 0
            else:
                init_radius = SandWave.MAX_RADIUS
            self.sand_waves.append(SandWave(self.x, init_radius, self.wave_radius_speed))

    def set_frequency_by_disk_io(self, io_bytes: int):
        """
        根据磁盘IO的频率设置波的周期
        """

        self.period = self.DISKIO_FREQ_RD[io_bytes.bit_length() - 1]  # bit_length() 相当于取对数

    def paint(self, painter: QPainter):
        for sand_wave in self.sand_waves:
            sand_wave.paint(painter)
