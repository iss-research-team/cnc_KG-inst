# -*- coding:utf-8 -*-
# 机构持有专利/论文

import csv
import json


def not_empty(s):
    return s and s.strip()


def get_link_hold(label):
    with open('../../data/middle_file/3.index/index_text_inst_' + label + '.json', 'r',
              encoding='UTF-8') as file:
        index_text_index_dict = json.load(file)

    csv_write_path = '../../data/output/link/link_text_inst_' + label + '.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for text, inf in index_text_index_dict.items():
        institution_list = inf['institution']
        time = inf['time']
        for institution in institution_list:
            csv_write.writerow([int(text), institution, time])


if __name__ == '__main__':
    label = 'literature'
    # 把总的institution引进来
    get_link_hold(label)
