import sys
import math
from lxml import etree
import random
import subprocess

file_base = './temp/first_23.svg'

base = etree.parse(open(file_base))
root = base.getroot()



map = root[3]
print(map)



arr_female = []
arr_male = []


#get the element index
for child in map:

    temp = child.get("style")
    print(temp)
    if 'ff0004' in str(temp):
        arr_female.append(map.getchildren().index(child))
    if 'ff0003' in str(temp):
        arr_male.append(map.getchildren().index(child))

for i in range(0,15):

    print('second' + str(i))

    if i < 12:
        index_female = random.randint(0,len(arr_female)-1)
        for child in map[arr_female[index_female]]:
            old = child.get("style")
            new = old.replace('ff0004', '000000')
            child.set("style", new)
        arr_female.pop(index_female)

    index_male = random.randint(0,len(arr_male)-1)
    for child in map[arr_male[index_male]]:
        old = child.get("style")
        new = old.replace('ff0003', '000000')
        child.set("style", new)
    arr_male.pop(index_male)

    path_svg = './temp/second_' + str(i).zfill(2) +'.svg'
    path_png = './temp/second_' + str(i).zfill(2) +'.png'
    base.write(path_svg, pretty_print=False)
    subprocess.call(['inkscape','--without-gui', '--export-background=#ffffff','--export-dpi=150', '--export-png='+path_png, path_svg], shell=True)







