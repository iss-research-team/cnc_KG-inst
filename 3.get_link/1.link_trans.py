#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/10 下午8:37
# @Author  : liu yuhan
# @FileName: 1.link_trans.py
# @Software: PyCharm

import os
import json
import csv


def link_trans():
    link_file_path = '../data/middle_file/3.index'
    link_save_file_path = '../data/output/link'

    link_file_list = os.listdir(link_file_path)
    for link_file in link_file_list:
        print('processing---', link_file)
        with open(os.path.join(link_file_path, link_file), 'r', encoding='UTF-8') as file:
            link_dict = json.load(file)
        csv_write = csv.writer(open(os.path.join(link_save_file_path, link_file.replace('.json', '.csv')),
                                    'w', encoding='UTF-8'))
        for source, target_list in link_dict.items():
            source = int(source)
            for target in target_list:
                csv_write.writerow([source, target])


if __name__ == '__main__':
    link_trans()
