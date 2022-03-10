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
    """
    后续还是要把专利的作者考虑进来
    """

    def __init__(self, index_save_path, link_1_save_path, link_2_save_path):
        # trans pattern
        self.pattern = re.compile("[.,']")
        # 为有人名的机构准备的正则表达式
        self.pattern_remove_name = re.compile(r"[\[](.*?)[]]", re.S)
        # 保存
        self.index_save_path = index_save_path
        self.link_1_save_path = link_1_save_path
        self.link_2_save_path = link_2_save_path

        self.inst2index = dict()
        self.doc_l2index = dict()
        self.get_index()
        # 存储
        self.author2index = dict()
        self.inst_author = defaultdict(set)
        self.doc_author = defaultdict(set)

    def get_index(self):
        with open('../data/middle_file/2.4.inst_index/inst2index.json', 'r', encoding='UTF-8') as file:
            self.inst2index = json.load(file)
        with open('../data/output/node/doc_literature2index.json', 'r', encoding='UTF-8') as file:
            self.doc_l2index = json.load(file)

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

    def get_author(self):
        with open('../data/processed_file/relationship_dict_literature.json', 'r', encoding='utf-8') as file:
            literature_dict = json.load(file)
        index = 1

        for doc, value in tqdm(literature_dict.items()):
            if not value['institution']:
                continue
            inst_str = value['institution']
            # 去除人名
            inst_str = re.sub(self.pattern_remove_name, '', inst_str)
            inst_list_temper = [inst[:inst.find(',')].strip() for inst in inst_str.split('; ')]
            inst_list_temper = self.name_trans(inst_list_temper)
            # 转换成label

            if len(inst_list_temper) > 1:
                # 作者在多个单位
                authors_list_temper = re.findall(self.pattern_remove_name, value['institution'])
                for authors, inst in zip(authors_list_temper, inst_list_temper):
                    authors = authors.split('; ')
                    for author in authors:
                        author_inst = author + ' | ' + inst
                        if author_inst not in self.author2index:
                            self.author2index[author_inst] = index
                            index += 1
                        self.inst_author[self.inst2index[inst]].add(self.author2index[author_inst])
                        self.doc_author[self.doc_l2index[doc]].add(self.author2index[author_inst])
            else:
                # 有author字段
                authors = value["author"]
                inst = inst_list_temper[0]
                for author in authors:
                    author_inst = author + ' | ' + inst
                    if author_inst not in self.author2index:
                        self.author2index[author_inst] = index
                        index += 1
                    self.inst_author[self.inst2index[inst]].add(self.author2index[author_inst])
                    self.doc_author[self.doc_l2index[doc]].add(self.author2index[author_inst])
        print('num of author:', len(self.author2index))

    def save(self):
        self.inst_author = dict((inst, list(author_set)) for inst, author_set in self.inst_author.items())
        self.doc_author = dict((doc, list(author_set)) for doc, author_set in self.doc_author.items())

        with open(self.index_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.author2index, file)
        with open(self.link_1_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.inst_author, file)
        with open(self.link_2_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.doc_author, file)


if __name__ == '__main__':
    index_save_path = '../data/output/node/author2index.json'
    link_1_save_path = '../data/middle_file/3.index/inst_author_dict.json'
    link_2_save_path = '../data/middle_file/3.index/doc_author_dict.json'
    author = Author(index_save_path, link_1_save_path, link_2_save_path)
    author.get_author()
    author.save()
