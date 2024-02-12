from auto_api import AutoApi
from config import configs


def main():
    for conf in configs:
        a = AutoApi(conf)
        a.start()


if __name__ == "__main__":
    main()
