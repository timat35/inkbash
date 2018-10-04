import sys
import re
import os
from lxml import etree
import subprocess
import math



area = [14,15,16,17]
y = [0]*len(area)
x = [0]*len(area)

for i in range(0,len(area)):
    y[i] = i

dpi = 200

dir_file = "./temp"

panel_base = etree.parse('./panel_base.svg')
panel_root = panel_base.getroot()



for file_base in os.listdir(dir_file):

    print(file_base)
    pattern = "^.+_(\d+)_.+$"
    regex = re.search(pattern, file_base)
    area_code = regex.group(1)

    path_eps = os.path.join(dir_file, file_base)
    subprocess.call(['inkscape','--without-gui', '--export-plain-svg=./temp.svg', path_eps], shell=True)

    base = etree.parse('./temp.svg')
    root = base.getroot()
    map = root[2][0]

    map.remove(map[0])

    for child in map:
        if len(child) > 0:
            for text in child:
                if not(re.search("[^a-zA-Z*]", text[0].text)):
                    country_label = text[0].text[:]


    country_label = country_label.replace("*", "")
    print(country_label)

    base.write('./done/prediction_testis_'+country_label+'.svg', pretty_print=False)
    subprocess.call(['inkscape','--without-gui', '-d' + str(dpi) ,'--export-background=#ffffff','--export-png=./done/prediction_testis_'+country_label+'.png', './done/prediction_testis_'+country_label+'.svg'], shell=True)

    temp = root[:][2]


    ind = area.index(int(area_code))
    print(ind)

    x_trim = str(x[ind]*690)
    y_trim=str(960 + (y[ind]*1000))

    temp.set("transform", "matrix(1.3333333,0,0,-1.3333333,"+x_trim+","+y_trim+")")

    x[ind] = x[ind]+1

    if x[ind] == 7:
        x[ind] = 0
        for i in range(ind,len(area)):
            y[i] = y[i]+1


    panel_root.append(temp)



panel_base.write('./test.svg', pretty_print=False)


print(i)









