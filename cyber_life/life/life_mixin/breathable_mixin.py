from cyber_life.life.gas_manager import GAS_MANAGER
from cyber_life.life.life_mixin.life import Life


class BreathableMixin(Life):
    """
    呼吸作用，当一个类继承了这个类，就拥有了呼吸的能力
    """

    def breath(self):
        """
        呼吸作用，O2 + C --> CO2 + 100能量
        这里是公式的简化
        :return:
        """
        # 一次呼吸作用需要的碳量和氧气量是一样的
        carbon_request = self.o2_pre_request
        if carbon_request > self.fixed_carbon:
            # 呼吸不了了，没有足够的碳，或许只能死了
            return
        if GAS_MANAGER.oxygen < self.o2_pre_request:
            # 没有足够的氧气
            return
        # 呼吸作用请求成功

        self.fixed_carbon -= carbon_request
        self.energy += self.o2_pre_request * 100
        GAS_MANAGER.reduce_oxygen(self.o2_pre_request)
        GAS_MANAGER.add_carbon_dioxide(self.o2_pre_request)
        pass
