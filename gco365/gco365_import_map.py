import sys
from lxml import etree
import subprocess



title = "map title"
filename = "tweet_test_map"
filebase = 'base_map'


file_final = './result/'+ filename + '.svg'



base = etree.parse(open('./base/'+ filebase +'.svg'))
root = base.getroot()

# remove name space
for elem in root.getiterator():
	elem.tag = etree.QName(elem).localname
etree.cleanup_namespaces(root)

#drop other style
root[0].remove( root[0][1])  # drop other css


for elem in root.getiterator():
	if elem.tag == 'text':
		if elem.text != None:
			if 'â€“' in elem.text:
				elem.text = elem.text.replace('â€“', '-')
			if 'â‰¥' in elem.text:
				elem.text = elem.text.replace('â‰¥', '≥')	
		else:
			root.remove(elem)
	

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

title = root[1].text


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





# move legend
root[4].set("transform", "translate(235.88221,-105.20411)")

#remove element




#group element 

group = etree.Element('g')
for child in root:
	if child.tag != 'defs':
		group.append(child)

root.append(group)
root[1].set("transform", "matrix(0.74487008,0,0,0.74487008,-61.426871,2.6436889)")



root.set("width", "1194.07649")
root.set("height", "595.50091")

dis = etree.parse(open('./base/gco_template_map.svg'))
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
base.write(file_final, pretty_print=False)
subprocess.Popen(['inkscape', '-f=' + file_final])
print("look on inkscape")

