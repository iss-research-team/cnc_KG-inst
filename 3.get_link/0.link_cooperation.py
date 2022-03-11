# -*- coding:utf-8 -*-

import csv
import json
import os
from tqdm import tqdm
from collections import Counter


def get_cooperation_author():
    link_file_path = '../data/middle_file/3.index/doc_author_dict.json'
    link_save_file_path = '../data/output/link/author_cooperation.csv'

    with open(link_file_path, 'r', encoding='UTF-8') as file:
        doc_author = json.load(file)
    link_dict = Counter()

    for _, author_list in tqdm(doc_author.items()):
        if len(author_list) < 2:
            continue
        author_list = sorted(author_list)
        for i in range(0, len(author_list) - 1):
            for j in range(i + 1, len(author_list)):
                link_dict[' | '.join([str(author_list[i]), str(author_list[j])])] += 1

    print('num of links:', len(link_dict))
    # 直接写csv，不写json了
    csv_write = csv.writer(open(link_save_file_path, 'w', encoding='UTF-8', newline=''))
    for link, weight in link_dict.items():
        csv_write.writerow([int(index) for index in link.split(' | ')] + [weight])


def get_cooperation_inst():
    link_file_path = '../data/middle_file/3.index/'
    link_save_file_path = '../data/output/link/inst_cooperation.csv'

    link_file_list = ['doc_literature_inst_dict.json',
                      'doc_patent_inst_dict.json']

    link_dict = Counter()

    for link_file in link_file_list:
        print('processing---', link_file)
        with open(os.path.join(link_file_path, link_file), 'r', encoding='UTF-8') as file:
            doc_inst = json.load(file)

        for _, inst_list in tqdm(doc_inst.items()):
            if len(inst_list) < 2:
                continue
            inst_list = sorted(inst_list)
            for i in range(0, len(inst_list) - 1):
                for j in range(i + 1, len(inst_list)):
                    link_dict[' | '.join([str(inst_list[i]), str(inst_list[j])])] += 1

    print('num of links:', len(link_dict))
    # 直接写csv，不写json了
    csv_write = csv.writer(open(link_save_file_path, 'w', encoding='UTF-8', newline=''))
    for link, weight in link_dict.items():
        csv_write.writerow([int(index) for index in link.split(' | ')] + [weight])


if __name__ == '__main__':
    # get_cooperation_author()
    get_cooperation_inst()
