"""
@Project: BaiDu Search Key
@Author: Amlei
@Email: lixiang.altr@qq.com
@FileNAme: baidu.py
"""

from pprint import pprint
from time import sleep
from function.data import Data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from function.key import save_csv_dict, baidu_key

# 搜索关键词
keyword: list[str] = ["管"]
# 存储全部数据
data: dict[list[str]] = {i: [] for i in keyword}

# 浏览器驱动
# driver = webdriver.Edge()
edge_options = Options()
edge_options.add_argument('--headless')
driver = webdriver.Edge(options=edge_options)
driver.get(Data.baidu_url)

# 单个关键字最大引申数量
max_items: int = 5000
current_num: int = 0
file_name: str = ""

def DFS(keyword: str, send_key: str) -> bool:
    """ 深度搜索
    
    Args:
        keyword (str): 源关键词
        send_key (str): 搜索关键词
    """
    global data, search_element, driver, current_num
    
    current_num += 1

    # 满足最大量退出
    if len(data[keyword]) > max_items:
        return False
    if len(data[keyword]) % 500 == 0:
        sleep(5)
    else:
        sleep(1.5)    
        
    search_element.clear()
    search_element.send_keys(send_key)
    baidu_key(keyword, send_key, data)
    
    # 使用深度搜索思想，模拟人点击提交按钮
    driver.find_element(By.ID, "su").click()
    
    # 在每一个深度搜索中加入广度搜索，定位相关搜索关键词
    # 所有的关键字最终都要汇总到 file 中
    other_key = driver.find_elements(By.CLASS_NAME, "rs-col_8Qlx-")
    data[keyword] += [i.text for i in other_key]
    
    
    print(f"{keyword}当前{len(data[keyword])}条\n\n")
    
    # 递归搜索
    DFS(keyword, data[keyword][current_num])

try:
    # 显示等待搜索框出现
    search_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "kw")))
        
    for i in keyword:
        file_name = i
        # 首次按照关键词搜索获取
        search_element.send_keys(i)
        baidu_key(i, i, data)
        driver.find_element(By.ID, "su").click()
        other_key = driver.find_elements(By.CLASS_NAME, "rs-col_8Qlx-")
        data[i] += [i.text for i in other_key]
        
        # 等待下一页,定位下一页按钮，开启广度搜索 -> 目前每页相关搜索内容均相同
        for item in data.values():
            sleep(2)
            
            if DFS(i, item[current_num]):
                current_num += 1
            else:
                pprint(data)
                print(f"当前{i}已有{max_items}条数据，开始下一个关键词")
                break
        
        # 保存文件
        save_csv_dict(data, i)
        print(f"--------------{i}文件保存完成------------------\n\n")
        # 当前数据清空，释放内存
        """存在问题， finally 会保存空的内容 在抖音中"""
        data[i] = []

except Exception as e:
    print(f"错误:{e}\n")
    
finally:
    print(data)
    save_csv_dict(data, file_name)
    input("按任意键退出")
