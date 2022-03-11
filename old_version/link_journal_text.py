# -*- coding:utf-8 -*-
# 机构持有专利/论文

import csv
import json


def get_link_journal_text():
    with open('../../data/middle_file/3.index/index_journal_text_dict.json', 'r', encoding='UTF-8') as file:
        index_journal_text_dict = json.load(file)

    csv_write_path = '../../data/output/link/link_journal_text.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for journal, text_list in index_journal_text_dict.items():
        for text in text_list:
            csv_write.writerow([int(journal), text])


if __name__ == '__main__':
    # 把总的institution引进来
    get_link_journal_text()
