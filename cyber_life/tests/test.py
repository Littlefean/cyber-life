from cyber_life.computer_info import SYSTEM_INFO_MANAGER


def main():
    print(dir(SYSTEM_INFO_MANAGER))
    SYSTEM_INFO_MANAGER.start()
    while True:
        pass
    pass


if __name__ == '__main__':
    main()
