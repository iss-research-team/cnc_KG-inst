# 需要导出额外的两个信息
# 机构作者信息，文本作者信息

import json
import re
from tqdm import tqdm
from collections import defaultdict


def journal_deal(journal, pattern):
    # 两个原则：
    # 1.去除括号中的内容
    # 2.& 替换成and
    journal = re.sub(pattern, ' ', journal)
    journal = journal.replace('&', ' AND ')
    journal = ''.join(re.findall("[A-Za-z0-9 ]", journal))
    journal = ' '.join(journal.split())
    return journal


def get_journal():
    with open('../../data/processed_file/relationship_dict_literature.json', 'r', encoding='utf-8') as file:
        literature_dict = json.load(file)
    with open('../../data/output/node/text_label_dict_literature.json', 'r', encoding='UTF-8') as file:
        text_label_dict = json.load(file)

    journal_dict = dict()
    label = 1
    index_journal_text_dict = defaultdict(set)

    pattern = re.compile(r"[\(](.*?)[\)]", re.S)

    for key, value in tqdm(literature_dict.items()):
        text = text_label_dict[key]
        if not value['so']:
            continue
        journal = value['so']
        journal = journal_deal(journal, pattern)
        if journal not in journal_dict:
            journal_dict[journal] = label
            label += 1
        index_journal_text_dict[journal_dict[journal]].add(text)
    print(len(journal_dict))

    for journal in index_journal_text_dict:
        index_journal_text_dict[journal] = list(index_journal_text_dict[journal])

    with open('../../data/output/node/journal_label_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(journal_dict, file)
    with open('../../data/middle_file/3.index/index_journal_text_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(index_journal_text_dict, file)


if __name__ == '__main__':
    get_journal()
