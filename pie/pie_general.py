import copy
from lxml import etree
import subprocess
import csv

graph_title = ''
file_eps = './temp/temp.eps'
file_svg = file_eps.replace('.eps', '.svg')

minLabel = False

print(file_eps)
subprocess.call(['inkscape','--without-gui', '--export-plain-svg='+file_svg, file_eps], shell=True)
print(file_svg)


label_file = open('./temp/cancer_info.csv', newline='')
cancer_list = list(csv.reader(label_file, delimiter=',', quotechar='"'))
nb_top = len(cancer_list)-1

print(nb_top)

file_final = './done/pie_'+graph_title+'.svg'


lab_cancer = ["none"]*(nb_top)
lab_cases= [0]*(nb_top)
lab_percent= [0]*(nb_top)

i = 0

for x in cancer_list[1:]:

    lab_cancer[i] = x[0]
    lab_cases[i] = int(x[1])
    i = i +1

lab_percent = [round(x*100 / sum(lab_cases),1) for x in lab_cases]



if (abs(sum(lab_percent) - 100) > 0.05):
    lab_percent[nb_top-1] =  round(lab_percent[nb_top-1] + (100 - round(sum(lab_percent),1)),1)


if minLabel:
    file_base = './pie_base_minlabel.svg'
else:
    file_base = './pie_base.svg'

base = etree.parse(open(file_base))
root = base.getroot()

base_pie = etree.parse(open(file_svg))
root_pie = base_pie.getroot()
pie = root_pie[2]

pie[0].remove(pie[0][0])
pie[0].remove(pie[0][(nb_top)*2])


temp = pie[0]
temp.set("transform", "matrix(0.13333333,0,0,-0.13333333,-11.129944,442.08418)")
root.append(temp)



temp = copy.copy(root[3])
root.remove(root[3])
root.append(temp)

j=0


for child in root[4]:
    for new in child:
        for i in range(0,(nb_top)):
            if new[0].text == str(i+1)+"%":
                new[0].text = str(lab_percent[i])+"%"
            if new[0].text == 'label'+str(i+1):
                new[0].text = lab_cancer[i]
        if new[0].text == "Title":
            new[0].text = graph_title
        if j <= (nb_top*2):
            print(new[0].text)
            j=j+1
        else:
            child.remove(new)


base.write(file_final, pretty_print=False)
subprocess.Popen(['inkscape', '-f=' + file_final])
print("look on inkscape")





