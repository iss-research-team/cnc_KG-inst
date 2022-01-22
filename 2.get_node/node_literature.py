# -*- coding:utf-8 -*-

import csv
import json
import re


def not_empty(s):
    return s and s.strip()


def make_dict(label):
    '''
    生成专利论文的字典
    :param label:
    :return:
    '''
    with open('../../data/processed_file/relationship_dict_' + label + '.json', 'r', encoding='UTF-8') as file:
        relationship_dict = json.load(file)

    index_text_dict = dict()
    index = 0

    for text in relationship_dict:
        if not text:
            print(1)
        index_text_dict[text] = index
        index += 1
    with open('../../data/output/node/text_label_dict_' + label + '.json', 'w', encoding='UTF-8') as file:
        json.dump(index_text_dict, file)


if __name__ == '__main__':
    label = 'literature'
    make_dict(label)
