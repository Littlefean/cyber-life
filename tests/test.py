from computer_info.manager import SYSTEM_INFO_MANAGER


def main():
    print(dir(SYSTEM_INFO_MANAGER))
    SYSTEM_INFO_MANAGER.start()
    while True:
        pass
    pass


if __name__ == '__main__':
    main()
