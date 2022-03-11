# -*- coding:utf-8 -*-

import csv
import json
from collections import Counter
from tqdm import tqdm


def get_link_hold(label):
    with open('../../data/middle_file/3.index/index_text_inst_' + label + '.json', 'r',
              encoding='UTF-8') as file:
        index_text_index_dict = json.load(file)

    link_list_count = Counter()

    for text, inf in tqdm(index_text_index_dict.items()):
        inst_list = inf['institution']
        time = inf['time']
        if len(inst_list) < 2:
            continue
        inst_list = sorted(inst_list)
        for i in range(0, len(inst_list) - 1):
            for j in range(i + 1, len(inst_list)):
                link_list_count[str(inst_list[i]) + ' | ' + str(inst_list[j]) + ' | ' + str(time)] += 1

    # 直接写csv，不写json了。link_iterature.csv
    csv_write_path = '../../data/output/link/link_inst_cooperation_' + label + '.csv'
    csv_write = csv.writer(open(csv_write_path, 'w', encoding='UTF-8', newline=''))
    for link, weight in link_list_count.items():
        s, t, time = [int(inf) for inf in link.split(' | ')]
        csv_write.writerow([s, t, weight, time])

    print('num of link:', len(link_list_count))


if __name__ == '__main__':
    label = 'literature'
    get_link_hold(label)
