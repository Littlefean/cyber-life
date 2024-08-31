"""
CPU性能测试
这里专门写一些非常吃性能的代码
"""

from multiprocessing import Process
from random import randint
from threading import Thread
from typing import Literal


def cpu_burn():
    arr = [randint(1, 1000000) for _ in range(1000000)]
    for i in range(1000000):
        for j in range(100000000):
            for k in range(100000000):
                arr[i] = randint(1, 1000000)


def main(method: Literal['process', 'thread'] = 'process', n: int = 10):
    """
    燃烧吧！CPU！

    :param method: 多线程还是多进程
    :param n: 进程数或线程数
    """
    if method == 'thread':
        print('CPU 多线程测试')
        threads = []
        for i in range(n):
            t = Thread(target=cpu_burn)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    elif method == 'process':
        print('CPU 多进程测试')
        processes = []
        for i in range(n):
            p = Process(target=cpu_burn)
            processes.append(p)
            p.start()
        for p in processes:
            p.join()

    else:
        raise ValueError('未知 method')


if __name__ == '__main__':
    main('process', 10)
