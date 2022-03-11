#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/7/13 上午10:32
# @Author  : liu yuhan
# @FileName: 4.inst_labeled.py
# @Software: PyCharm

"""
通过连通图的方式进行合并
"""

import json
from tqdm import tqdm
import networkx as nx


def inst_match():
    # 机构名字list

    index2inst = dict()
    inst2index = dict()

    inst_graph = nx.Graph()
    with open('../data/middle_file/2.2.inst_trans_dict/inst_list.json', 'r', encoding='UTF-8') as file:
        inst_list = json.load(file)
    inst_graph.add_nodes_from(inst_list)

    combine_list_patent_path = '../data/middle_file/2.0.inst_index_patent/combine_list_patent.json'
    combine_list_1_path = '../data/middle_file/2.3.combine/combine_list_equal_0.9.json'
    combine_list_2_path = '../data/middle_file/2.3.combine/combine_list_equal_0.9.json'

    with open(combine_list_patent_path, 'r', encoding='UTF-8') as file:
        combine_list_patent = json.load(file)
    with open(combine_list_1_path, 'r', encoding='UTF-8') as file:
        combine_list_1 = json.load(file)
    with open(combine_list_2_path, 'r', encoding='UTF-8') as file:
        combine_list_2 = json.load(file)

    inst_graph.add_edges_from(combine_list_patent + combine_list_1 + combine_list_2)

    for index, c in enumerate(nx.connected_components(inst_graph)):
        # 得到不连通的子集
        node_set = inst_graph.subgraph(c).nodes()
        index2inst[index] = list(node_set)
        for node in node_set:
            inst2index[node] = index
    print(len(index2inst))

    index2inst_save_path = '../data/middle_file/2.4.inst_index/index2inst.json'
    inst2index_save_path = '../data/middle_file/2.4.inst_index/inst2index.json'

    with open(index2inst_save_path, 'w', encoding='UTF-8') as file:
        json.dump(index2inst, file)
    with open(inst2index_save_path, 'w', encoding='UTF-8') as file:
        json.dump(inst2index, file)


if __name__ == '__main__':
    inst_match()
