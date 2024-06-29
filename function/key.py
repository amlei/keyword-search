import os
import pandas as pd
import requests
from time import sleep


def baidu_search_keyword(datas: dict) -> list[str]:
    """ 搜索关键词

    Args:
        datas (dict): _description_

    Returns:
        list[str]: _description_
    """
    data: list[str] = []   
     
    for i in datas['g']:
        data.append(i['q'])
        
    return data


def baidu_key(source: str, q: str, data: dict[list[str]]) -> None:
    """ 关键字搜索
    Args:
        source (str): 原搜索关键字
        q (str): 最新搜索关键字
        data (dict[list[str]]): 数据集
        current_item (int): 当前类目条数
    """
    sleep(1.5)
    url: str = f"https://www.baidu.com/sugrec?pre=1&p=3&ie=utf-8&json=1&prod=pc&from=pc_web&&wd={q}"
    keyword = baidu_search_keyword(requests.get(url).json())
    data[source] += keyword
    sleep(1)


def save_csv_dict(data: dict, file_name: str, path: str) -> None:
    """ 将关键词保存进 CSV 文件

    Args:
        data (dict): _description_
        file_name (str): _description_
    """
    df = pd.DataFrame(data)

    df.drop_duplicates()
    df.to_csv(f"{path}{file_name}.csv", encoding="utf-8")


def save_csv_list(data: list[str], file_name: str, path: str, platform: str) -> None:
    """ 将关键词保存进 CSV 文件
    """
    df = pd.DataFrame(data)
    df.drop_duplicates()

    dir: str = path.split("/")[-1]

    if os.path.exists(f"../file/{dir}"):
        df.to_csv(f"{path}/{file_name}-{platform}.csv", encoding="utf-8")
    else:
        os.mkdir(f"../file/{dir}")
        df.to_csv(f"{path}/{file_name}-{platform}.csv", encoding="utf-8")

if __name__ == "__main__":

    sava_data = ['304不锈钢接头', '不锈钢万能转换头']

    save_csv_list(sava_data, "test")


    