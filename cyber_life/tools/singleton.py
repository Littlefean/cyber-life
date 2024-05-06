class SingletonMeta(type):
    """
    单例元类，指定该元类作为metaclass的类
    只能实例化出同一个对象
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
