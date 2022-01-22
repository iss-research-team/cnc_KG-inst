# 这里先放ipc后面再不断的加入
import json


def get_att(label):
    with open('../../data/processed_file/relationship_dict_' + label + '.json', 'r', encoding='UTF-8') as file:
        text_relationship_dict = json.load(file)
    with open('../../data/output/node/text_label_dict_' + label + '.json', 'r', encoding='UTF-8') as file:
        text_label_dict = json.load(file)

    text_dict = dict()

    for text, inf in text_relationship_dict.items():
        if label == 'patent':
            text_dict[text] = {'label': text_label_dict[text],
                               'title': inf['title'],
                               'IPC': inf['IPC'],
                               'time': inf['time']}
        elif label == 'literature':
            text_dict[text] = {'label': text_label_dict[text],
                               'so': inf['so'],
                               'time': inf['time']}

    json.dump(text_dict,
              open('../../data/output/node_with_att/text_label_dict_' + label + '.json', 'w', encoding='UTF-8'))


if __name__ == '__main__':
    label = 'literature'
    get_att(label)
