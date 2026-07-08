import random
from function.print_log import log


def make_asstes_house():
    house_no = "CS" + str(random.randint(100000, 999999))
    log.info(f'生成随机房号：{house_no}')
    return house_no





if __name__ == '__main__':
    make_asstes_house()