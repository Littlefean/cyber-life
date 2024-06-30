"""
测试内存消耗
这里专门写一些非常占内存的代码
"""


def consume_memory(plan_size: int = 128, block: int = 16):
    """
    测试内存消耗
    :param plan_size: 预计分配的内存大小，单位为 MB
    :param block: 一次分配的内存块大小，单位为 MB
    """

    assert isinstance(plan_size, int) and plan_size > 0, 'plan_size must be a positive integer'
    assert isinstance(block, int) and block > 0, 'block must be a positive integer'

    try:
        data = []
        tot_size = 0  # 总共分配的内存，单位为 MB

        while tot_size + block <= plan_size:
            data.append(' ' * (1024 * 1024 * block))  # 一次分配 block MB 的内存
            tot_size += block
            print('%d MB allocated' % tot_size)

        data.append(' ' * (1024 * 1024 * (plan_size - tot_size)))  # 最后一次分配剩余的内存
        tot_size = plan_size
        print('%d MB allocated' % tot_size)

    except MemoryError:
        print('Memory is full.')

    except KeyboardInterrupt:
        print('Memory allocation stopped.')

    else:
        print('Memory allocation completed.')

    finally:
        input('Press Enter to exit...')


if __name__ == '__main__':
    consume_memory(1024 * 16, 1024)
