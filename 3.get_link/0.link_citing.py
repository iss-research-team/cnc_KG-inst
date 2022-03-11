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
    with open('../data/processed_file/relationship_dict_' + label + '.json', 'r', encoding='UTF-8') as file:
        relationship_dict = json.load(file)
    with open('../data/output/node/doc_' + label + '2index.json', 'r', encoding='UTF-8') as file:
        doc2index = json.load(file)
    with open('../data/middle_file/3.index/doc_' + label + '_inst_dict.json', 'r', encoding='UTF-8') as file:
        doc_inst = json.load(file)

    doc_citing_dict = dict()

    # 如果label是literature，建立一个di字典：
    di_dict = dict()
    if label == 'literature':
        di_dict = get_di_dict(relationship_dict, doc2index)

    for key, value in tqdm(relationship_dict.items()):
        citing_index_list = set()
        if label == 'literature' and value['citing']:
            if not value['citing']:
                continue
            citing_inf_list = value['citing'].split(';')
            for citing_inf in citing_inf_list:
                di = citing_inf.split(',')[-1]
                if ' DOI ' in di:
                    di = di.strip().split()[-1]
                    if di in di_dict:
                        citing_index_list.add(di_dict[di])
        if label == 'patent' and value['citing_patent']:
            if not value['citing_patent']:
                continue
            citing_inf = value['citing_patent'].split(' | ')
            citing_list_temper = [citing_inf[i * 9 + 1] for i in range(int(len(citing_inf) / 9))]
            citing_list_temper = list(filter(not_empty, citing_list_temper))
            for citing in citing_list_temper:
                if citing in doc2index:
                    citing_index_list.add(doc2index[citing])
        citing_index_list = sorted(list(citing_index_list))
        if citing_index_list:
            doc_citing_dict[doc2index[key]] = citing_index_list

    print('index completed!')

    csv_write_path = '../data/output/link/doc_citing_' + label + '.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    # 合并提权重
    for source, target_list in tqdm(doc_citing_dict.items()):
        for target in target_list:
            csv_write.writerow([source, target])

    link_inst_dict = Counter()
    # 合并提权重
    for source, target_list in tqdm(doc_citing_dict.items()):
        if str(source) not in doc_inst:
            continue
        inst_source_list = doc_inst[str(source)]
        inst_target_list = []
        for target in target_list:
            try:
                inst_target_list += doc_inst[str(target)]
            except KeyError:
                continue
        for i in inst_source_list:
            for j in inst_target_list:
                link_inst_dict[' | '.join([str(i), str(j)])] += 1

    print('num of links:', len(link_inst_dict))
    # 直接写csv，不写json了
    csv_write_path = '../data/output/link/inst_citing_' + label + '.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for link, weight in link_inst_dict.items():
        csv_write.writerow([int(index) for index in link.split(' | ')] + [weight])


if __name__ == '__main__':
    label = 'literature'
    get_citing(label)
