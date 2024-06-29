import sys
from plat.douyin_new import DouYin


def main():
    """ 主函数 """
    choice: int = int(input("请输入序号：\n\t1.抖音\n2.百度"))
    match choice:
        case 1:
            DouYin().run()
        case 2:
            pass


if __name__ == '__main__':
    main()