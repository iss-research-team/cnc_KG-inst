# -*- coding:utf-8 -*-
# 机构持有专利/论文

import csv
import json


def not_empty(s):
    return s and s.strip()


def get_link_inst_product():
    with open('../../data/middle_file/3.index/index_inst_product_dict.json', 'r', encoding='UTF-8') as file:
        index_inst_product_dict = json.load(file)
    csv_write_path = '../../data/output/link/link_inst_product.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for inst, product_list in index_inst_product_dict.items():
        for product in product_list:
            csv_write.writerow([int(inst), product])


def get_link_exhi_product():
    with open('../../data/middle_file/3.index/index_exhi_product_dict.json', 'r', encoding='UTF-8') as file:
        index_inst_product_dict = json.load(file)

    csv_write_path = '../../data/output/link/link_exhi_product.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for exhi, product_list in index_inst_product_dict.items():
        for product in product_list:
            csv_write.writerow([int(exhi), product])


if __name__ == '__main__':
    # 把总的institution引进来
    get_link_inst_product()
    get_link_exhi_product()
