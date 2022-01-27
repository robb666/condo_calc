from pprint import pprint
import re

datapath = '/home/robb/Desktop/customer_form.txt'

with open(datapath, 'r') as file:
    dicti = re.split(' |\n+', file.read())
    print(dicti)
    di = {dicti[num].rstrip(':'): dicti[num + 1] for num in range(len(dicti))
          if ':' in dicti[num] and ':' not in dicti[num + 1]}


pprint(di)


