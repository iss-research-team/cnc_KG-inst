# 需要导出额外的两个信息
# 机构作者信息，文本作者信息

import json
import re
from collections import defaultdict
from tqdm import tqdm


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

class Author:
    def __init__(self):


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


def add_author(author_list, inst, text, index_inst_author_dict, index_text_author_dict, author_dict, label):
    '''
    :param author_list:
    :param inst:
    :param text:
    :param index_inst_author_dict:
    :param index_text_author_dict:
    :param author_dict:
    :param label:
    :return:
    '''

    for author in author_list:
        # 给每一个作者前面加一个inst
        author = str(inst) + ' | ' + author
        if author not in author_dict:
            author_dict[author] = label
            label += 1
        index_inst_author_dict[inst].add(author_dict[author])
        index_text_author_dict[text].add(author_dict[author])
    return index_inst_author_dict, index_text_author_dict, author_dict, label


def get_author():
    with open('../../data/processed_file/relationship_dict_literature.json', 'r', encoding='utf-8') as file:
        literature_dict = json.load(file)
    # 处理过的机构名，用于替换
    with open('../../data/middle_file/2.2.inst_trans_dict/institution_trans_dict_literature.json', 'r',
              encoding='UTF-8') as file:
        inst_trans_dict = json.load(file)
    with open('../../data/middle_file/2.3.combine/combine_list-0709.json', 'r', encoding='UTF-8') as file:
        combine_list = json.load(file)
    combine_dict = get_combine_dict(combine_list)
    with open('../../data/output/node/institution_label_dict.json', 'r', encoding='UTF-8') as file:
        inst_label_dict = json.load(file)
    with open('../../data/output/node/text_label_dict_literature.json', 'r', encoding='UTF-8') as file:
        text_label_dict = json.load(file)

    author_dict = dict()
    label = 1
    index_inst_author_dict = defaultdict(set)
    index_text_author_dict = defaultdict(set)

    pattern = re.compile(r"[\[](.*?)[\]]", re.S)

    for key, value in tqdm(literature_dict.items()):
        text = text_label_dict[key]
        if not value['institution']:
            continue
        inst_list_temper = value['institution']
        # 去除人名
        inst_list_temper = re.sub(pattern, '', inst_list_temper)
        inst_list_temper = [inst[:inst.index(',')].strip() for inst in inst_list_temper.split(';')]
        # 转换成label
        inst_list_temper = trans2label(inst_list_temper, inst_trans_dict, inst_label_dict, combine_dict)

        if len(inst_list_temper) > 1:
            authors_list = re.findall(pattern, value['institution'])
            for authors, inst in zip(authors_list, inst_list_temper):
                author_list = authors.split('; ')
                index_inst_author_dict, index_text_author_dict, \
                author_dict, label = add_author(author_list, inst, text, index_inst_author_dict, index_text_author_dict,
                                                author_dict, label)

        else:
            # 有author字段
            author_list = value["author"]
            inst = inst_list_temper[0]
            index_inst_author_dict, index_text_author_dict, \
            author_dict, label = add_author(author_list, inst, text, index_inst_author_dict, index_text_author_dict,
                                            author_dict, label)

    for inst in index_inst_author_dict:
        index_inst_author_dict[inst] = list(index_inst_author_dict[inst])
    for text in index_text_author_dict:
        index_text_author_dict[text] = list(index_text_author_dict[text])

    with open('../../data/output/node/author_label_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(author_dict, file)
    with open('../../data/middle_file/3.index/index_inst_author_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(index_inst_author_dict, file)
    with open('../../data/middle_file/3.index/index_text_author_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(index_text_author_dict, file)


if __name__ == '__main__':
    get_author()
