#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/1/26
# @Author  : liu yuhan
# @FileName: preporcess_patent.py
# @Software: PyCharm

import os
import xlrd
import csv
import json
from tqdm import tqdm


# 0 公开号
# 1 标题 - DWPI
# 2 标题 (英语)
# 3 标题
# 4 标题 (原文)
# 5 摘要 - DWPI
# 6 摘要 (英语)
# 7 摘要
# 8 摘要 (原文)
# 9 权利要求 (英语)
# 10 权利要求
# 11 权利要求计数
# 12 权利要求第一项 - DWPI
# 13 权利要求第一项
# 14 独立权利要求
# 15 优化的专利权人
# 16 专利权人 - DWPI
# 17 专利权人代码 - DWPI
# 18 专利权人 - 标准化
# 19 专利权人/申请人
# 20 专利权人 - 原始
# 21 专利权人 - 原始 (带有地址)
# 22 专利权人 - 原始 - 国家/地区
# 23 专利权人计数
# 24 终属母公司
# 25 发明人 - DWPI
# 26 发明人
# 27 发明人 - 原始
# 28 发明人 - 带有地址
# 29 发明人计数
# 30 优先权日 - DWPI
# 31 优先权日
# 32 公开日期
# 33 优先权国家/地区
# 34 优先权国家/地区 - DWPI
# 35 IPC - 现版 - DWPI
# 36 IPC - 现版
# 37 引用的专利详细信息 - DPCI
# 38 引用的参考文献详细信息 - 专利
# 39 引用的专利计数 - DPCI
# 40 引用的非专利 - DPCI
# 41 引用的参考文献 - 非专利
# 42 引用的非专利计数 - DPCI
# 43 施引专利详细信息 - DPCI
# 44 施引参考文献详细信息 - 专利
# 45 施引专利计数 - DPCI
# 46 DWPI 同族专利成员 失效/有效
# 47 INPADOC 同族专利成员 失效/有效
# 48 DWPI 同族专利成员计数
# 49 领域影响
# 50 综合专利影响力



def get_str(str1, str2):
    if str1 != '':
        inf = str1
    elif str2 != '':
        inf = str2
    else:
        inf = ''
    return inf


def not_empty(s):
    return s and s.strip()


def deal(prepare_path, csv_write_path):
    csv.field_size_limit(500 * 1024 * 1024)

    prepare_file_list = os.listdir(prepare_path)

    patent_count = 0
    # 去重机制
    patent_dict = dict()

    for each_file in prepare_file_list:
        csv_read = csv.reader(open(os.path.join(prepare_path, each_file), 'r', encoding='UTF-8'))
        # 跳过前三行
        next(csv_read)
        next(csv_read)
        next(csv_read)
        for inf_list in tqdm(csv_read):
            # 信息归拢
            patent_id = inf_list[0]
            # 1.时间的问题时间为空跳过循环
            date = get_str(inf_list[30], inf_list[31])
            if not date:
                continue
            time_list = date.split(' | ')
            time = sorted([int(time[:4]) for time in time_list])[0]
            # 其他的信息
            # 2021.12.27专利权人的部分更新
            holder = {'inst-dwpi': inf_list[16],
                      'inst-parent': inf_list[24],
                      'inst-adv': inf_list[15],
                      'inst-original': inf_list[20]}

            author = {'author-dwpi': inf_list[25],
                      'author-original': inf_list[27]}
            holder_code = inf_list[17]
            title = get_str(inf_list[1], inf_list[2])
            # citing_patent = get_str(inf_list[37], inf_list[38])
            citing_patent = inf_list[37]
            citing_paper = get_str(inf_list[40], inf_list[41])
            IPC = get_str(inf_list[35], inf_list[36])
            family = inf_list[46]

            if patent_id in patent_dict:
                continue
            # 这个地方的属性定义需要细化
            patent_dict[patent_id] = {'time': time,
                                      'title': title,
                                      'institution': holder,
                                      'author': author,
                                      'institution_code': holder_code,
                                      'citing_patent': citing_patent,
                                      'citing_paper': citing_paper,
                                      'IPC': IPC,
                                      'family': family}
            patent_count += 1
    json.dump(patent_dict, open(json_write_path, 'w', encoding='UTF-8'))

    print('获取专利数量：', patent_count)


if __name__ == '__main__':
    prepare_path = '../../data/input/patent'
    json_write_path = '../../data/processed_file/relationship_dict_patent.json'
    deal(prepare_path, json_write_path)
