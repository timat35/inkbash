import sys
import copy
from lxml import etree
import math
import subprocess
import csv

graph_title = 'South and Central America'

for i in range(0,3):
    subprocess.call(['inkscape','--without-gui', '--export-plain-svg=./temp/pie'+str(i)+'.svg', './temp/pie'+str(i)+'.eps'], shell=True)
    print('pie'+str(i) + " convert")


label_file = open('./temp/cancer_info.csv', newline='')
cancer_list = list(csv.reader(label_file, delimiter=',', quotechar='"'))
nb_label = int((len(cancer_list)-1)/3)

print(nb_label)

lab_cancer1 = ["none"]*(nb_label)
lab_cases1= [0]*(nb_label)
lab_percent1= [0]*(nb_label)

lab_cancer2 = ["none"]*(nb_label)
lab_cases2= [0]*(nb_label)
lab_percent2= [0]*(nb_label)

lab_cancer3 = ["none"]*(nb_label)
lab_cases3= [0]*(nb_label)
lab_percent3= [0]*(nb_label)




i = 0

for x in cancer_list[1:11]:

    lab_cancer1[i] = x[0]
    lab_cases1[i] = int(x[1])
    i = i +1

lab_percent1 = [round(x*100 / sum(lab_cases1),1) for x in lab_cases1]


if (abs(sum(lab_percent1) - 100) > 0.05):
    lab_percent1[nb_label-1] =  round(lab_percent1[nb_label-1] + (100 - round(sum(lab_percent1),1)),1)

i = 0

for x in cancer_list[11:21]:

    lab_cancer2[i] = x[0]
    lab_cases2[i] = int(x[1])
    i = i +1

lab_percent2 = [round(x*100 / sum(lab_cases2),1) for x in lab_cases2]


if (abs(sum(lab_percent2) - 100) > 0.05):
    lab_percent2[nb_label-1] =  round(lab_percent2[nb_label-1] + (100 - round(sum(lab_percent2),1)),1)


i = 0

for x in cancer_list[21:31]:

    lab_cancer3[i] = x[0]
    lab_cases3[i] = int(x[1])
    i = i +1

lab_percent3 = [round(x*100 / sum(lab_cases3),1) for x in lab_cases3]


if (abs(sum(lab_percent3) - 100) > 0.05):
    lab_percent3[nb_label-1] =  round(lab_percent3[nb_label-1] + (100 - round(sum(lab_percent3),1)),1)

lab_total = [0,0,0]
pie_size= [0,0,0]
pie_file = ["./temp/pie0.svg", "./temp/pie1.svg", "./temp/pie2.svg"]
pie_x_scale = ["-2.5593047", "356.80114", "698.53954"]

lab_total[0] = round(sum(lab_cases1),1)
lab_total[1] = round(sum(lab_cases2),1)
lab_total[2] = round(sum(lab_cases3),1)


pie_size[0] = math.sqrt( lab_total[0]/lab_total[2]) * 400
pie_size[1] = math.sqrt(lab_total[1]/lab_total[2]) * 400
pie_size[2] = 400

print(pie_size)

file_base = './3pie_base.svg'

base = etree.parse(open(file_base))
root = base.getroot()

for i in range(0,3):


    base_pie = etree.parse(open(pie_file[i]))
    root_pie = base_pie.getroot()
    pie = root_pie[2]

    pie[0].remove(pie[0][0])
    pie[0].remove(pie[0][(nb_label)*2])

    temp = pie[0]
    scale = (pie_size[i]/268.533)*0.1

    temp.set("transform", "matrix(" + str(scale) + ",0,0,"+ str(scale*-1) + "," + str(i*400) + ",0)")

    root.append(temp)



for child in root[3]:
    if len(child.getchildren()) == 1:
        for i in range(0,11):
            if child[0].text == "label" + str(i+1):
                child[0].text = lab_cancer1[i]
            if child[0].text == "label" + str(i+1+10):
                child[0].text = lab_cancer2[i]
            if child[0].text == "label" + str(i+1+20):
                child[0].text = lab_cancer3[i]
            if child[0].text == str(i+1)+"%":
                child[0].text = str(lab_percent1[i])+"%"
            if child[0].text == str(i+1+10)+"%":
                child[0].text = str(lab_percent2[i])+"%"
            if child[0].text == str(i+1+20)+"%":
                child[0].text = str(lab_percent3[i])+"%"


        if child[0].text == "Title":
            child[0].text = graph_title
    if len(child.getchildren()) == 2:
        for i in range(0,3):
            if child[0].text == str((i+1)*1000):
                if lab_total[i] > 1000000:
                    child[0].text = str((round(lab_total[i]/1000000,1))) + " million"
                else:
                    child[0].text = str(int(round(lab_total[i]/1000,0))*1000)





base.write('./test.svg', pretty_print=False)




