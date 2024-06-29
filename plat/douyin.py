"""
@Project: DouYin Search Key
@Author: Amlei
@Email: lixiang.altr@qq.com
@FileNAme: douyin.py
"""

import json
import requests
from time import sleep
from pprint import pprint
from function.key import save_csv_dict, save_csv_list
from function.data import Data


def def_sleep(num: float, content: str) -> None:
    print(content)
    sleep(num)


class DouYin:
    """ 抖音 搜索关键词数据爬取"""

    def __init__(self, keywords: list[str], classify: str):
        # 以列表为搜索
        self.keyword: list[str] = keywords
        self.items: list[str] = []
        self.classify: str = classify
        self.current_num: int = 0

    def get(self, key: str) -> dict:
        """ 处理 get 请求
        Args:
            key: 搜索关键词

        Returns: get 返回的 json 数据
        """

        url: str = f"{Data.douyin_url}/aweme/v1/web/api/suggest_words/?query={key}&business_id=30125&aid=6383&app_name=douyin_web&pd=aweme_general&update_version_code=170400&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=126.0.0.0&browser_online=true&engine_name=Blink&engine_version=126.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7366419329670104586&msToken=p2Yl7EakUoJn5xpIcv-WEwkjNIpKqJ5cgElENFsvqbfE2T1ORjsptrjnhSuJ402cmiPMIuPvSXTjD_TcnkMxrIPRb9SOteZA1yruQULnuoipmWawZIWSIw==&a_bogus=Ev8M/mgvDiVivD6D5UALfY3q6VZ3YmCr0CPYMD2fvVfViy39HMTQ9exoJszv3SYjNs/DIebjy4haT3O2rQAnMpWUHuXLUdQ2sg8kKl5Q5xSSs1fee6m/rsJx5kGlFerM-JV3EcksqJKGKbYg09OJ4XFvPjoja3LkFk6FOosU"

        return requests.get(url).json()

    def append(self, content: dict) -> None:
        """ json 数据
        Args:
            content: get 请求的 json 数据

        Returns: None
        """
        for i in range(len(content['data'][0]['words'])):
            self.items.append(content['data'][0]['words'][i]['word'])

    def clear_items(self) -> None:
        """ 清空临时数据
        Returns: None
        """
        self.items = []
        self.current_num = 0

    def option_key(self, keyword: str, option: int = 0, last_keyword: str = None) -> str:
        """ 最近一次搜索关键词 -> 不必从头开始(可选)

        Args:
            keyword: 关键词
            option: 0, 读取  1, 写入
            last_keyword: 最近的关键词

        Returns:
        """
        ret: str = ""
        with open("../file/data.json", "r", encoding="utf-8") as f:
            data: dict = json.loads(f.read())

        match option:
            case 0:
                try:
                    ret = data[0]['Platform'][self.platform]['Last Keywords'][keyword]
                except:
                    # 当前 keyword 不存在时
                    pass
            case 1:
                if last_keyword:
                    with open("../file/data.json", "w", encoding="utf-8") as f:
                        data[0]['Last Keywords'][keyword] = last_keyword
                        json.dump(data, f, ensure_ascii=False, indent=4)
                else:
                    print("确保 last_keyword 参数存在才能进行写入操作")

        return ret

    def list_to_dict(self) -> dict:
        """ 列表转为字典索引

        Returns: 字典索引
        """
        return {i: j for i, j in enumerate(self.keyword)}

    def run(self) -> None:
        """ 运行函数
        Returns: None
        """
        file_name: str = ""
        try:
            # 对每个关键词进行抓取
            for i in self.keyword:
                file_name = i
                print(f"开始搜索【{i}】, 总量抓取:{Data.max_items}条")

                self.append(self.get(i))

                # 大于最大量停止
                while True:
                    if len(self.items) >= Data.max_items:
                        break
                    else:
                        self.append(self.get(self.items[self.current_num]))
                        self.current_num += 1

                        # 每 pause 条暂停时间长
                        if len(self.items) % Data.pause == 0:
                            def_sleep(Data.fifty_sleep, f"已增量抓取{len(self.items)}条，休眠{Data.fifty_sleep}秒")
                        else:
                            def_sleep(Data.one_sleep, f"第{len(self.items)}条")

                save_csv_list(self.items, file_name, path=f"../file/{self.classify}")

                # 列表清空
                self.clear_items()
                def_sleep(Data.items_sleep, "{:-<12}{}文件保存完成{:-<12}\n".format('-', i, '-'))

            print("{:-<12}{}{:-<12}\n".format('-', "本次搜索列表均搜索完毕", '-'))
        # except Exception as e:
        #     print(f"错误:{e}")

        finally:
            print(self.items)
            if self.items:
                save_csv_list(self.items, file_name, path=f"../file/{self.classify}")


if __name__ == '__main__':
    # DouYin(Data.tiein, "接头").run()

    content: str = DouYin(Data.tiein, "接头").option_key(keyword="接头", option=0)
    # content: str = Baidu(Data.tiein, "接头").last_key(keyword="接头", option=1, last_keyword="接头有哪些？")
    print(content)
