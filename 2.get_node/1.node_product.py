# 需要导出额外的两个信息
# 机构作者信息，文本作者信息

import json
import re
from collections import defaultdict


def get_emo_dict():
    with open('../data/input/exhibition/exhibitor_emo_2019.json', 'r', encoding='UTF-8') as file:
        inf_list = json.load(file)

    emo_name_dict = dict()
    for inf in inf_list:
        emo_name_dict[inf['brief']] = inf['translate_name_en']
    return emo_name_dict


class Product:
    def __init__(self, index_1_save_path, index_2_save_path, link_1_save_path, link_2_save_path):
        # trans pattern
        self.pattern = re.compile("[.,']")
        # 保存
        self.index_1_save_path = index_1_save_path
        self.index_2_save_path = index_2_save_path
        self.link_1_save_path = link_1_save_path
        self.link_2_save_path = link_2_save_path
        self.inst2index = dict()
        self.get_index()
        # 存储
        self.exh2index = {'cimt_2019': 0,
                          'cimt_2021': 1,
                          'emo_2019': 2}
        self.product2index = dict()
        self.exh_inst = defaultdict(set)
        self.inst_product = defaultdict(set)

    def get_index(self):
        with open('../data/middle_file/2.4.inst_index/inst2index.json', 'r', encoding='UTF-8') as file:
            self.inst2index = json.load(file)

    def name_trans(self, inst):
        """
        去除无用的字符，小写
        :return:
        """
        inst_trans = self.pattern.sub('', inst)
        return inst_trans.lower().strip()

    def get_product(self):
        index = 0
        key_dict = {'cimt_2019': ['cimt_2019.json', '公司英文名称', '展品名称(en)'],
                    'cimt_2021': ['cimt_2021.json', '公司英文名称', '展品名称(en)'],
                    'emo_2019': ['product_emo_2019.json', 'exhibitor', 'product']}

        emo_name_trans = get_emo_dict()

        for exhi, exhi_inf in key_dict.items():
            with open('../data/input/exhibition/' + exhi_inf[0], 'r', encoding='UTF-8') as file:
                inf_list = json.load(file)
            inst_key = exhi_inf[1]
            product_key = exhi_inf[2]
            for inf in inf_list:
                if inst_key not in inf or product_key not in inf:
                    continue
                inst = inf[inst_key]
                if exhi == 'emo_2019':
                    inst = emo_name_trans[inst]
                inst = self.name_trans(inst)
                # product
                product = inst + ' | ' + inf[product_key]
                if product not in self.product2index:
                    self.product2index[product] = index
                    index += 1

                self.exh_inst[self.exh2index[exhi]].add(self.inst2index[inst])
                self.inst_product[self.inst2index[inst]].add(self.product2index[product])

        print('num of exhibition:', len(self.exh2index))
        print('num of product:', len(self.product2index))


    def save(self):
        self.exh_inst = dict((exh, list(inst_set)) for exh, inst_set in self.exh_inst.items())
        self.inst_product = dict((inst, list(product_set)) for inst, product_set in self.inst_product.items())

        with open(self.index_1_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.product2index, file)
        with open(self.index_2_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.exh2index, file)
        with open(self.link_1_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.inst_product, file)
        with open(self.link_2_save_path, 'w', encoding='UTF-8') as file:
            json.dump(self.exh_inst, file)


if __name__ == '__main__':
    index_1_save_path = '../data/output/node/product2index.json'
    index_2_save_path = '../data/output/node/exhibition2index.json'

    link_1_save_path = '../data/middle_file/3.index/inst_product_dict.json'
    link_2_save_path = '../data/middle_file/3.index/exh_inst_dict.json'

    product = Product(index_1_save_path, index_2_save_path, link_1_save_path, link_2_save_path)
    product.get_product()
    product.save()
