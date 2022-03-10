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


class Inst:
    def __init__(self, label, save_path_json):
        """
        字典中保存的信息，dwpi的信息和orig的信息
        """
        self.label = label
        self.inst_list = []
        self.pattern = re.compile("[.,']")
        # 保存
        self.save_path_json = save_path_json

    def name_trans(self, inst_list):
        """
        去除无用的字符，小写
        :return:
        """
        inst_list_trans = []
        for inst in inst_list:
            inst_trans = self.pattern.sub('', inst)
            inst_list_trans.append(inst_trans.lower().strip())
        return list(set(inst_list_trans))

    def get_inst_list(self):
        """
        把inst提取出来
        :param label:
        :return:
        """
        if self.label == 'literature':
            self.get_inst_list_literature()
        elif self.label == 'supply':
            self.get_inst_list_supply()
        elif self.label == 'exhibition':
            self.get_inst_list_exhibition()
        else:
            raise ValueError(self.label + ' is not exist')

        # 企业名称转换
        self.inst_list = self.name_trans(self.inst_list)
        # 去重 + 排序
        self.inst_list = sorted(list(set(self.inst_list)))
        self.inst_list = list(filter(not_empty, self.inst_list))

        print(label)
        print('num of inst:', len(self.inst_list))
        json.dump(self.inst_list, open(self.save_path_json, 'w', encoding='UTF-8'))

    def get_inst_list_literature(self):
        """
        论文inst获取
        :return:
        """
        # 为有人名的机构准备的正则表达式
        pattern = re.compile(r"\[(.*?)\]", re.S)
        # 读文件
        relationship_dict = json.load(open('../data/processed_file/relationship_dict_' + label + '.json'
                                           , 'r', encoding='UTF-8'))
        for each_record in relationship_dict:
            if relationship_dict[each_record]['institution']:
                inst_list_temper = relationship_dict[each_record]['institution']
                # 去除人名
                inst_list_temper = re.sub(pattern, '', inst_list_temper)
                # 把第一项提出来
                inst_list_temper = [inst[:inst.index(',')].strip() for inst in inst_list_temper.split('; ')]
                self.inst_list += inst_list_temper

    def get_inst_list_supply(self):
        """
        供应链inst获取
        :return:
        """
        file_path = '../data/input/supply_chain'
        file_list = os.listdir(file_path)
        for each_file in file_list:
            self.inst_list += json.load(open(os.path.join(file_path, each_file)))['nodes']
        self.inst_list = [node['name'] for node in self.inst_list]

    def get_inst_list_exhibition(self):
        """
        展会inst获取
        :return:
        """
        key_dict = {'cimt_2019.json': '公司英文名称',
                    'cimt_2021.json': '公司英文名称',
                    'exhibitor_emo_2019.json': 'translate_name_en'}

        for file_name in key_dict:
            with open('../data/input/exhibition/' + file_name, 'r', encoding='UTF-8') as file:
                inf_list = json.load(file)
            key = key_dict[file_name]
            for inf in inf_list:
                if key in inf:
                    self.inst_list.append(inf[key])


if __name__ == '__main__':
    label = 'literature'
    save_path = '../data/middle_file/2.1.inst_list/inst_list_' + label + '.json'
    inst = Inst(label, save_path)
    inst.get_inst_list()
