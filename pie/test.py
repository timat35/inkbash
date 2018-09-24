import sys
import copy
from lxml import etree
import math
import subprocess
import csv

graph_title = 'China'
file_eps = './temp.eps'
file_svg = file_eps.replace('.eps','.svg')
nb_top = 5

#subprocess.call(['inkscape','--without-gui', '--export-plain-svg='+file_svg, file_eps], shell=True)



label_file = open('./temp/cancer_info.csv', newline='')
cancer_list = list(csv.reader(label_file, delimiter=',', quotechar='"'))
nb_top = len(cancer_list)-2


lab_cancer = ["none"]*(nb_top+1)
lab_cases= [0]*(nb_top+1)

i = 0

for x in cancer_list[1:]:

    lab_cancer[i] = x[0]
    lab_cases[i] = int(x[1])
    i = i +1

lab_percent = [round(x*100 / sum(lab_cases),1) for x in lab_cases]

print(lab_percent)
print(sum(lab_percent))

file_base = './pie_top'+str(nb_top)+'_base.svg'

base = etree.parse(open(file_base))
root = base.getroot()

base_pie = etree.parse(open(file_svg))
root_pie = base_pie.getroot()
pie = root_pie[2]

pie[0].remove(pie[0][0])
pie[0].remove(pie[0][(nb_top+1)*2])


temp = pie[0]
temp.set("transform", "matrix(0.13333333,0,0,-0.13333333,-11.129944,442.08418)")
root.append(temp)



temp = copy.copy(root[3])
root.remove(root[3])
root.append(temp)

for child in root:
    for new in child:
        print(new)


base.write('./test.svg', pretty_print=False)






