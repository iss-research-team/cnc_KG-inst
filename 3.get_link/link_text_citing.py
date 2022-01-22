# -*- coding:utf-8 -*-

import csv
import json
from collections import Counter
from tqdm import tqdm


def not_empty(s):
    return s and s.strip()


def get_di_dict(text_relationship_dict, text_label_dict):
    di_dict = dict()
    for key, value in tqdm(text_relationship_dict.items()):
        text = text_label_dict[key]
        di = value.get('di', '')
        if di:
            di_dict[di] = text
    return di_dict


def get_citing(label):
    with open('../../data/processed_file/relationship_dict_' + label + '.json', 'r', encoding='UTF-8') as file:
        text_relationship_dict = json.load(file)
    with open('../../data/output/node/text_label_dict_' + label + '.json', 'r', encoding='UTF-8') as file:
        text_label_dict = json.load(file)

    text_citing_dict = dict()

    # 如果label是literature，建立一个di字典：
    di_dict = dict()
    if label == 'literature':
        di_dict = get_di_dict(text_relationship_dict, text_label_dict)

    for key, value in tqdm(text_relationship_dict.items()):
        text = text_label_dict[key]
        time = value['time']

        citing_label_list = []
        if label == 'literature' and value['citing']:
            if not value['citing']:
                continue
            citing_inf_list = value['citing'].split(';')
            for citing_inf in citing_inf_list:
                di = citing_inf.split(',')[-1]
                if ' DOI ' in di:
                    di = di.strip().split()[-1]
                    if di in di_dict:
                        citing_label_list.append(di_dict[di])
        if label == 'patent' and value['citing_patent']:
            if not value['citing_patent']:
                continue
            citing_inf = value['citing_patent'].split(' | ')
            citing_list_temper = [citing_inf[i * 9 + 1] for i in range(int(len(citing_inf) / 9))]
            citing_list_temper = list(filter(not_empty, citing_list_temper))
            for citing in citing_list_temper:
                if citing in text_label_dict:
                    citing_label_list.append(text_label_dict[citing])
        citing_label_list = sorted(list(set(citing_label_list)))
        if citing_label_list:
            text_citing_dict[text] = {'citing_label': citing_label_list,
                                      'time': time}

    print('index completed!')

    link_citing_dict = Counter()
    # 合并提权重
    for source, inf in tqdm(text_citing_dict.items()):
        target_list = inf['citing_label']
        time = inf['time']
        for target in target_list:
            link_citing_dict[' | '.join([str(source), str(target), str(time)])] += 1

    csv_write_path = '../../data/output/link/link_text_citing_' + label + '.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for link, weight in link_citing_dict.items():
        s, t, time = [int(inf) for inf in link.split(' | ')]
        csv_write.writerow([s, t, weight, time])

    print('合作计数：', len(link_citing_dict))


if __name__ == '__main__':
    label = 'patent'
    get_citing(label)
