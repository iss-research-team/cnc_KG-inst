# -*- coding:utf-8 -*-

import csv
import json
from collections import Counter
from tqdm import tqdm


def not_empty(s):
    return s and s.strip()


def dict_trans(index_dict):
    index_dict_trans = dict()
    for node in index_dict:
        index_dict_trans[int(node)] = index_dict[node]
    return index_dict_trans


def get_citing(label):
    """
    根据text的引用生成inst的引用
    :param label:
    :return:
    """
    with open('../../data/middle_file/3.index/index_text_inst_' + label + '.json') as file:
        text_inst_dict = json.load(file)
    text_inst_dict = dict_trans(text_inst_dict)

    csv_read_path = '../../data/output/link/link_text_citing_' + label + '.csv'
    csv_read = csv.reader(open(csv_read_path, 'r', encoding='UTF-8'))

    csv_write_path = '../../data/output/link/link_inst_citing_' + label + '.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))

    link_list_count = Counter()
    for link in csv_read:
        s = int(link[0])
        t = int(link[1])
        try:
            s_list = text_inst_dict[s]['institution']
            t_list = text_inst_dict[t]['institution']
            time = text_inst_dict[s]['time']
        except KeyError:
            continue
        for inst_s in s_list:
            for inst_t in t_list:
                link_list_count[str(inst_s) + ' | ' + str(inst_t) + ' | ' + str(time)] += 1

    # 读取完成
    for link, weight in tqdm(link_list_count.items()):
        s, t, time = [int(inf) for inf in link.split(' | ')]
        csv_write.writerow([s, t, weight, time])


if __name__ == '__main__':
    label = 'literature'
    get_citing(label)
