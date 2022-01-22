#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/7/16 上午11:22
# @Author  : liu yuhan
# @FileName: link_tp_text.py
# @Software: PyCharm


import csv
import json


def not_empty(s):
    return s and s.strip()


def get_link(label):
    csv_read_path = '../../data/input/tech_tree/tech_frequence_' + label + '.csv'
    csv_read = csv.reader(open(csv_read_path, 'r', encoding='UTF-8'))

    csv_write_path = '../../data/output/link/link_text_tp_' + label + '.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))

    # tp label
    with open('../../data/output/node/techpoint_label_dict.json', 'r', encoding='UTF-8') as file:
        techpoint_dict = json.load(file)

    # text label
    with open('../../data/output/node/text_label_dict_' + label + '.json', 'r', encoding='UTF-8') as file:
        text_dict = json.load(file)

    next(csv_read)

    for each_line in csv_read:
        csv_write.writerow([text_dict[each_line[0]], techpoint_dict[each_line[1]], each_line[2]])


if __name__ == '__main__':
    label = 'patent'
    # 把总的institution引进来
    get_link(label)
