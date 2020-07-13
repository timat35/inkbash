# coding: utf-8

# encoding=utf8  
import sys
import re
import os
import csv
import pandas as pd

# python 2.x hack for encoding system
if (sys.version[0] == '2'):
	reload(sys)  
	sys.setdefaultencoding('utf8')
	
from lxml import etree
import subprocess

regex = r"map_(.+)_(.+)_(.+)_(.+)"

cancer_name = pd.read_csv('./template/map_R_cancer_name.csv')


# parameter 
# name of the base file in the folder base
filebase = 'map_female_incidence_asr_Colorectum'

# name of the final file
filename = "tw_"+filebase

# height of the graph can be edit
# format is 16:9 (1200*)
heigth = 675 



# if title edit, this will overwrite GCO title
title_ASR = "Estimated age-standardized rates (World) in 2018"

title_sex = re.sub(regex, r"\1", filebase)
if title_sex == 'both':
	title_sex = 'both sexes'
else:
	title_sex = title_sex+'s'

title_type = re.sub(regex, r"\2", filebase)
title_key = re.sub(regex, r"\3", filebase)

if title_key == 'asr':
	title_base = 'Estimated age-standardized ' + title_type + ' rates (World) in 2018'
elif title_key == 'cumrisk':
	title_base = 'Estimated cumulative risk of ' + title_type + ' in 2018'


# title_cancer = cancer_name[cancer_name["file_cancer"] == re.sub(regex, r"\4", filebase)]
title_cancer = cancer_name[cancer_name["file_cancer"] == re.sub(regex, r"\4", filebase)]['cancer_name'].values[0]

title = title_base + ', ' + title_cancer + ', ' + title_sex

file_svg = './result/' + filename+ '.svg'
file_png = './result/'+ filename + '.png'

base = etree.parse(open('./base/'+ filebase +'.svg'))
root = base.getroot()

# remove name space
for elem in root.getiterator():
	elem.tag = etree.QName(elem).localname
etree.cleanup_namespaces(root)

# drop other style
# root[0].remove( root[0][1])  # drop other .css


root[2].remove(root[2][2])
root[2].remove(root[2][1])
root[2].remove(root[2][0])

	

# get title from GCO
if title == "":
	title = root[1].text






# group element 

group = etree.Element('g')
for child in root:
	if child.tag != 'defs':
		group.append(child)

root.append(group)
root[1].set("transform", "matrix(0.96858294,0,0,0.96858294,13.080029,7.3815728)")



root.set("width", "1200")
root.set("height", "675")

dis = etree.parse(open('./template/gco_template_map_R.svg'))
root_dis = dis.getroot()

# remove name space
for elem in root_dis.getiterator():
	elem.tag = etree.QName(elem).localname
etree.cleanup_namespaces(root_dis)

# edit text 
for child in root_dis[3]:
	if child.tag == 'text':
		if child[0].text == 'title':
			child[0].text = title

root.insert(root.index(root[0])+1,root_dis[3])
base.write(file_svg, pretty_print=False)


# export to png
subprocess.call(['inkscape', 
			'--without-gui', 
			'--export-height=' + str(heigth), 
			'--export-png=' + file_png, 
			file_svg], shell=True)


print(filename + ' is processed')

