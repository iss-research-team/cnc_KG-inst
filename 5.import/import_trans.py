#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/11 下午8:18
# @Author  : liu yuhan
# @FileName: import_trans.py
# @Software: PyCharm


import csv
import os
import json


def find_inst(inst_list):
    inst_list = sorted(inst_list, key=lambda x: len(x), reverse=True)
    return inst_list[0], '; '.join(inst_list[1:])


def node_trans_inst():
    node_path = '../data/middle_file/2.4.inst_index/index2inst.json'
    node_save_path = '../data/output/import/inst2index.csv'
    print('processing--- index2inst.json')

    with open(node_path, 'r', encoding='UTF-8') as file:
        node2index = json.load(file)
    csv_write = csv.writer(open(node_save_path, 'w', encoding='UTF-8'))

    head = ['InstId:ID', 'name', 'other_names', ':LABEL']
    csv_write.writerow(head)
    for index, inst_list in node2index.items():
        if len(inst_list) == 1:
            inst = inst_list[0]
            other_name = ''
        else:
            inst, other_name = find_inst(inst_list)

        csv_write.writerow(['Inst_' + index, inst, other_name, 'Inst'])


def node_trans(node_class_dict):
    node_path = '../data/output/node'
    node_save_path = '../data/output/import'

    for node_file, node_class in node_class_dict.items():
        print('processing---', node_file)

        with open(os.path.join(node_path, node_file), 'r', encoding='UTF-8') as file:
            node2index = json.load(file)
        csv_write = csv.writer(open(os.path.join(node_save_path, node_file.replace('json', 'csv')),
                                    'w', encoding='UTF-8'))
        head = [node_class + 'Id:ID', 'name', ':LABEL']
        csv_write.writerow(head)
        for node, index in node2index.items():
            csv_write.writerow([node_class + '_' + str(index), node, node_class])


def link_trans(link_role_dict):
    link_path = '../data/output/link'
    link_save_path = '../data/output/import'

    for link_file, link_role in link_role_dict.items():
        print('processing---', link_file)

        csv_read = csv.reader(open(os.path.join(link_path, link_file), 'r', encoding='UTF-8'))
        csv_write = csv.writer(open(os.path.join(link_save_path, link_file), 'w', encoding='UTF-8'))

        head = [':START_ID', ':END_ID', ':TYPE']
        csv_write.writerow(head)

        for source, target in csv_read:
            csv_write.writerow([link_role[0] + '_' + source, link_role[2] + '_' + target, '_'.join(link_role)])


def link_weight_trans(link_role_dict):
    link_path = '../data/output/link'
    link_save_path = '../data/output/import'

    for link_file, link_role in link_role_dict.items():
        print('processing---', link_file)

        csv_read = csv.reader(open(os.path.join(link_path, link_file), 'r', encoding='UTF-8'))
        csv_write = csv.writer(open(os.path.join(link_save_path, link_file), 'w', encoding='UTF-8'))

        head = [':START_ID', 'Weight', ':END_ID', ':TYPE']
        csv_write.writerow(head)

        for source, target, weight in csv_read:
            csv_write.writerow([link_role[0] + '_' + source, weight, link_role[2] + '_' + target, '_'.join(link_role)])


if __name__ == '__main__':
    with open('import_inf.json', 'r', encoding='UTF-8') as file:
        inf_dict = json.load(file)
    node_trans_inst()
    node_trans(inf_dict['node_class_dict'])
    link_trans(inf_dict['link_role_dict'])
    link_weight_trans(inf_dict['link_role_weight_dict'])
