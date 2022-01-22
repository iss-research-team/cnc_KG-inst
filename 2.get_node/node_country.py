import json
import csv
import re
from collections import defaultdict
from tqdm import tqdm

state = {'ca', 'tn', 'ny', 'az', 'ms', 'la', 'nj', 'tx', 'fl'}


def not_empty(s):
    return s and s.strip()


# 特殊情况替换
def deal(country):
    country = country.lower()
    if "usa" in country:
        return "american"
    if re.findall("[0-9]+", country):
        return "american"
    if country in state:
        return "american"
    if "china" in country:
        return "china"
    return country.strip()


def set2list(_dict):
    _dict_trans = dict()
    for key, value in _dict.items():
        _dict_trans[key] = list(value)
    return _dict_trans


def get_inst_p(str_list):
    str_len_list = [len(each_str) for each_str in str_list]
    return str_list[str_len_list.index(max(str_len_list))]


def get_combine_dict(combine_list):
    '''
    将combine_list转换成一个字典
    :param combine_list:
    :return:
    '''
    combine_dict = dict()
    for combine in combine_list:
        inst_p = get_inst_p(combine)
        for inst in combine:
            combine_dict[inst] = inst_p
    return combine_dict


def trans2label(inst_list_temper, inst_trans_dict, inst_label_dict, combine_dict):
    inst_list_temper_trans = []
    for inst in inst_list_temper:
        if inst in inst_trans_dict:
            inst_trans = inst_trans_dict[inst]['+']
            if inst_trans in inst_label_dict:
                inst_list_temper_trans.append(inst_label_dict[inst_trans])
            else:
                inst_list_temper_trans.append(inst_label_dict[combine_dict[inst_trans]])
    return inst_list_temper_trans


def get_country():
    with open('../../data/processed_file/relationship_dict_literature.json', 'r', encoding='utf-8') as file:
        literature_dict = json.load(file)
    # 处理过的机构名，用于替换
    with open('../../data/middle_file/2.2.institution_trans_dict/institution_trans_dict_literature.json', 'r',
              encoding='UTF-8') as file:
        inst_trans_dict = json.load(file)
    with open('../../data/middle_file/2.3.combine/combine_list-0709.json', 'r', encoding='UTF-8') as file:
        combine_list = json.load(file)
    combine_dict = get_combine_dict(combine_list)
    with open('../../data/output/node/institution_label_dict.json', 'r', encoding='UTF-8') as file:
        inst_label_dict = json.load(file)

    country_dict = dict()
    label = 1
    index_country_inst_dict = defaultdict(set)

    # 为有人名的机构准备的正则表达式
    pattern = re.compile(r"[\[](.*?)[\]]", re.S)

    for key, value in tqdm(literature_dict.items()):
        if not value['institution']:
            continue

        inst_list_temper = value['institution']
        # 去除人名
        inst_list_temper = re.sub(pattern, '', inst_list_temper)
        country_list_temper = [inst[inst.rfind(',') + 1:].strip() for inst in inst_list_temper.split(';')]
        inst_list_temper = [inst[:inst.find(',')].strip() for inst in inst_list_temper.split(';')]
        # 转换成label
        inst_list_temper = trans2label(inst_list_temper, inst_trans_dict, inst_label_dict, combine_dict)

        for country, inst in zip(country_list_temper, inst_list_temper):
            country = deal(country)
            if country not in country_dict:
                country_dict[country] = label
                label += 1
            index_country_inst_dict[country_dict[country]].add(inst)

    for country in index_country_inst_dict:
        index_country_inst_dict[country] = list(index_country_inst_dict[country])

    with open('../../data/output/node/country_label_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(country_dict, file)
    with open('../../data/middle_file/3.index/index_country_inst_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(index_country_inst_dict, file)


if __name__ == '__main__':
    get_country()
