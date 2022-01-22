#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/7/16 上午11:16
# @Author  : liu yuhan
# @FileName: node_techpoint.py
# @Software: PyCharm


import json
import csv


def get_node_list(tech_tree_dict):
    node_list = []
    for father in tech_tree_dict:
        node_list.append(father)
        child_list = tech_tree_dict[father]
        if child_list:
            node_list += child_list

    node_list = sorted(list(set(node_list)))
    return node_list


def get_tech_point():
    tech_tree_dict_path = '../../data/input/tech_tree/tech_tree_dict.json'

    with open(tech_tree_dict_path, 'r', encoding='UTF-8') as file:
        tech_tree_dict = json.load(file)

    # 把总的技术体系引入
    tech_1_list = ['machine parts',
                   'intelligent system',
                   'numerical control system',
                   'network technology',
                   'process system']
    tech_tree_dict['machine tool'] = tech_1_list
    techpoint_list = get_node_list(tech_tree_dict)
    techpoint_dict = dict(zip(techpoint_list, [i for i in range(len(techpoint_list))]))
    with open('../../data/output/node/techpoint_label_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(techpoint_dict, file)


if __name__ == '__main__':
    get_tech_point()
