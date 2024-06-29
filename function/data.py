from dotenv import dotenv_values

config = dotenv_values("../.env")


class Data:
    baidu_url: str = config["BAIDU_URL"]
    douyin_url: str = config["DOUYIN_URL"]
    max_items: int = int(config["MAX_ITEMS"])
    pause: int = int(config['PAUSE'])

    tube: list[str] = []
    tiein: list[str] = []
    shrink: list[str] = []

    fifty_sleep: int = 10
    items_sleep: int = 20
    one_sleep: int = 7


if __name__ == '__main__':
    print(Data.baidu_url)
    print(Data.max_items)