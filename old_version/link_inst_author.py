# -*- coding:utf-8 -*-
# 机构作者 这个不需要时间

import csv
import json


def not_empty(s):
    return s and s.strip()


def get_link_hold():
    with open('../../data/middle_file/3.index/index_inst_author_dict.json', 'r',
              encoding='UTF-8') as file:
        index_text_index_dict = json.load(file)

    csv_write_path = '../../data/output/link/link_inst_author.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for text, institution_list in index_text_index_dict.items():
        for institution in institution_list:
            csv_write.writerow([int(text), institution])


if __name__ == '__main__':
    get_link_hold()
