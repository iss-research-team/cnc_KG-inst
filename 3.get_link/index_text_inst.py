# -*- coding:utf-8 -*-

# 这是一个很重要的中间结果
import json
import re


def not_empty(s):
    return s and s.strip()


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
    '''
    将机构trans为label
    :param inst_list_temper:
    :param inst_trans_dict:
    :param inst_label_dict:
    :param combine_dict:
    :return:
    '''
    inst_list_temper_trans = []
    for inst in inst_list_temper:
        if inst in inst_trans_dict:
            inst_trans = inst_trans_dict[inst]['+']
            if inst_trans in inst_label_dict:
                inst_list_temper_trans.append(inst_label_dict[inst_trans])
            else:
                inst_list_temper_trans.append(inst_label_dict[combine_dict[inst_trans]])
    return inst_list_temper_trans


def get_text_inst_dict():
    with open('../../data/processed_file/relationship_dict_' + label + '.json', 'r', encoding='UTF-8') as file:
        relationship_dict = json.load(file)
    # trans_dict
    with open('../../data/middle_file/2.2.institution_trans_dict/institution_trans_dict_' + label + '.json', 'r',
              encoding='UTF-8') as file:
        inst_trans_dict = json.load(file)
    with open('../../data/middle_file/2.3.combine/combine_list-0709.json', 'r', encoding='UTF-8') as file:
        combine_list = json.load(file)
    combine_dict = get_combine_dict(combine_list)
    with open('../../data/output/node/institution_label_dict.json', 'r', encoding='UTF-8') as file:
        inst_label_dict = json.load(file)

    with open('../../data/output/node/text_label_dict_' + label + '.json', 'r', encoding='UTF-8')as file:
        text_label_dict = json.load(file)

    index_text_inst_dict = dict()

    # 为有人名的机构准备的正则表达式
    pattern = re.compile(r"[\[](.*?)[\]]", re.S)

    for each_record in relationship_dict:
        if not relationship_dict[each_record]['institution']:
            continue
        inst_list_temper = []
        if label == 'literature':
            inst_list_temper = relationship_dict[each_record]['institution']
            # 去除人名
            inst_list_temper = re.sub(pattern, '', inst_list_temper)
            # 把第一项提出来
            inst_list_temper = [inst[:inst.index(',')].strip() for inst in inst_list_temper.split(';')]
            # 转换成label
            inst_list_temper = trans2label(inst_list_temper, inst_trans_dict, inst_label_dict, combine_dict)

        elif label == 'patent':
            inst_list_temper = relationship_dict[each_record]['institution'].split(' | ')
            # 转换成label
            inst_list_temper = trans2label(inst_list_temper, inst_trans_dict, inst_label_dict, combine_dict)
        time = relationship_dict[each_record]['time']

        index_text_inst_dict[text_label_dict[each_record]] = {'institution': inst_list_temper, 'time': time}

    with open('../../data/middle_file/3.index/index_text_inst_' + label + '.json', 'w',
              encoding='UTF-8') as file:
        json.dump(index_text_inst_dict, file)


if __name__ == '__main__':
    label = 'literature'
    get_text_inst_dict()
