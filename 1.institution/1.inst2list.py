#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/1/26
# @Author  : liu yuhan
# @FileName: inst2list.py
# @Software: PyCharm

import csv
import json
import re
import os

csv.field_size_limit(500 * 1024 * 1024)


def not_empty(s):
    return s and s.strip()


def get_institution_list(label):
    '''
    把institution提取出来
    :param label:
    :return:
    '''
    # 获取专利权人list
    institution_list = []

    if label == 'literature':
        # 为有人名的机构准备的正则表达式
        pattern = re.compile(r"\[(.*?)\]", re.S)
        # 读文件
        relationship_dict = json.load(open('../../data/processed_file/relationship_dict_' + label + '.json'
                                           , 'r', encoding='UTF-8'))
        for each_record in relationship_dict:
            if relationship_dict[each_record]['institution']:
                institution_list_temper = relationship_dict[each_record]['institution']
                # 去除人名
                institution_list_temper = re.sub(pattern, '', institution_list_temper)
                # 把第一项提出来
                institution_list_temper = [institution[:institution.index(',')].strip() for institution in
                                           institution_list_temper.split(';')]
                institution_list += institution_list_temper

    elif label == 'patent':
        # 读文件
        relationship_dict = json.load(open('../../data/processed_file/relationship_dict_' + label + '.json'
                                           , 'r', encoding='UTF-8'))
        for each_record in relationship_dict:
            institution_list_temper = relationship_dict[each_record]['institution'].split(' | ')
            institution_list += institution_list_temper

    elif label == 'supply':
        file_path = '../../data/input/supply_chain'
        file_list = os.listdir(file_path)
        for each_file in file_list:
            institution_list += json.load(open(os.path.join(file_path, each_file)))['nodes']
        institution_list = [node['name'] for node in institution_list]

    elif label == 'exhibition':
        key_dict = {'cimt_2019.json': '公司英文名称',
                    'cimt_2021.json': '公司英文名称',
                    'exhibitor_emo_2019.json': 'translate_name_en'}

        for file_name in key_dict:
            with open('../data/result/' + file_name, 'r', encoding='UTF-8') as file:
                inf_list = json.load(file)
            key = key_dict[file_name]
            for inf in inf_list:
                if key in inf:
                    institution_list.append(inf[key])

    # 去重 + 排序
    institution_list = sorted(list(set(institution_list)))
    institution_list = list(filter(not_empty, institution_list))
    print(label)
    print('总的专利权人数量：', len(institution_list))
    json.dump(institution_list, open('../../data/middle_file/institution_list_' + label + '.json',
                                     'w', encoding='UTF-8'))


if __name__ == '__main__':
    label = 'supply'
    get_institution_list(label)
