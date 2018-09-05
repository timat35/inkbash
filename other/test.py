import sys
import math
from lxml import etree
import random
import subprocess

file_base = './multi_male_female_proportion_allsites_base.svg'

base = etree.parse(open(file_base))
root = base.getroot()
subprocess.call(['inkscape','--without-gui', '--export-background=#ffffff','--export-png=./temp/base.png', file_base], shell=True)



map = root[3]

arr_female = []
arr_male = []
arr_female2 = []
arr_male2 = []


#get the element index
for child in map:

    temp = child.get("style")
    if 'b62ca1' in str(temp):
        arr_female.append(map.getchildren().index(child))
    if '2c7bb6' in str(temp):
        arr_male.append(map.getchildren().index(child))



for i in range(0,24):

    print('first' + str(i))

    if i < 20:
        index_female = random.randint(0,len(arr_female)-1)
        for child in map[arr_female[index_female]]:
            old = child.get("style")
            new = old.replace('b62ca1', 'ff0004')
            child.set("style", new)
        arr_female2.append(arr_female[index_female])
        arr_female.pop(index_female)


    index_male = random.randint(0,len(arr_male)-1)
    for child in map[arr_male[index_male]]:
        old = child.get("style")
        new = old.replace('2c7bb6', 'ff0004')
        child.set("style", new)
    arr_male2.append(arr_male[index_male])
    arr_male.pop(index_male)

    path_svg = './temp/first_' + str(i).zfill(2) +'.svg'
    path_png = './temp/first_' + str(i).zfill(2) +'.png'
    base.write(path_svg, pretty_print=False)
    subprocess.call(['inkscape','--without-gui', '--export-background=#ffffff', '--export-png='+path_png, path_svg], shell=True)

    print(arr_female2)
    print(arr_male2)




base = etree.parse(open(path_svg))
root = base.getroot()

map = root[3]



for i in range(0,15):

    print('second' + str(i))

    if i < 12:
        index_female = random.randint(0,len(arr_female2)-1)
        for child in map[arr_female2[index_female]]:
            old = child.get("style")
            new = old.replace('ff0004', '000000')
            child.set("style", new)
        arr_female2.pop(index_female)

    index_male = random.randint(0,len(arr_male2)-1)
    for child in map[arr_male2[index_male]]:
        old = child.get("style")
        new = old.replace('ff0004', '000000')
        child.set("style", new)
    arr_male2.pop(index_male)

    path_svg = './temp/second_' + str(i).zfill(2) +'.svg'
    path_png = './temp/second_' + str(i).zfill(2) +'.png'
    base.write(path_svg, pretty_print=False)
    subprocess.call(['inkscape','--without-gui', '--export-background=#ffffff', '--export-png='+path_png, path_svg], shell=True)







