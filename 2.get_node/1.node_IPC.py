# 需要导出额外的两个信息
# 机构作者信息，文本作者信息

import json
import re
import pandas as pd
from tqdm import tqdm
from collections import defaultdict


class IPC:
    def __init__(self, index_save_path, link_save_path_1, link_save_path_2):
        # 保存
        self.index_save_path = index_save_path
        self.ipc_doc_path = link_save_path_1
        self.ipc_tree_path = link_save_path_2

        self.doc_p2index = dict()
        self.get_index()
        # 存储
        # 这个地方需要获取父级
        self.index = 0
        self.ipc2index = dict()
        self.ipc_tree = defaultdict(set)
        self.ipc_doc = defaultdict(set)

    def get_index(self):
        with open('../data/output/node/doc_patent2index.json', 'r', encoding='UTF-8') as file:
            self.doc_p2index = json.load(file)

    def get_ipc_link(self):
        with open('../data/processed_file/relationship_dict_patent.json', 'r', encoding='utf-8') as file:
            literature_dict = json.load(file)

        for key, value in tqdm(literature_dict.items()):
            if not value['IPC']:
                continue
            doc_index = self.doc_p2index[key]
            ipc_list = value['IPC'].split(' | ')
            for ipc in ipc_list:
                ipc = ipc.replace(' (IPC 1-7)', '')
                if ipc not in self.ipc2index:
                    self.ipc2index[ipc] = self.index
                    self.index += 1
                self.ipc_doc[self.ipc2index[ipc]].add(doc_index)

    def get_ipc_tree(self):
        """
        构建ipc树
        :return:
        """

        def get_father(ipc, f, s):
            """
            :param ipc:
            :param f: father_bit
            :param s: son_bit
            :return:
            """
            ipc_f = ''
            if s == -1:
                # 对于第五级，大于c的所有的
                if len(ipc) > f:
                    ipc_f = ipc[:f]
            else:
                if len(ipc) == s:
                    ipc_f = ipc[:f]

            return ipc_f

        for f, s in [(8, -1), (4, 8), (3, 4), (1, 3)]:
            ipc2index_temper = self.ipc2index.copy()
            for ipc in ipc2index_temper:
                ipc_f = get_father(ipc, f=f, s=s)
                if not ipc_f:
                    continue
                if ipc_f not in self.ipc2index:
                    self.ipc2index[ipc_f] = self.index
                    self.index += 1
                self.ipc_tree[self.ipc2index[ipc_f]].add(self.ipc2index[ipc])
        print('num of ipc:', len(self.ipc2index))

    def save(self):
        def set2list(inf_dict):
            return dict((key, list(value_set)) for key, value_set in inf_dict.items())

        self.ipc_tree = set2list(self.ipc_tree)
        self.ipc_doc = set2list(self.ipc_doc)

        with open(self.index_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.ipc2index, file)
        with open(self.ipc_doc_path, 'w', encoding='UTF-8') as file:
            json.dump(self.ipc_doc, file)
        with open(self.ipc_tree_path, 'w', encoding='UTF-8') as file:
            json.dump(self.ipc_tree, file)


if __name__ == '__main__':
    index_save_path = '../data/output/node/ipc2index.json'
    link_save_path_1 = '../data/middle_file/3.index/ipc_doc_dict.json'
    link_save_path_2 = '../data/middle_file/3.index/ipc_tree_dict.json'

    ipc = IPC(index_save_path, link_save_path_1, link_save_path_2)
    ipc.get_ipc_link()
    ipc.get_ipc_tree()
    ipc.save()
