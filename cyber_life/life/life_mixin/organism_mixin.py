from cyber_life.life.gas_manager import GAS_MANAGER
from cyber_life.life.life_mixin.life import Life
from cyber_life.life.tank import LIFE_TANK


class OrganismMixin(Life):
    """
    光合作用，只要一个类继承了这个类，就能实现光合作用。
    """

    def photosynthesis(self):
        """
        光合作用 在一帧内完成
        在一帧内光合作用，CO2 --light_intensity--> O2 + C
        实际上光合作用有水的参与，这里就简化公式了。
        :return:
        """
        co2_cost = self.co2_pre_request * LIFE_TANK.light_brightness_current

        if GAS_MANAGER.carbon_dioxide < co2_cost:
            # 光合作用不了了，因为环境中没有足够的二氧化碳
            return

        GAS_MANAGER.reduce_carbon_dioxide(co2_cost)
        GAS_MANAGER.add_oxygen(co2_cost)  # 一份CO2产生一份氧气

        self.fixed_carbon += co2_cost  # 生物体内固定的碳增加
