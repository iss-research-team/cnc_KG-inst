import json


def node_combine():
    institution_trans_dict_1 = json.load(open(
        '../../data/middle_file/2.2.institution_trans_dict/institution_trans_dict_patent.json', 'r', encoding='UTF-8'))
    institution_trans_dict_2 = json.load(open(
        '../../data/middle_file/2.2.institution_trans_dict/institution_trans_dict_literature.json', 'r', encoding='UTF-8'))
    institution_trans_dict_3 = json.load(open(
        '../../data/middle_file/2.2.institution_trans_dict/institution_trans_dict_supply.json', 'r', encoding='UTF-8'))
    institution_trans_dict_4 = json.load(open(
        '../../data/middle_file/2.2.institution_trans_dict/institution_trans_dict_exhibition.json', 'r', encoding='UTF-8'))

    inst_trans_list_1 = []
    inst_trans_list_2 = []
    inst_dict_2_1 = dict()

    for institution_dict in [institution_trans_dict_1, institution_trans_dict_2, institution_trans_dict_3,
                             institution_trans_dict_4]:
        for key, value in institution_dict.items():
            inst_trans_list_1.append(value['+'])
            inst_trans_list_2.append(value['='])
            if value['='] not in inst_dict_2_1:
                inst_dict_2_1[value['=']] = [value['+']]
            else:
                inst_dict_2_1[value['=']].append(value['+'])

    for inst in inst_dict_2_1:
        inst_dict_2_1[inst] = list(set(inst_dict_2_1[inst]))

    # 合并去重
    inst_trans_list_1 = sorted(list(set(inst_trans_list_1)))
    inst_trans_list_2 = sorted(list(set(inst_trans_list_2)))

    institution_label_dict_1 = dict(zip(inst_trans_list_1, [label for label in range(len(inst_trans_list_1))]))
    institution_label_dict_2 = dict(zip(inst_trans_list_2, [label for label in range(len(inst_trans_list_2))]))

    print('patent', len(institution_trans_dict_1))
    print('literature', len(institution_trans_dict_2))
    print('supply', len(institution_trans_dict_3))
    print('exhibition', len(institution_trans_dict_4))

    print('合并前的长度', len(institution_trans_dict_1) + len(institution_trans_dict_2) + len(institution_trans_dict_3) + len(
        institution_trans_dict_4),
          '合并后的长度有组织形式', len(inst_trans_list_1),
          '合并后的长度无组织形式', len(inst_trans_list_2))

    with open('../../data/middle_file/2.3.combine/institution_label_dict_1.json', 'w', encoding='UTF-8') as file:
        json.dump(institution_label_dict_1, file)
    with open('../../data/middle_file/2.3.combine/institution_label_dict_2.json', 'w', encoding='UTF-8') as file:
        json.dump(institution_label_dict_2, file)
    with open('../../data/middle_file/2.3.combine/inst_dict_2_1.json', 'w', encoding='UTF-8') as file:
        json.dump(inst_dict_2_1, file)


if __name__ == '__main__':
    node_combine()
