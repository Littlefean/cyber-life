import json

from cyber_life.tools.singleton import SingletonMeta


class SettingsObject(metaclass=SingletonMeta):
    def __init__(self):
        # 以下都是最初的默认值，后续用户可能会自定义修改
        self.is_fish_visible = True
        self.is_swap_memory_fixed = False
        self.swap_memory_height_rate = 0.125  # 1 / 8
        self.put_food_rate = 0.1  # 鼠标点击放置食物概率

    def save_to_json(self):
        with open('user_settings.json', 'w') as f:
            f.write(json.dumps(self.__dict__, indent=2))

    def load_from_json(self):
        def _load():
            with open('user_settings.json', 'r') as f:
                data = json.loads(f.read())
                self.__dict__.update(data)

        try:
            _load()
        except FileNotFoundError:
            # 可能是第一次运行，文件不存在
            self.save_to_json()
            _load()
        except json.JSONDecodeError:
            # 可能是被人修改了文件，内容不符合格式，重新覆盖保存
            self.save_to_json()
            _load()
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {e}")
            raise e


# 在被其它文件导入时执行
SETTINGS = SettingsObject()
SETTINGS.load_from_json()  # 导入设置
