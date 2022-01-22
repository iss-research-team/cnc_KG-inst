import json
import re
from tqdm import tqdm


def get_org(institution, org_list):
    organization = ''
    institution = institution.lower()
    institution = re.findall(r'[a-z0-9 -]+', institution)
    institution = ''.join(institution)
    institution = ' '.join(institution.split()) + ' '

    for org in org_list:
        if org in institution:
            if institution.find(org) == len(institution) - len(org):
                organization = org
                break
    if organization:
        institution = institution[:-len(organization)]
    return institution.strip(), organization[1:-1]


def get_words_list(file_path):
    file = open(file_path, 'r', encoding='UTF-8')
    word_list = []
    for each_line in file:
        word_list.append(each_line[:-1].lower())
    return word_list


def company_judge(holder, flag):
    # 特殊符号和数字
    for symbol in special_symbol_list + number_list:
        if symbol in holder:
            flag = 1
            break
    # 特殊字眼
    holder = holder.lower()
    holder = re.findall(r'[a-z0-9 -]+', holder)
    holder = ''.join(holder)
    holder = ' '.join(holder.split()) + ' '

    for word in special_word_list_1 + special_word_list_2:
        if word in holder:
            flag = 1
            break
    words_list = holder.replace('-', ' ').split()
    # 没有空格
    if len(words_list) == 1:
        flag = 1

    # 末尾出现国家代码
    if words_list[-1] in country_code_2bit_list + country_code_3bit_list:
        flag = 1
    # 判断是不是人名
    if flag != 1:
        # if holder[-2] == ' ':
        #     flag = -1
        if words_list[0] in first_name_list or words_list[-1] in first_name_list:
            flag = -1

    return flag


if __name__ == '__main__':
    '''
    这个地方实际上没有去除任何信息，只是把地名提到了最前面
    label还是可以在三个方向进行转换

    20210706 肥猫
    进行一轮修改
    经营范围列表更新
    '''

    label = 'patent'
    institution_list = json.load(open('../data/2.1.institution_list/institution_list_' + label +
                                      '.json', 'r', encoding='UTF-8'))

    # 组织形式
    org_list_path = '../../data/sign/company/organization_list.txt'
    org_list = [' ' + line.strip().lower() + ' ' for line in open(org_list_path, 'r', encoding='UTF-8').readlines()]
    # 经营范围
    opr_list_path = '../../data/sign/company/operation_list.txt'
    opr_list = [' ' + line.strip().lower() + ' ' for line in open(opr_list_path, 'r', encoding='UTF-8').readlines()]

    institution_trans_dict = dict()

    if label == 'supply' or label == 'exhibition' or label == 'literature':

        # 这里稍微处理一下
        for institution in tqdm(institution_list):
            institution_trans, org = get_org(institution, org_list)
            if org:
                institution_trans_dict[institution] = {'+': institution_trans + ' ' + org,
                                                       '=': institution_trans}
            else:
                institution_trans_dict[institution] = {'+': institution_trans,
                                                       '=': institution_trans}
            print(institution + '|' + institution_trans.strip() + '|' + org)

    elif label == 'patent':
        special_words_1_file_path = '../../data/sign/company/operation_list.txt'
        special_words_2_file_path = '../../data/sign/company/organization_list.txt'

        country_code_2bit_file_path = '../../data/sign/company/country_code_2bit.txt'
        country_code_3bit_file_path = '../../data/sign/company/country_code_3bit.txt'

        first_name_chinese_file_path = '../../data/sign/person/lastname_chinese.txt'
        first_name_japanese_file_path = '../../data/sign/person/lastname_japanese.txt'
        first_name_american_file_path = '../../data/sign/person/lastname_english.txt'

        special_word_list_1 = get_words_list(special_words_1_file_path)
        special_word_list_2 = get_words_list(special_words_2_file_path)

        country_code_2bit_list = get_words_list(country_code_2bit_file_path)
        country_code_3bit_list = get_words_list(country_code_3bit_file_path)
        special_symbol_list = ['&', '+', '/', '(', ')']
        number_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        first_name_list = get_words_list(first_name_chinese_file_path) + \
                          get_words_list(first_name_japanese_file_path) + \
                          get_words_list(first_name_american_file_path)

        for institution in tqdm(institution_list):
            flag = 0
            flag = company_judge(institution, flag)
            if flag == 1:
                institution_trans, org = get_org(institution, org_list)
                if org:
                    institution_trans_dict[institution] = {'+': institution_trans + ' ' + org,
                                                           '=': institution_trans}
                else:
                    institution_trans_dict[institution] = {'+': institution_trans,
                                                           '=': institution_trans}
                print(institution + '|' + institution_trans.strip() + '|' + org)

    json.dump(institution_trans_dict,
              open('../../data/middle_file/2.2.institution_trans_dict/institution_trans_dict_' + label + '.json', 'w',
                   encoding='UTF-8'))
