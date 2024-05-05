"""
钩子管理器，管理所有钩子的运行
与监测器不同，钩子是根据不确定的动作做出不同的反应，
检测器只是以固定的时间间隔进行检测一个数值
"""
import threading

from .hook_mouse import MouseHook
from tools.singleton import SingletonMeta


class _SystemHookManager(metaclass=SingletonMeta):
    def __init__(self):
        self.mouse_hook = MouseHook()
        pass

    def start(self):
        # 开启所有钩子的监听
        threading.Thread(target=self.mouse_hook.start).start()
        pass

    def stop(self):
        # 先不做，暂时用不到，后续有需求再改结构
        pass


print("system hook manager init")
SYSTEM_HOOK_MANAGER = _SystemHookManager()
print("system hook manager inited")
