# coding: utf-8

# encoding=utf8  
import sys  

# python 2.x hack for encoding system
if (sys.version[0] == '2'):
	reload(sys)  
	sys.setdefaultencoding('utf8')
	

from lxml import etree
import subprocess

# parameter 
# name of the base file in the folder base
filebase = 'semi_pie_cancer'

# name of the final file
filename = "pie_result"

# height of the graph can be edit
# format is 16:9 (1200*675)
heigth = 675 

# if title edit, this will overwrite GCO title
title = ""


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
for elem in root.getiterator():
	if elem.tag == 'text':
		if elem.text == None:
			root.remove(elem)

base.write(file_svg, pretty_print=False)
subprocess.Popen(['inkscape', '-f=' + file_svg])


	
# # remove element not use
# for elem in root.getiterator():
# 	if elem.tag == 'text':
# 		if (elem.text != None):
# 			if 'source' in elem.text:
# 				root.remove(elem)
# 			if 'Graph production' in elem.text:
# 				root.remove(elem)
# 			if 'World Health' in elem.text:
# 				root.remove(elem)
# 			if 'WHO All' in elem.text:
# 				root.remove(elem)

# # correction of label
# for elem in root.getiterator():
# 	if elem.tag == 'text':
# 		if (elem.text != None):
# 			if 'â€“' in elem.text:
# 				elem.text = elem.text.replace('â€“', '-')
# 			if 'â‰¥' in elem.text:
# 				elem.text = elem.text.replace('â‰¥', '≥')

# # get title from GCO
# if title == "":
# 	title = root[1].text

# # keep removing element not use
# for child in root:
# 	if child.tag == 'image':
# 		root.remove(child)
# 	if child.tag == 'a':
# 		root.remove(child)
# 	if child.tag == 'use':
# 		root.remove(child)
# 	if child.tag == 'rect':
# 		root.remove(child)
# 	if child.tag == 'path':
# 		root.remove(child)
# 	if child.tag == 'text':
# 		root.remove(child)

# # #get number of legend
# # nb_legend = len(root[4])-6


# # move legend
# root[4].set("transform", "translate(-33.11779,-168.4184)")

# # base.write(file_svg, pretty_print=False)


# # group element 

# group = etree.Element('g')
# for child in root:
# 	if child.tag != 'defs':
# 		group.append(child)

# root.append(group)
# root[1].set("transform", "matrix(0.80150477,0,0,0.80150477,99.244218,20.356044)")



# root.set("width", "1200")
# root.set("height", "675")

# dis = etree.parse(open('./template/gco_template_map.svg'))
# root_dis = dis.getroot()

# # remove name space
# for elem in root_dis.getiterator():
# 	elem.tag = etree.QName(elem).localname
# etree.cleanup_namespaces(root_dis)

# # edit text 
# for child in root_dis[3]:
# 	if child.tag == 'text':
# 		if child[0].text == 'title':
# 			child[0].text = title

# root.insert(root.index(root[0])+1,root_dis)
# base.write(file_svg, pretty_print=False)


# # export to png
# subprocess.call(['inkscape', 
# 			'--without-gui', 
# 			'--export-height=' + str(heigth), 
# 			'--export-png=' + file_png, 
# 			file_svg], shell=True)


# print(filename + ' is processed')

