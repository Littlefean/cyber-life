import psutil

from .inspector_abc import Inspector


class InspectorDiskUsage(Inspector):
    INSPECTION_INTERVAL = 10

    def __init__(self):
        super().__init__()
        self._current_result = 0.0

    def get_current_result(self) -> float:
        """
        获取当前的C盘使用率
        :return:
        """
        return self._current_result

    def inspect(self):
        try:
            # macos 没有C盘
            self._current_result = psutil.disk_usage('C:').percent / 100
        except Exception as e:
            print(f"Failed to inspect disk usage: {e}")
