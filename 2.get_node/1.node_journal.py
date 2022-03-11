# 需要导出额外的两个信息
# 机构作者信息，文本作者信息

import json
import re
from tqdm import tqdm
from collections import defaultdict


def journal_deal(journal_name, pattern):
    # 两个原则：
    # 1.去除括号中的内容
    # 2.& 替换成and
    journal_name = re.sub(pattern, ' ', journal_name)
    journal_name = journal_name.replace('&', ' AND ')
    journal_name = ''.join(re.findall("[A-Za-z0-9 ]", journal_name))
    journal_name = ' '.join(journal_name.split())
    return journal_name


class Journal:
    def __init__(self, index_save_path, link_save_path):
        # 保存
        self.index_save_path = index_save_path
        self.link_save_path = link_save_path

        self.doc_l2index = dict()
        self.get_index()
        # 存储
        self.journal2index = dict()
        self.journal_doc = defaultdict(set)

    def get_index(self):
        with open('../data/output/node/doc_literature2index.json', 'r', encoding='UTF-8') as file:
            self.doc_l2index = json.load(file)

    def get_journal(self):
        with open('../data/processed_file/relationship_dict_literature.json', 'r', encoding='utf-8') as file:
            literature_dict = json.load(file)
        index = 0
        pattern = re.compile(r"[(](.*?)[)]", re.S)

        for key, value in tqdm(literature_dict.items()):
            if not value['so']:
                continue
            journal = value['so']
            journal = journal_deal(journal, pattern)
            if journal not in self.journal2index:
                self.journal2index[journal] = index
                index += 1
            self.journal_doc[self.journal2index[journal]].add(self.doc_l2index[key])
        print('num of journal:', len(self.journal2index))

    def save(self):
        self.journal_doc = dict((journal, list(doc_set)) for journal, doc_set in self.journal_doc.items())

        with open(self.index_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.journal2index, file)
        with open(self.link_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.journal_doc, file)


if __name__ == '__main__':
    index_save_path = '../data/output/node/journal2index.json'
    link_save_path = '../data/middle_file/3.index/journal_doc_dict.json'

    journal = Journal(index_save_path, link_save_path)
    journal.get_journal()
    journal.save()
