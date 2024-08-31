from typing import List

import psutil

from .inspector_abc import Inspector


class InspectorCpu(Inspector):
    INSPECTION_INTERVAL = 0.1  # seconds

    def __init__(self):
        super().__init__()
        self.performance_percent_per_core = [0.0 for _ in range(psutil.cpu_count())]

    def inspect(self):
        new_cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
        for i in range(len(new_cpu_percent)):
            self.performance_percent_per_core[i] = new_cpu_percent[i] / 100.0

    def get_current_result(self) -> List[float]:
        return self.performance_percent_per_core
