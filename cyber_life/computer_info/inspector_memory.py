import psutil
from .inspector_abc import Inspector


class MemoryInfo:
    def __init__(self, physical_memory_percent, physical_memory_total, swap_memory_percent, swap_memory_total):
        # 物理内存使用率，单位为百分比，[0, 1]
        self.physical_memory_percent = physical_memory_percent
        # 物理内存总量，单位为字节
        self.physical_memory_total = physical_memory_total
        # 交换内存使用率，单位为百分比，[0, 1]
        self.swap_memory_percent = swap_memory_percent
        # 交换内存总量，单位为字节
        self.swap_memory_total = swap_memory_total


class InspectorMemory(Inspector):
    INSPECTION_INTERVAL = 1

    def __init__(self):
        super().__init__()
        self.memory_info = MemoryInfo(0, 0, 0, 0)
        self.inspect()

    def inspect(self):
        self.memory_info = MemoryInfo(
            psutil.virtual_memory().percent / 100,
            psutil.virtual_memory().total,
            psutil.swap_memory().percent / 100,
            psutil.swap_memory().total
        )
        pass

    def get_current_result(self) -> MemoryInfo:
        return self.memory_info
