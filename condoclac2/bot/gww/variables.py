from pprint import pprint
import re


def customer_data(path):
    file_dict = {}
    with open(path, 'r', encoding='utf8') as file:
        file = file.readlines()
        for f in file:
            string = re.sub(':\s+', ':', f)
            clean_str = re.sub('\n+', '', string)
            arr = re.split('\n', clean_str)
            for item in arr:
                colon_splitted = item.split(':')
                if colon_splitted[0] != '':
                    file_dict[colon_splitted[0]] = colon_splitted[1].rstrip()
                else:
                    pass

        file_dict['Zabezpieczenia'] = re.split(',\s+|,', file_dict['Zabezpieczenia'].rstrip())

    return file_dict
