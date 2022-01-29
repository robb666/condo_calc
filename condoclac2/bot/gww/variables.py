from pprint import pprint
import re


def customer_data(path):
    file_dict = {}
    with open(path, 'r') as file:
        string = file.read().replace(': ', ':')
        clean_str = re.sub('\n+', '\n', string)
        arr = re.split('\n', clean_str)
        for item in arr:
            colon_splitted = item.split(':')
            if colon_splitted[0] != '':
                file_dict[colon_splitted[0]] = colon_splitted[1]
    file_dict['Zabezpieczenia'] = re.split(',\s+|,', file_dict['Zabezpieczenia'].rstrip())
    pprint(file_dict)
    return file_dict
