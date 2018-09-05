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



for i in range(0,20):

    print('first' + str(i))

    if i < 18:
        for child in map[arr_female[i]]:
            old = child.get("style")
            new = old.replace('b62ca1', 'ff0004')
            child.set("style", new)

    for child in map[arr_male[i]]:
        old = child.get("style")
        new = old.replace('2c7bb6', 'ff0004')
        child.set("style", new)

    path_svg = './temp/first_' + str(i).zfill(2) +'.svg'
    path_png = './temp/first_' + str(i).zfill(2) +'.png'
    base.write(path_svg, pretty_print=False)
    subprocess.call(['inkscape','--without-gui', '--export-background=#ffffff', '--export-png='+path_png, path_svg], shell=True)





base = etree.parse(open(path_svg))
root = base.getroot()

map = root[3]



for i in range(0,13):

    print('second' + str(i))

    if i < 9:
        for child in map[arr_female[i]]:
            old = child.get("style")
            new = old.replace('ff0004', '000000')
            child.set("style", new)

    for child in map[arr_male[i]]:
        old = child.get("style")
        new = old.replace('ff0004', '000000')
        child.set("style", new)

    path_svg = './temp/second_' + str(i).zfill(2) +'.svg'
    path_png = './temp/second_' + str(i).zfill(2) +'.png'
    base.write(path_svg, pretty_print=False)
    subprocess.call(['inkscape','--without-gui', '--export-background=#ffffff', '--export-png='+path_png, path_svg], shell=True)







