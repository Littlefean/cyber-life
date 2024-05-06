from cyber_life.tools.singleton import SingletonMeta


class GasManager(metaclass=SingletonMeta):
    """
    气体在水中的溶解度通常用mg/L表示，毫克/升表示
    如果水温增高，溶解氧量会降低，因为热水不如冷水能有效保持氧气。

    ```
    溶解氧通常在 6-9 mg/L
    自然水体中的CO₂浓度通常低于10 mg/L
    通常情况下，每克鱼体重每小时大约需要1毫克氧气。
    ...内容作废，直接先用最简单的数字表示氧气含量。
    ```
    """

    def __init__(self):
        # 水中氧气含量
        self.oxygen = 1000
        # 水中二氧化碳含量
        self.carbon_dioxide = 1000

    def add_oxygen(self, amount):
        self.oxygen += amount

    def add_carbon_dioxide(self, amount):
        self.carbon_dioxide += amount

    def reduce_oxygen(self, amount):
        self.oxygen -= amount

    def reduce_carbon_dioxide(self, amount):
        self.carbon_dioxide -= amount

    def photosynthesis_tick(self, carbon_request_amount: float, light_intensity: float) -> float:
        """
        在一帧内光合作用，CO2 --light_intensity--> O2 + C
        实际上光合作用有水的参与，这里就简化公式了。
        :param light_intensity: 光照强度，实际上可以代表转换率
        :param carbon_request_amount: 一帧内的消耗二氧化碳的请求使用量
        :return: 这个光合作用中固定了多少碳元素
        """
        carbon_cost = carbon_request_amount * light_intensity
        if self.carbon_dioxide < carbon_cost:
            return 0
        self.reduce_carbon_dioxide(carbon_cost)
        self.add_oxygen(carbon_cost)
        return carbon_cost

    # 呼吸作用
    def respiration_tick(self, oxygen_request_amount: float, carbon_request_amount: float) -> float:
        """
        呼吸作用，O2 + C --> CO2 + 100能量
        :param carbon_request_amount: 一帧内的自身碳的消耗量请求
        :param oxygen_request_amount: 一帧内的消耗氧气的请求使用量
        :return: 这个呼吸作用中固定了多少氧气
        """
        if oxygen_request_amount != carbon_request_amount:
            # 暂时不考虑无氧呼吸情况
            raise ValueError("Oxygen and carbon request amount must be equal.")

        if self.oxygen < oxygen_request_amount:
            return 0
        self.reduce_oxygen(oxygen_request_amount)
        self.add_carbon_dioxide(oxygen_request_amount)
        return 100 * oxygen_request_amount


GAS_MANAGER = GasManager()
