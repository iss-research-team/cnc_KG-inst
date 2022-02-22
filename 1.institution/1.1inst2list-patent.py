#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/27 上午9:55
# @Author  : liu yuhan
# @FileName: 1.1inst2list-patent.py
# @Software: PyCharm

# 由于专利的特殊性，这里单独对专利进行处理

import csv
import json
import re
import networkx as nx

csv.field_size_limit(500 * 1024 * 1024)


def not_empty(s):
    return s and s.strip()


class Inst4Patent:
    def __init__(self, save_path_json, save_path_csv):
        """
        字典中保存的信息，dwpi的信息和orig的信息
        """
        self.inst_dict = dict()
        self.inst2index = dict()
        # self.link_list = []
        self.pattern = re.compile("[.,']")

        # 图需要提前建好
        self.inst_graph = nx.Graph()
        self.inst_dwpi_set = set()

        # 这个为第三次检索做准备
        self.rest_collect = []

        self.save_path_json = save_path_json
        self.save_path_csv = save_path_csv

    def name_trans(self, inst_list, tage):
        """
        去除无用的字符，小写
        :return:
        """
        inst_list_trans = []
        for inst in inst_list:
            inst_trans = self.pattern.sub('', inst)
            inst_list_trans.append(inst_trans.lower() + tage)
        return list(set(inst_list_trans))

    def sub_author(self, inst_inf, author_inf):
        """
        去除发明人
        :param inst_inf:
        :param author_inf:
        :return:
        """
        # 标准化的
        inst_list_1 = inst_inf['inst-dwpi'].split(' | ')
        author_list_1 = author_inf['author-dwpi'].split(' | ')
        inst_list_clean_1 = list(set(inst_list_1) - set(author_list_1))
        inst_list_clean_1 = list(filter(not_empty, inst_list_clean_1))

        # 原始的
        inst_list_2 = inst_inf['inst-original'].split(' | ')
        author_list_2 = author_inf['author-original'].split(' | ')
        inst_list_clean_2 = list(set(inst_list_2) - set(author_list_2))
        inst_list_clean_2 = list(filter(not_empty, inst_list_clean_2))
        return self.name_trans(inst_list_clean_1, ' --dwpi'), \
               self.name_trans(inst_list_clean_2, ' --orig')

    def index_inst(self):
        # 通过联通子图合并机构
        for index, c in enumerate(nx.connected_components(self.inst_graph)):
            # 得到不连通的子集
            node_set = self.inst_graph.subgraph(c).nodes()
            inst_dwpi_set_temper = set()
            inst_orig_set_temper = set()
            for node in node_set:
                if node in self.inst_dwpi_set:
                    inst_dwpi_set_temper.add(node)
                else:
                    inst_orig_set_temper.add(node)
            self.inst_dict[index] = {'dwpi': inst_dwpi_set_temper,
                                     'orig': inst_orig_set_temper}
        print(len(self.inst_dict))

    def inst_index(self):
        for index, inst_inf in self.inst_dict.items():
            for inst in inst_inf['dwpi']:
                self.inst2index[inst] = index
            for inst in inst_inf['orig']:
                self.inst2index[inst] = index

    def get_inst_first_time(self):
        """
        第一阶段，只提取节点不提取关系
        通过最大联通图的方式合并企业

        是最简单的部分，但是可以处理接近90的专利

        :return:
        """
        # 读文件
        relationship_dict = json.load(open('../data/processed_file/relationship_dict_patent.json',
                                           'r', encoding='UTF-8'))

        for each_record in relationship_dict:
            inst_inf = relationship_dict[each_record]['institution']
            author_inf = relationship_dict[each_record]['author']
            # 去除发明人
            inst_list_clean_1, inst_list_clean_2 = self.sub_author(inst_inf, author_inf)

            if not inst_list_clean_1:
                # 去除了专利权人是发明人的情况
                continue
            # 第一次捞取
            # 这个地方有一个逻辑是只有一个dwpi和一个orig时，二者是对应的

            if len(inst_list_clean_1) == 1 and len(inst_list_clean_2) <= 1:
                inst_dwpi = inst_list_clean_1[0]
                self.inst_graph.add_node(inst_dwpi)
                # 节点分类
                self.inst_dwpi_set.add(inst_dwpi)
                if len(inst_list_clean_2) == 1:
                    inst_orig = inst_list_clean_2[0]
                    self.inst_graph.add_node(inst_orig)
                    self.inst_graph.add_edge(inst_dwpi, inst_orig)

        # 索引转换
        self.index_inst()
        self.inst_index()

    def second_inst_remove(self, inst_list_1, inst_list_2):
        inst_list_1_remove, inst_list_2_remove = inst_list_1.copy(), inst_list_2.copy()
        for inst in inst_list_1:
            if inst in self.inst2index:
                inst_list_1_remove.remove(inst)
                inst_orig_list_temper = list(self.inst_dict[self.inst2index[inst]]['orig'])
                for inst_orig in inst_orig_list_temper:
                    try:
                        inst_list_2_remove.remove(inst_orig)
                    except ValueError:
                        continue

        return inst_list_1_remove, inst_list_2_remove

    def get_inst_second_time(self):
        """
        这是机构获取的第二个阶段
        这个过程进行一次完整的获取
        可以处理的加入字典，不能处理的写入一个新的list等待处理
        :return:
        """
        # 读文件
        relationship_dict = json.load(open('../data/processed_file/relationship_dict_patent.json',
                                           'r', encoding='UTF-8'))

        for each_record in relationship_dict:
            inst_inf = relationship_dict[each_record]['institution']
            author_inf = relationship_dict[each_record]['author']
            # 去除发明人
            inst_list_clean_1, inst_list_clean_2 = self.sub_author(inst_inf, author_inf)
            if len(inst_list_clean_1) <= 1:
                continue
            # 第二次捞取
            inst_list_clean_1, inst_list_clean_2 = self.second_inst_remove(inst_list_clean_1, inst_list_clean_2)
            if len(inst_list_clean_1) == 1 and len(inst_list_clean_2) <= 1:
                inst_dwpi = inst_list_clean_1[0]
                self.inst_graph.add_node(inst_dwpi)
                # 节点分类
                self.inst_dwpi_set.add(inst_dwpi)
                if len(inst_list_clean_2) == 1:
                    inst_orig = inst_list_clean_2[0]
                    self.inst_graph.add_node(inst_orig)
                    self.inst_graph.add_edge(inst_dwpi, inst_orig)
            else:
                self.rest_collect.append([inst_list_clean_1, inst_list_clean_2])

        # 索引转换
        self.index_inst()
        self.inst_index()

    def get_inst_third_time(self):
        """
        这是机构获取的最后一个阶段
        这个过程进行多次循环进行最后的获取
        :return:
        """
        # 读文件
        while True:
            rest_collect = self.rest_collect.copy()
            self.rest_collect = []
            for inst_list_clean_1, inst_list_clean_2 in rest_collect:

                # 第二次捞取
                inst_list_clean_1, inst_list_clean_2 = self.second_inst_remove(inst_list_clean_1, inst_list_clean_2)
                if len(inst_list_clean_1) == 1 and len(inst_list_clean_2) <= 1:
                    inst_dwpi = inst_list_clean_1[0]
                    self.inst_graph.add_node(inst_dwpi)
                    # 节点分类
                    self.inst_dwpi_set.add(inst_dwpi)
                    if len(inst_list_clean_2) == 1:
                        inst_orig = inst_list_clean_2[0]
                        self.inst_graph.add_node(inst_orig)
                        self.inst_graph.add_edge(inst_dwpi, inst_orig)
                else:
                    self.rest_collect.append([inst_list_clean_1, inst_list_clean_2])

            # 索引转换
            self.index_inst()
            self.inst_index()
            if self.rest_collect == rest_collect:
                break

    def get_inst_forth_time(self):
        """
        事实上这是节点提取的最后一个阶段
        :return:
        """
        rest_collect = self.rest_collect.copy()
        self.rest_collect = []
        for inst_list_clean_1, inst_list_clean_2 in rest_collect:
            inst_dict_clean_1 = dict(zip([inst.replace(' --dwpi', '', -1) for inst in inst_list_clean_1],
                                         inst_list_clean_1))
            inst_dict_clean_2 = dict(zip([inst.replace(' --orig', '', -1) for inst in inst_list_clean_2],
                                         inst_list_clean_2))

            # 把两个list中同名的企业拿出来
            inst_list_common = list(set(inst_dict_clean_1.keys()) & set(inst_dict_clean_2.keys()))
            if inst_list_common:
                for node in inst_list_common:
                    self.inst_graph.add_node(inst_dict_clean_1[node])
                    self.inst_graph.add_node(inst_dict_clean_2[node])

                    inst_list_clean_1.remove(inst_dict_clean_1[node])
                    inst_list_clean_2.remove(inst_dict_clean_2[node])
            else:
                if inst_list_clean_1:
                    self.rest_collect.append([inst_list_clean_1, inst_list_clean_2])

        # 索引转换
        self.index_inst()
        self.inst_index()

    def rest_output(self):
        csv_write = csv.writer(open(rest_path_csv, 'w', encoding='UTF-8', newline=''))

        for _ in self.rest_collect:
            csv_write.writerow(_[0] + [''] + _[1])

    def index_save(self):
        """
        用于保存生成的index_dict
        :return:
        """
        # with open(self.save_path_json, 'w', encoding="UTF-8") as file:
        #     json.dump(self.inst_dict, file)
        csv_write = csv.writer(open(self.save_path_csv, 'w', encoding='UTF-8', newline=''))
        for index, inst_inf in self.inst_dict.items():
            csv_write.writerow([index] + list(inst_inf['dwpi']) + ['  |  '] + list(inst_inf['orig']))

    # for inst, orig in self.inst_dict.items():
    #     if len(orig) > 1:
    #         print(inst, orig)

    #     # 2. 去除母公司
    #
    #     # 需要判断一下有多少是不一样的inst_p，inst_a
    #     if inst_a != inst_p:
    #         # 这是一个坑
    #         continue
    #     # 当前公司，母公司，原始都只有一个
    #     if ' | ' in inst_p:
    #         continue
    #     if inst_p in inst_list_clean_1 and len(inst_list_clean_1) > 1:
    #         inst_list_clean_1.remove(inst_p)
    #
    #     if len(inst_list_clean_1) != len(inst_list_clean_2):
    #         count += 1
    #         print('dwpi', inst_list_clean_1)
    #         print(inst_inf)
    #         print(author_inf)
    #         print('orig', inst_list_clean_2)
    # print(count)
    # # 这里要找的是一一对应的关系，并将其加入字典
    # # 标准化-母公司-原始
    # if len(inst_list_clean) == 1:
    #
    # print(inst_inf)
    # print(inst_list)
    # print(inst_list_clean)
    # if inst_inf['inst-standard'] and inst_inf['inst-standard'] in inst_dict:
    #     continue
    # if ' | ' in inst_inf['inst-standard']:
    #     continue
    # inst = inst_inf['inst-standard']
    # if inst_inf['inst-adv'] != inst_inf['inst-parent']:
    #     continue
    # inst_parent = inst_inf['inst-adv']
    # inst_orig = inst_inf['inst-original']
    # inst_dict[inst] = {'orig': inst_orig,
    #                    'parent': inst_parent, }

    # print(inst_dict)
    # print(len(inst_dict))
    # # 去重 + 排序
    # institution_list = sorted(list(set(institution_list)))
    # # 去空
    # institution_list = list(filter(not_empty, institution_list))
    # print(label)
    # print('总的专利权人数量：', len(institution_list))
    # json.dump(institution_list, open('../../data/middle_file/institution_list_' + label + '.json',
    #                                  'w', encoding='UTF-8'))


if __name__ == '__main__':
    save_path_json = '../data/middle_file/2.1.inst_index/inst_patent.json'
    save_path_csv = '../data/middle_file/2.1.inst_index/inst_patent.csv'
    rest_path_csv = '../data/middle_file/2.1.inst_index/inst_rest_patent.csv'

    inst = Inst4Patent(save_path_json, save_path_csv)
    inst.get_inst_first_time()
    inst.get_inst_second_time()
    inst.get_inst_third_time()
    inst.get_inst_forth_time()
    inst.rest_output()
    inst.index_save()



"""
先到这里啦，在这里耽搁的时间是在是太多了
继续往前走了
"""