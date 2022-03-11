import json
import Levenshtein
from tqdm import tqdm


# 计算莱文斯坦比
def string_Levenshtein(str1, str2):
    sim = Levenshtein.ratio(str1, str2)
    return sim


def node_combine():
    with open('../data/middle_file/2.2.inst_trans_dict/inst_trans_dict.json', 'r', encoding='UTF-8') as file:
        inst_dict = json.load(file)
    with open('../data/middle_file/2.2.inst_trans_dict/inst_list.json', 'r', encoding='UTF-8') as file:
        inst_list = json.load(file)
    num_inst = len(inst_list)
    # +的阈值，带有组织形式
    k_1 = 0.85
    # =的阈值，没有组织形式
    k_2 = 0.75

    combine_list_1 = []
    combine_list_2 = []

    for i in tqdm(range(0, num_inst - 1)):
        inst_1 = inst_list[i]
        inst_1_plus = inst_dict[inst_1]['+']
        inst_1_equal = inst_dict[inst_1]['=']

        for j in range(i + 1, num_inst):
            inst_2 = inst_list[j]
            inst_2_plus = inst_dict[inst_2]['+']
            inst_2_equal = inst_dict[inst_2]['=']
            sim_1 = string_Levenshtein(inst_1_plus, inst_2_plus)
            sim_2 = string_Levenshtein(inst_1_equal, inst_2_equal)
            if sim_1 > k_1:
                combine_list_1.append([inst_1, inst_2])
            if sim_2 > k_2:
                combine_list_2.append([inst_1, inst_2])

    link_path_1_json = '../data/middle_file/2.3.combine/combine_list_plus_0.95.json'
    link_path_2_json = '../data/middle_file/2.3.combine/combine_list_equal_0.95.json'

    with open(link_path_1_json, 'w', encoding="UTF-8") as file:
        json.dump(combine_list_1, file)
    with open(link_path_2_json, 'w', encoding="UTF-8") as file:
        json.dump(combine_list_2, file)


if __name__ == '__main__':
    node_combine()
