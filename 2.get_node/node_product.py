# 需要导出额外的两个信息
# 机构作者信息，文本作者信息

import json
from collections import defaultdict


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


def get_emo_dict():
    with open('../../data/input/exhibition/exhibitor_emo_2019.json', 'r', encoding='UTF-8') as file:
        inf_list = json.load(file)

    emo_name_dict = dict()
    for inf in inf_list:
        emo_name_dict[inf['brief']] = inf['translate_name_en']
    return emo_name_dict


def trans2label(inst, inst_trans_dict, inst_label_dict, combine_dict):
    inst_label = -1
    if inst in inst_trans_dict:
        inst_trans = inst_trans_dict[inst]['+']
        if inst_trans in inst_label_dict:
            inst_label = inst_label_dict[inst_trans]
        else:
            inst_label = inst_label_dict[combine_dict[inst_trans]]

    return inst_label


def get_product():
    # 处理过的机构名，用于替换
    with open('../../data/middle_file/2.2.institution_trans_dict/institution_trans_dict_exhibition.json', 'r',
              encoding='UTF-8') as file:
        inst_trans_dict = json.load(file)
    with open('../../data/middle_file/2.3.combine/combine_list-0709.json', 'r', encoding='UTF-8') as file:
        combine_list = json.load(file)
    combine_dict = get_combine_dict(combine_list)
    with open('../../data/output/node/institution_label_dict.json', 'r', encoding='UTF-8') as file:
        inst_label_dict = json.load(file)

    exhi_dict = {'cimt_2019': 0,
                 'cimt_2021': 1,
                 'emo_2019': 2}

    product_dict = dict()
    label = 1
    index_inst_product_dict = defaultdict(set)
    index_exhi_product_dict = defaultdict(set)

    key_dict = {'cimt_2019': ['cimt_2019.json', '公司英文名称', '展品名称(en)'],
                'cimt_2021': ['cimt_2021.json', '公司英文名称', '展品名称(en)'],
                'emo_2019': ['product_emo_2019.json', 'exhibitor', 'product']}

    emo_name_trans = get_emo_dict()

    for exhi, exhi_inf in key_dict.items():
        with open('../../data/input/exhibition/' + exhi_inf[0], 'r', encoding='UTF-8') as file:
            inf_list = json.load(file)

        inst_key = exhi_inf[1]
        product_key = exhi_inf[2]
        for inf in inf_list:
            if inst_key in inf and product_key in inf:
                inst = inf[inst_key]
                if exhi == 'emo_2019':
                    inst = emo_name_trans[inst]
                inst = trans2label(inst, inst_trans_dict, inst_label_dict, combine_dict)

                # product
                product = str(inst) + ' | ' + inf[product_key]
                if product not in product_dict:
                    product_dict[product] = label
                    index_inst_product_dict[inst].add(label)
                    index_exhi_product_dict[exhi_dict[exhi]].add(label)
                    label += 1

    for inst in index_inst_product_dict:
        index_inst_product_dict[inst] = list(index_inst_product_dict[inst])

    for exhi in index_exhi_product_dict:
        index_exhi_product_dict[exhi] = list(index_exhi_product_dict[exhi])

    with open('../../data/output/node/product_label_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(product_dict, file)
    with open('../../data/output/node/exhibition_label_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(exhi_dict, file)
    with open('../../data/middle_file/3.index/index_inst_product_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(index_inst_product_dict, file)
    with open('../../data/middle_file/3.index/index_exhi_product_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(index_exhi_product_dict, file)


if __name__ == '__main__':
    get_product()
