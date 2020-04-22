import sys
from lxml import etree
import subprocess


heigth = 675 
title = ""

filename = "022_gco365"
filebase = 'map-graph6'

file_svg = './result/' + filename+ '.svg'
file_png = './result/'+ filename + '.png'

base = etree.parse(open('./base/'+ filebase +'.svg'))
root = base.getroot()

# remove name space
for elem in root.getiterator():
	elem.tag = etree.QName(elem).localname
etree.cleanup_namespaces(root)

#drop other style
root[0].remove( root[0][1])  # drop other .css


# remove element not use
for elem in root.getiterator():
	if elem.tag == 'text':
		if elem.text == None:
			root.remove(elem)
	
# remove element not use
for elem in root.getiterator():
	if elem.tag == 'text':
		if 'source' in elem.text:
			root.remove(elem)
		if 'Graph production' in elem.text:
			root.remove(elem)
		if 'World Health' in elem.text:
			root.remove(elem)
		if 'WHO All' in elem.text:
			root.remove(elem)

# correction of label
for elem in root.getiterator():
	if elem.tag == 'text':
		if 'â€“' in elem.text:
			elem.text = elem.text.replace('â€“', '-')
		if 'â‰¥' in elem.text:
			elem.text = elem.text.replace('â‰¥', '≥')

# get title from GCO
if title == "":
	title = root[1].text

# keep removing element not use
for child in root:
	if child.tag == 'image':
		root.remove(child)
	if child.tag == 'a':
		root.remove(child)
	if child.tag == 'use':
		root.remove(child)
	if child.tag == 'rect':
		root.remove(child)
	if child.tag == 'path':
		root.remove(child)
	if child.tag == 'text':
		root.remove(child)

# #get number of legend
# nb_legend = len(root[4])-6


# move legend
root[4].set("transform", "translate(235.88221,-103.4184)")



#group element 

group = etree.Element('g')
for child in root:
	if child.tag != 'defs':
		group.append(child)

root.append(group)
root[1].set("transform", "matrix(0.80150477,0,0,0.80150477,-116.37924,20.356044)")



root.set("width", "1200")
root.set("height", "675")

dis = etree.parse(open('./template/gco_template_map.svg'))
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

root.insert(root.index(root[0])+1,root_dis)
base.write(file_svg, pretty_print=False)


# export to png
subprocess.call(['inkscape', 
			'--without-gui', 
			'--export-height=' + str(heigth), 
			'--export-png=' + file_png, 
			file_svg], shell=True)


print(filename + ' is processed')
