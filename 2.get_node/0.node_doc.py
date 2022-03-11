# -*- coding:utf-8 -*-

import csv
import json
import re
from tqdm import tqdm
from collections import defaultdict


def not_empty(s):
    return s and s.strip()


class Doc:
    def __init__(self, label, index_save_path, link_save_path):
        # trans pattern
        self.pattern = re.compile("[.,']")
        # 为有人名的机构准备的正则表达式
        self.pattern_remove_name = re.compile(r"[\[](.*?)[]]", re.S)
        self.label = label
        self.index_save_path = index_save_path
        self.link_save_path = link_save_path
        self.inst2index = dict()
        self.get_index()
        self.doc2index = dict()
        self.doc_inst = defaultdict(set)

    def get_index(self):
        with open('../data/middle_file/2.4.inst_index/inst2index.json', 'r', encoding='UTF-8') as file:
            self.inst2index = json.load(file)
        with open('../data/output/node/doc_literature2index.json', 'r', encoding='UTF-8') as file:
            self.doc_l2index = json.load(file)

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

    def trans2label(self, inst_list_temper):
        """
        转换为label
        :param inst_list_temper:
        :return:
        """
        return [self.inst2index[inst] for inst in inst_list_temper if inst in self.inst2index]

    def get_inst_list_patent(self, inst_inf, author_inf):
        """
        去除发明人
        :param inst_inf:
        :param author_inf:
        :return:
        """
        # 标准化的
        inst_list_1 = inst_inf['inst-dwpi'].split(' | ')
        author_list_1 = author_inf['author-dwpi'].split(' | ')
        # 原始的
        inst_list_2 = inst_inf['inst-original'].split(' | ')
        author_list_2 = author_inf['author-original'].split(' | ')

        inst_list_clean_1 = set(inst_list_1) - set(author_list_1)
        inst_list_clean_2 = set(inst_list_2) - set(author_list_2)
        inst_list_clean = list(inst_list_clean_1 | inst_list_clean_2)
        inst_list_clean = list(filter(not_empty, inst_list_clean))
        return self.name_trans(inst_list_clean)

    def get_inst_list_literature(self, inst_str):
        """
        :param inst_inf:
        :param author_inf:
        :return:
        """
        # 去除人名
        inst_str = re.sub(self.pattern_remove_name, '', inst_str)
        inst_list_temper = [inst[:inst.find(',')].strip() for inst in inst_str.split('; ')]
        inst_list_temper = list(filter(not_empty, inst_list_temper))
        return self.name_trans(inst_list_temper)

    def get_doc(self):
        with open('../data/processed_file/relationship_dict_' + self.label + '.json', 'r', encoding='UTF-8') as file:
            relationship_dict = json.load(file)
        index = 0
        for doc, value in tqdm(relationship_dict.items()):
            if doc not in self.doc2index:
                self.doc2index[doc] = index
                index += 1
            # 获取清单
            if self.label == 'patent':
                inst_list_temper = self.get_inst_list_patent(value['institution'], value['author'])
            elif self.label == 'literature':
                inst_list_temper = self.get_inst_list_literature(value['institution'])
            else:
                inst_list_temper = []
            if not inst_list_temper:
                continue
            # 转换成label
            inst_list_temper = self.trans2label(inst_list_temper)

            for inst in inst_list_temper:
                self.doc_inst[self.doc2index[doc]].add(inst)
        print('num of ' + label + ':', len(self.doc2index))

    def save(self):
        self.doc_inst = dict((doc, list(inst_set)) for doc, inst_set in self.doc_inst.items())

        with open(self.index_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.doc2index, file)
        with open(self.link_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.doc_inst, file)


if __name__ == '__main__':
    # label = 'patent'
    label = 'literature'
    index_save_path = '../data/output/node/doc_' + label + '2index.json'
    link_save_path = '../data/middle_file/3.index/doc_' + label + '_inst_dict.json'
    doc = Doc(label, index_save_path, link_save_path)
    doc.get_doc()
    doc.save()
