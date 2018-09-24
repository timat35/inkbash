import sys
import copy
from lxml import etree
import math
import subprocess
import csv

graph_title = 'Europe'
file_eps = './temp/temp.eps'
file_svg = file_eps.replace('.eps','.svg')


#subprocess.call(['inkscape','--without-gui', '--export-plain-svg='+file_svg, file_eps], shell=True)



label_file = open('./temp/cancer_info.csv', newline='')
cancer_list = list(csv.reader(label_file, delimiter=',', quotechar='"'))
nb_top = len(cancer_list)-2


lab_cancer = ["none"]*(nb_top+1)
lab_cases= [0]*(nb_top+1)
lab_percent= [0]*(nb_top+1)

i = 0

for x in cancer_list[1:]:

    lab_cancer[i] = x[0]
    lab_cases[i] = int(x[1])
    i = i +1

lab_percent = [round(x*100 / sum(lab_cases),1) for x in lab_cases]



if (abs(sum(lab_percent) - 100) > 0.05):
    lab_percent[nb_top] =  round(lab_percent[nb_top] + (100 - round(sum(lab_percent),1)),1)



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

for child in root[4]:
    for new in child:
        for i in range(0,(nb_top+1)):
            if new[0].text == str(i+1)+"%":
                new[0].text = str(lab_percent[i])+"%"
            if new[0].text == 'label'+str(i+1):
                new[0].text = lab_cancer[i]
        if new[0].text == "Title":
            new[0].text = graph_title
        print(new[0].text)


base.write('./done/pie_top'+str(nb_top)+'_'+graph_title+'.svg', pretty_print=False)






