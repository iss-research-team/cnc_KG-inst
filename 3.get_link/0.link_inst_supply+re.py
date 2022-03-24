# -*- coding:utf-8 -*-
import json
import csv
import re
from collections import defaultdict


def name_trans(inst_list):
    """
    去除无用的字符，小写
    :return:
    """
    # trans pattern
    pattern = re.compile("[.,']")
    inst_list_trans = []
    for inst in inst_list:
        inst_trans = pattern.sub('', inst)
        inst_list_trans.append(inst_trans.lower().strip())
    return inst_list_trans


def trans2label(inst_list_temper, inst2index):
    """
    转换为label
    :param inst_list_temper:
    :return:
    """
    return [inst2index[inst] for inst in inst_list_temper if inst in inst2index]


def get_supply():
    with open('../data/middle_file/2.4.inst_index/inst2index.json', 'r', encoding='UTF-8') as file:
        inst2index = json.load(file)

    link_list = []
    # 这为了后续的分析做准备
    inst_supply_dict = defaultdict(set)
    # 读文件
    file_path_dict = {'../data/input/supply_chain/company_link_1.json': 0,
                      '../data/input/supply_chain/company_link_3.json': 1}
    for file_path in file_path_dict:
        inst_list = json.load(open(file_path))['nodes']
        inst_link = json.load(open(file_path))['links']

        # 转换成label
        node_name_list = name_trans([inst['name'] for inst in inst_list])
        node_name_list = trans2label(node_name_list, inst2index)
        node_id_list = [inst['node_id'] for inst in inst_list]
        node_dict = dict(zip(node_id_list, node_name_list))

        for link in inst_link:
            if file_path_dict[file_path] == 0:
                link = [node_dict[link['source']], node_dict[link['target']]]
            else:
                link = [node_dict[link['target']], node_dict[link['source']]]
            link_list.append(link)
            inst_supply_dict[link[0]].add(link[1])

    # 这个地方为去重服务
    # 这里需要考虑的是加权重是否有意义
    # 目前来看权重是没有意义的
    link_list = [' | '.join([str(link[0]), str(link[1])]) for link in link_list]
    link_list = sorted(list(set(link_list)))

    def set2list(inf_dict):
        return dict((key, list(value_set)) for key, value_set in inf_dict.items())

    inst_supply_dict = set2list(inst_supply_dict)
    with open('../data/middle_file/3.index/inst_supply_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(inst_supply_dict, file)

    # 直接写csv，不写json了。
    csv_write_path = '../data/output/link/link_inst_supply.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for link in link_list:
        csv_write.writerow([int(index) for index in link.split(' | ')])

    print('供应链计数：', len(link_list))


def get_re():
    with open('../data/middle_file/2.4.inst_index/inst2index.json', 'r', encoding='UTF-8') as file:
        inst2index = json.load(file)

    link_list = []
    # 读文件
    file_path = '../data/input/supply_chain/company_link_2.json'
    inst_list = json.load(open(file_path))['nodes']
    inst_link = json.load(open(file_path))['links']

    # 转换成label
    node_name_list = name_trans([inst['name'] for inst in inst_list])
    node_name_list = trans2label(node_name_list, inst2index)
    node_id_list = [inst['node_id'] for inst in inst_list]
    node_dict = dict(zip(node_id_list, node_name_list))

    for link in inst_link:
        link = [node_dict[link['source']], node_dict[link['target']]]
        link_list.append(link)

    # 这个地方为去重服务
    # 这里需要考虑的是加权重是否有意义
    # 目前来看权重是没有意义的
    link_list = [' | '.join([str(link[0]), str(link[1])]) for link in link_list]
    link_list = sorted(list(set(link_list)))

    # 直接写csv，不写json了。
    csv_write_path = '../data/output/link/link_inst_re.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for link in link_list:
        csv_write.writerow([int(index) for index in link.split(' | ')])

    print('同比计数：', len(link_list))


if __name__ == '__main__':
    get_supply()
    get_re()
