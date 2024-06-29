"""
@Project: BaiDu Search Key
@Author: Amlei
@Email: lixiang.altr@qq.com
@FileNAme: baidu.py
"""
import json
import requests
from plat.douyin_new import DouYin, def_sleep
from pprint import pprint
from function.data import Data
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from function.key import save_csv_list


class Baidu(DouYin):
    def __init__(self, keywords: list[str], classify: str):
        super().__init__(keywords, classify)

        self.search_element = None
        self.driver = webdriver.Edge(options=Options().add_argument('--headless'))
        self.driver.get(Data.baidu_url)
        self.platform: str = "百度"
        self.max_items: int = 5000
        self.flag: int = 0  # 标志偶数增量

    def run(self) -> None:
        """ 执行函数

        Returns: None

        """
        file_name: str = ""
        last_key: str = ""

        try:
            # 显示等待搜索框出现
            self.search_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "kw")))

            for i in self.keyword:
                file_name = i
                search_key: str = i
                # 按照最新的关键词数据更新，跳过已抓取的关键词 【待办】

                print(f"开始搜索【{i}】, 总量抓取不少于:{self.max_items}条")
                # last_key = self.option_key(keyword=file_name)

                # if last_key:
                    # 如果存在最新的搜索关键词，按照最新的搜索
                    # search_key = last_key

                self.search_element.send_keys(search_key)
                # 增加搜索框内的相关词
                self.search_key(search_key)
                sleep(2)

                # 页面底部相关搜索词
                self.driver.find_element(By.ID, "su").click()
                sleep(1)
                self.bottom_key()

                # 深度搜索
                if self.dfs(self.items[self.current_num]) is False:
                    # 保存文件
                    save_csv_list(self.items, file_name, path=f"../file/{self.classify}", platform=self.platform)
                    last_key = self.items[-1]
                    # 列表清空
                    self.clear_items()
                    def_sleep(Data.items_sleep, "{:-<12}{}文件保存完成{:-<12}\n".format('-', i, '-'))

                    continue

        finally:
            print(self.items)
            if self.items:
                save_csv_list(self.items, file_name, path=f"../file/{self.classify}",  platform=self.platform)

            # 不论是否异常，都要存储每个值最近的一个
            # self.option_key(keyword=file_name, last_keyword=last_key, option=1)

    def dfs(self, send_key: str) -> bool:
        """ 深度搜索
        Args:
            send_key: 搜索关键词
        Returns: Bool
        """
        self.current_num += 1

        # 满足最大量退出
        if len(self.items) > self.max_items:
            return False
        if len(self.items) % 2 == 0 and self.flag == 0:
            self.flag = 1
            def_sleep(5, f"已增量抓取{len(self.items)}条，休眠5秒")
        else:
            self.flag = 0
            def_sleep(1.5, f"第{len(self.items)}条")

        # 清楚搜索框内原有关键词，填入新搜索关键词，并添加新关键词的相关词
        self.search_element.clear()
        self.search_element.send_keys(send_key)
        sleep(1)
        self.search_key(send_key)

        # 使用深度搜索思想，模拟人点击提交按钮
        self.driver.find_element(By.ID, "su").click()
        self.bottom_key()

        # 递归搜索
        self.dfs(self.items[self.current_num])
        return True

    def get(self, key: str) -> dict:
        """ get 请求

        Args:
            key: 搜索关键词

        Returns: dict

        """
        url: str = f"{Data.baidu_url}/sugrec?pre=1&p=3&ie=utf-8&json=1&prod=pc&from=pc_web&&wd={key}"

        return requests.get(url).json()

    def append(self, content: dict) -> None:
        """ 增量更新

        Args:
            content: get 的数据

        Returns:

        """
        for i in content['g']:
            self.items.append(i['q'])

    def search_key(self, key: str) -> None:
        """ 搜索关键词存储

        Args:
            key: 关键词

        Returns: None

        """
        self.append(self.get(key))

    def bottom_key(self) -> None:
        """ 页面底部相关搜索词

        Returns: None

        """
        bottom_key = self.driver.find_elements(By.CLASS_NAME, "rs-col_8Qlx-")
        for j in bottom_key:
            self.items.append(j.text)




if __name__ == '__main__':
    Baidu(Data.tiein, "接头").run()
    # content: str = Baidu(Data.tiein, "接头").last_key(keyword="管", option=0)
    # content: str = Baidu(Data.tiein, "接头").last_key(keyword="接头", option=1, last_keyword="接头有哪些？")
    # print(content)