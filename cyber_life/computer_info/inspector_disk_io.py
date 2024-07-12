import time

import psutil

from .inspector_abc import Inspector


class DiskIoResult:
    def __init__(self, read_bytes: int, write_bytes: int):
        self.read_bytes: int = read_bytes  # in KB
        self.write_bytes: int = write_bytes  # in KB


class InspectorDiskIO(Inspector):
    INSPECTION_INTERVAL = 0.4

    def get_current_result(self):
        return self.current_result

    def __init__(self):
        super().__init__()
        self.current_result = DiskIoResult(0, 0)

    def inspect(self):
        disk_io_first = psutil.disk_io_counters()
        time.sleep(0.5)
        disk_io_second = psutil.disk_io_counters()
        read_bytes = (disk_io_second.read_bytes - disk_io_first.read_bytes) / 1024
        write_bytes = (disk_io_second.write_bytes - disk_io_first.write_bytes) / 1024
        self.current_result = DiskIoResult(round(read_bytes), round(write_bytes))
