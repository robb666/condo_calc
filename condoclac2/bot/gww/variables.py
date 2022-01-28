from pprint import pprint
import re


def customer_data(path):
    file_dict = {}
    with open(path, 'r') as file:
        string = file.read().replace(' ', '')
        clean_str = re.sub('\n+', '\n', string)
        arr = re.split('\n', clean_str)
        for item in arr:
            colon_splited = item.split(':')
            if colon_splited[0] != '':
                file_dict[colon_splited[0]] = colon_splited[1]
    pprint(file_dict)
    return file_dict
