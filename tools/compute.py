def number_to_number(from_number, to_number, rate: float) -> float:
    """
    假设问题是从x轴上一个点走到另一个点，以及当前完成程度，
    返回当前的x坐标。
    :param from_number:
    :param to_number:
    :param rate:
    :return:
    """
    return (to_number - from_number) * rate + from_number
