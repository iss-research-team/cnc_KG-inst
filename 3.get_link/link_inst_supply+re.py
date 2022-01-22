# -*- coding:utf-8 -*-
import json
import csv


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
    inst_list_temper_trans = []
    for inst in inst_list_temper:
        if inst in inst_trans_dict:
            inst_trans = inst_trans_dict[inst]['+']
            if inst_trans in inst_label_dict:
                inst_list_temper_trans.append(inst_label_dict[inst_trans])
            else:
                inst_list_temper_trans.append(inst_label_dict[combine_dict[inst_trans]])
    return inst_list_temper_trans


def get_supply():
    # 处理过的机构名，用于替换
    with open('../../data/middle_file/2.2.institution_trans_dict/institution_trans_dict_supply.json', 'r',
              encoding='UTF-8') as file:
        inst_trans_dict = json.load(file)
    with open('../../data/middle_file/2.3.combine/combine_list-0709.json', 'r', encoding='UTF-8') as file:
        combine_list = json.load(file)
    combine_dict = get_combine_dict(combine_list)
    with open('../../data/output/node/institution_label_dict.json', 'r', encoding='UTF-8') as file:
        inst_label_dict = json.load(file)

    link_list = []
    # 读文件
    file_path_dict = {'../../data/input/supply_chain/company_link_1.json': 0,
                      '../../data/input/supply_chain/company_link_3.json': 1}
    for file_path in file_path_dict:
        institution_list = json.load(open(file_path))['nodes']
        institution_link = json.load(open(file_path))['links']

        institution_dict = dict()
        for institution in institution_list:
            institution_dict[institution['node_id']] = institution['name']

        for link in institution_link:
            if file_path_dict[file_path] == 0:
                link = [institution_dict[link['source']], institution_dict[link['target']]]
            else:
                link = [institution_dict[link['target']], institution_dict[link['source']]]

            link = trans2label(link, inst_trans_dict, inst_label_dict, combine_dict)
            link_list.append(link)

    # 这个地方为去重服务
    # 这里需要考虑的是加权重是否有意义
    # 目前来开权重是没有意义的
    link_list = [' | '.join([str(link[0]), str(link[1])]) for link in link_list]
    link_list = sorted(list(set(link_list)))

    # 直接写csv，不写json了。
    csv_write_path = '../../data/output/link/link_inst_supply.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for link in link_list:
        csv_write.writerow([int(index) for index in link.split(' | ')])

    print('供应链计数：', len(link_list))


def get_re():
    # 处理过的机构名，用于替换
    with open('../../data/middle_file/2.2.institution_trans_dict/institution_trans_dict_supply.json', 'r',
              encoding='UTF-8') as file:
        inst_trans_dict = json.load(file)
    with open('../../data/middle_file/2.3.combine/combine_list-0709.json', 'r', encoding='UTF-8') as file:
        combine_list = json.load(file)
    combine_dict = get_combine_dict(combine_list)
    with open('../../data/output/node/institution_label_dict.json', 'r', encoding='UTF-8') as file:
        inst_label_dict = json.load(file)

    link_list = []
    # 读文件
    file_path_list = ['../../data/input/supply_chain/company_link_2.json']
    for file_path in file_path_list:
        institution_list = json.load(open(file_path))['nodes']
        institution_link = json.load(open(file_path))['links']

        institution_dict = dict()
        for institution in institution_list:
            institution_dict[institution['node_id']] = institution['name']

        for link in institution_link:
            link = [institution_dict[link['source']], institution_dict[link['target']]]
            link = trans2label(link, inst_trans_dict, inst_label_dict, combine_dict)
            link_list.append(link)

    # 这个地方为去重服务
    # 这里需要考虑的是加权重是否有意义
    # 目前来开权重是没有意义的
    link_list = [' | '.join([str(link[0]), str(link[1])]) for link in link_list]
    link_list = sorted(list(set(link_list)))

    # 直接写csv，不写json了。
    csv_write_path = '../../data/output/link/link_inst_re.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for link in link_list:
        csv_write.writerow([int(index) for index in link.split(' | ')])

    print('同比计数：', len(link_list))


if __name__ == '__main__':
    get_supply()
    get_re()
