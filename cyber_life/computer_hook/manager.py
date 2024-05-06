"""
钩子管理器，管理所有钩子的运行
与监测器不同，钩子是根据不确定的动作做出不同的反应，
检测器只是以固定的时间间隔进行检测一个数值
"""
from threading import Thread

from .hook_mouse import MouseHook
from cyber_life.tools.singleton import SingletonMeta


class _SystemHookManager(metaclass=SingletonMeta):
    def __init__(self):
        self.mouse_hook = MouseHook()

        self.thread_list = [Thread(target=self.mouse_hook.start, daemon=True)]
        pass

    def start(self):
        # 开启所有钩子的监听
        for thread in self.thread_list:
            thread.start()
        pass

    def stop(self):
        # 暂不需要，因为 daemon=True 的线程会自动结束
        pass


SYSTEM_HOOK_MANAGER = _SystemHookManager()
