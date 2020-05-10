# coding: utf-8

# encoding=utf8  
import sys  


# python 2.x hack for encoding system
if (sys.version[0] == '2'):
	reload(sys)  
	sys.setdefaultencoding('utf8')
	

from lxml import etree
from copy import deepcopy
import subprocess
import re

# parameter 
# name of the base file in the folder base
filebase = 'semi_pie_2'

# name of the final file
filename = "pie_result"

# open svg in  inkscape
bool_inkscape = True

# print to png
bool_png = False

# if title edit, this will overwrite GCO title
title = ""

# cancer label font size et position
font_size=12
x_span = 5
y_span_label = 16
y_span_number = 30

# height of the graph can be edit
# format is 16:9 (1200*675)
heigth = 675 




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

# remove element not use
for elem in root:
	if elem.tag == 'image':
		root.remove(elem)
	elif elem.tag == 'a':
		root.remove(elem)
	elif elem.tag == 'rect':
		root.remove(elem)
	elif elem.tag == 'text':
		if elem.get("id") == "chart-title":
			title = elem.text
			print(title)
		elif elem.get("id") == "chart-total":
			total_number = elem.text.replace('Â', '')
			print(total_number)
		root.remove(elem)
	elif elem.tag == 'g':
		if elem.get("class") == "highcharts-tooltip":
			root.remove(elem)
		elif elem.get("class") == "highcharts-legend":
			root.remove(elem)
		elif elem.get("class") == "highcharts-legend":
			root.remove(elem)
		elif elem.get("class") == "highcharts-series-group":
			elem.remove(elem[0])
		else:
			for child in elem.getiterator():
				if child.tag == 'tspan':
					if 'Â' in child.text:
							child.text = child.text.replace('Â', '')


# group element 
group = etree.Element('g')
for child in root:
	if child.tag != 'defs':
		group.append(child)

root.append(group)


root[len(root)-1].set("transform", "matrix(1.1434323,0,0,1.1434323,-364.71899,-172.72555)")

root.set("width", "1200")
root.set("height", "675")

dis = etree.parse(open('./template/gco_template_semipie.svg'))
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
	if child.tag == 'text':
		if child[0].text == 'total':
			child[0].text = total_number

root.insert(root.index(root[0])+1,root_dis)


group_label = root[len(root)-1][len(root[len(root)-1])-1]


regex = r"(font-size:).*?px"
resub = r"\g<1>" + str(font_size) + r"px"

for elem in group_label:
	if (elem.tag == 'g'):
		# get text from cancer
		cancer_name = elem[0][0].text
		cancer_number = elem[0][1].text
		print(cancer_name)
		print(cancer_number)

		label_position =elem.get("transform")

		#update object form template
		group_cancer_temp = root_dis[3][6]
		div_cancer_label = group_cancer_temp[0]
		div_cancer_number = group_cancer_temp[1]

		div_cancer_label[0].text =  cancer_name
		div_cancer_number[0].text =  cancer_number

		old_style = div_cancer_label.get("style")
		temp_style =  re.sub(regex, resub, old_style)

		div_cancer_label.set("style", temp_style)



		old_style = div_cancer_number.get("style")
		temp_style =  re.sub(regex, resub, old_style)
		div_cancer_number.set("style", temp_style)


		group_cancer_temp.set("transform", label_position)

		group_cancer_temp[0].set("x", str(x_span))
		group_cancer_temp[0].set("y", str(y_span_label))

		group_cancer_temp[1].set("x", str(x_span))
		group_cancer_temp[1].set("y", str(y_span_number))


		#insert elem in pie

		group_label.insert(group_label.index(elem), deepcopy(group_cancer_temp))
		group_label.remove(elem)

base.write(file_svg, pretty_print=False)

if bool_inkscape:
	subprocess.Popen(['inkscape', '-f=' + file_svg])


if bool_png:
	subprocess.call(['inkscape', 
				'--without-gui', 
				'--export-height=' + str(heigth), 
				'--export-png=' + file_png, 
				file_svg], shell=True)


