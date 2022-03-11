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


class Country:
    def __init__(self, index_save_path, link_save_path):
        # trans pattern
        self.pattern = re.compile("[.,']")
        # 为有人名的机构准备的正则表达式
        self.pattern_remove_name = re.compile(r"[\[](.*?)[]]", re.S)
        # 保存
        self.index_save_path = index_save_path
        self.link_save_path = link_save_path
        self.inst2index = dict()
        self.get_index()
        self.country2index = dict()
        self.country_inst = defaultdict(set)

    def get_index(self):
        with open('../data/middle_file/2.4.inst_index/inst2index.json', 'r', encoding='UTF-8') as file:
            self.inst2index = json.load(file)

    def name_trans(self, inst_list):
        """
        去除无用的字符，小写
        :return:
        """
        inst_list_trans = []
        for inst in inst_list:
            inst_trans = self.pattern.sub('', inst)
            inst_list_trans.append(inst_trans.lower().strip())
        return list(set(inst_list_trans))

    def trans2label(self, inst_list_temper):
        """
        转换为label
        :param inst_list_temper:
        :return:
        """
        return [self.inst2index[inst] for inst in inst_list_temper if inst in self.inst2index]

    def get_inst_list_literature(self, inst_str):
        """
        :param inst_inf:
        :param author_inf:
        :return:
        """
        # 去除人名
        inst_str = re.sub(self.pattern_remove_name, '', inst_str)
        inst_list_temper = [inst[:inst.find(',')].strip() for inst in inst_str.split('; ')]
        inst_list_temper = list(filter(not_empty, inst_list_temper))
        return self.name_trans(inst_list_temper)

    def get_country(self):
        with open('../data/processed_file/relationship_dict_literature.json', 'r', encoding='utf-8') as file:
            literature_dict = json.load(file)
        # 处理过的机构名，用于替换
        index = 0

        for key, value in tqdm(literature_dict.items()):
            if not value['institution']:
                continue
            inst_list_temper = self.get_inst_list_literature(value['institution'])
            # 转换成label
            inst_list_temper = self.trans2label(inst_list_temper)
            # 国家清单
            country_list_temper = [inst[inst.rfind(',') + 1:].strip() for inst in value['institution'].split('; ')]

            for country, inst in zip(country_list_temper, inst_list_temper):
                country = deal(country)
                if country not in self.country2index:
                    self.country2index[country] = index
                    index += 1
                self.country_inst[self.country2index[country]].add(inst)

    def save(self):
        self.country_inst = dict((country, list(inst_set)) for country, inst_set in self.country_inst.items())
        with open(self.index_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.country2index, file)
        with open(self.link_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.country_inst, file)


if __name__ == '__main__':
    index_save_path = '../data/output/node/country2index.json'
    link_save_path = '../data/middle_file/3.index/country_inst_dict.json'
    country = Country(index_save_path, link_save_path)
    country.get_country()
    country.save()
