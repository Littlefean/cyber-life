"""
测试磁盘IO性能
这里专门写一些占用磁盘IO资源的代码
"""
import os
from os import path


def diskio_burn(f_path: str, plan_size: int = 1024, block: int = 1):
    """
    测试磁盘IO性能

    :param f_path: 文件路径
    :param plan_size: 计划写入的大小，单位为 MB
    :param block: 写入的块大小，单位为 MB
    """

    # 写入文件

    tot_size = 0  # 总共写入的大小，单位位 MB
    once = b'0' * (block * 1024 * 1024)  # 每次都创建太浪费时间，所以事先准备好一个块数据

    with open(f_path, 'wb') as f:
        while tot_size + block <= plan_size:
            f.write(once)
            tot_size += block
            print(f'已写入 {tot_size} MB')
        f.write(b'0' * ((plan_size - tot_size) * 1024 * 1024))  # 最后一块数据写入文件
        print(f'已写入 {plan_size} MB')

    print()

    # 读取文件

    tot_size = 0  # 总共读取的大小，单位位 MB

    with open(f_path, 'rb') as f:
        while f.read(block * 1024 * 1024):
            tot_size += block
            print(f'已读取 {tot_size} MB')


if __name__ == '__main__':
    path = f'D:/【删除即可】一个被 {path.basename(__file__)} 创建的用于占用磁盘IO的文件，现在已无用'
    diskio_burn(path, 1024 * 10, 1024)
    os.remove(path)
