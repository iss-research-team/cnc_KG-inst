#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/7/13 上午10:32
# @Author  : liu yuhan
# @FileName: 4.inst_combine_1.py
# @Software: PyCharm

import json
from tqdm import tqdm
import difflib
import Levenshtein


# 1. difflib
def string_difflib(str1, str2):
    seq = difflib.SequenceMatcher(None, str1, str2)
    ratio = seq.ratio()
    return ratio


# 2. hamming距离，str1和str2长度必须一致，描述两个等长字串之间对应位置上不同字符的个数
def string_hamming(str1, str2):
    sim = Levenshtein.hamming(str1, str2)
    print('hamming similarity: ', sim)


# 3. 编辑距离，描述由一个字串转化成另一个字串最少的操作次数，在其中的操作包括 插入、删除、替换
def string_Levenshtein_distance(str1, str2):
    sim = Levenshtein.distance(str1, str2)
    return sim


# 4.计算莱文斯坦比
def string_Levenshtein(str1, str2):
    sim = Levenshtein.ratio(str1, str2)
    return sim


# 5.计算jaro距离
def string_jaro(str1, str2):
    sim = Levenshtein.jaro(str1, str2)
    return sim


# 6. Jaro–Winkler距离
def string_jaro_winkler(str1, str2):
    sim = Levenshtein.jaro_winkler(str1, str2)
    return sim


def institution_match(institution_path, output_path):
    # 机构名字list
    with open(institution_path, 'r', encoding='UTF-8') as file:
        institution_dict = json.load(file)
    institution_dict = {value: key for key, value in institution_dict.items()}

    matched_list = []

    length = len(institution_dict)

    for i in tqdm(range(0, length - 1)):
        # institution_1去除组织形式
        institution_1 = institution_dict[i]
        for j in range(i + 1, length):
            institution_2 = institution_dict[j]
            sim = string_Levenshtein(institution_1, institution_2)
            if sim > 0.80:
                matched_list.append([institution_1, institution_2, sim])

    with open(output_path, 'w', encoding='UTF-8') as file:
        json.dump(matched_list, file)


if __name__ == '__main__':
    institution_path_list = ['../../data/middle_file/2.3.combine/institution_label_dict_1.json',
                             '../../data/middle_file/2.3.combine/institution_label_dict_2.json']
    output_path_list = ['../../data/middle_file/2.3.combine/institution_process_dict_1.json',
                        '../../data/middle_file/2.3.combine/institution_process_dict_2.json']
    for institution_path, output_path_list in zip(institution_path_list, output_path_list):
        institution_match(institution_path, output_path_list)
