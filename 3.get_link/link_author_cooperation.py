# -*- coding:utf-8 -*-

import csv
import json


def get_link_hold():
    with open('../../data/middle_file/3.index/index_text_author_dict.json', 'r',
              encoding='UTF-8') as file:
        index_text_index_dict = json.load(file)

    link_list = []

    for text, inst_list in index_text_index_dict.items():
        if len(inst_list) < 2:
            continue
        inst_list = sorted(inst_list)
        for i in range(0, len(inst_list) - 1):
            for j in range(i + 1, len(inst_list)):
                link_list.append([inst_list[i], inst_list[j]])

    print(len(link_list))

    # 这个地方为去重服务
    link_list = [' | '.join([str(link[0]), str(link[1])]) for link in link_list]

    # 字典去重
    link_cooperation_dict = dict()
    for link in link_list:
        if link not in link_cooperation_dict:
            link_cooperation_dict[link] = 1
        else:
            link_cooperation_dict[link] += 1

    # 直接写csv，不写json了。link_iterature.csv
    csv_write_path = '../../data/output/link/link_author_cooperation.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for link in link_cooperation_dict:
        csv_write.writerow([int(index) for index in link.split(' | ')] + [link_cooperation_dict[link]])


if __name__ == '__main__':
    get_link_hold()
