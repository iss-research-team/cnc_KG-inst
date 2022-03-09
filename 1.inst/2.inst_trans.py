import json
import re
import os
from tqdm import tqdm


def get_org(inst, org_list):
    """
    获取企业的组织形式
    :param inst:
    :param org_list:
    :return:
    """
    organization = ''
    inst = ' '.join(inst.split()) + ' '

    for org in org_list:
        if org in inst:
            if inst.find(org) == len(inst) - len(org):
                organization = org
                break
    if organization:
        inst = inst[:-len(organization)]
    return inst.strip(), organization[1:-1]


def inst_trans():
    """
    这个地方实际上没有去除任何信息，只是把组织形式放在了最后面
    label还是可以在三个方向进行转换
    """
    # 组织形式
    org_list_path = '../data/sign/company/organization_list.txt'
    org_list = [' ' + line.strip().lower() + ' ' for line in open(org_list_path, 'r', encoding='UTF-8').readlines()]

    inst_file_path = '../data/middle_file/2.1.inst_list/'
    inst_file_list = os.listdir(inst_file_path)

    inst_list = []
    inst_trans_dict = dict()

    for inst_file in inst_file_list:
        print('processing---', inst_file)
        with open(os.path.join(inst_file_path, inst_file)) as file:
            inst_list += json.load(file)

    inst_list = sorted(list(set(inst_list)))
    with open('../data/middle_file/2.2.inst_trans_dict/inst_list.json', 'w', encoding='UTF-8') as file:
        json.dump(inst_list, file)
    # 这里稍微处理一下
    for inst in tqdm(inst_list):
        inst_trans, org = get_org(inst, org_list)
        if org:
            inst_trans_dict[inst] = {'+': inst_trans + ' ' + org,
                                     '=': inst_trans}
        else:
            inst_trans_dict[inst] = {'+': inst_trans,
                                     '=': inst_trans}
    with open('../data/middle_file/2.2.inst_trans_dict/inst_trans_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(inst_trans_dict, file)


if __name__ == '__main__':
    inst_trans()
