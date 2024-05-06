"""
CPU性能测试
这里专门写一些非常吃性能的代码
"""
from threading import Thread
from multiprocessing import Process


def thread_func():
    from random import randint
    import time
    arr = [randint(1, 1000000) for _ in range(1000000)]
    for i in range(1000000):
        for j in range(100000000):
            for k in range(100000000):
                arr[i] = randint(1, 1000000)


def main():
    threads = []
    for i in range(10):
        t = Thread(target=thread_func)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    processes = []

    for i in range(10):
        p = Process(target=process_func)

        processes.append(p)

        p.start()

    for p in processes:
        p.join()


def process_func():
    from random import randint

    arr = [randint(1, 1000000) for _ in range(1000000)]

    for i in range(1000000):
        for j in range(100000000):
            for k in range(100000000):
                arr[i] = randint(1, 1000000)
    pass


if __name__ == '__main__':
    main()
