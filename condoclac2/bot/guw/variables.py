from pprint import pprint
import re

datapath = '/home/robb/Desktop/customer_form.txt'

d = {}
with open(datapath, 'r') as file:
    string = file.read().replace(' ', '')
    clean_str = re.sub('\n+', '\n', string)
    arr = re.split('\n', clean_str)
    for item in arr:
        colon_splited = item.split(':')
        if colon_splited[0] != '':
            d[colon_splited[0]] = colon_splited[1]

pprint(d)


