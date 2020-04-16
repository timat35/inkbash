import sys
from lxml import etree
import subprocess


# print(str(sys.argv[2]))
# print(str(sys.argv[3]))
template = 1
text1 = "upper title"
text2 = "main title"
text3 = "subtitle"
filename = "tweet_test_bar"
filebase = 'base_bar'


file_final = './result/'+ filename + '.svg'


base = etree.parse(open('./base/'+ filebase +'.svg'))
root = base.getroot()

# remove name space
for elem in root.getiterator():
	elem.tag = etree.QName(elem).localname
etree.cleanup_namespaces(root)

#drop other style
root[0].remove( root[0][1])  # drop other css


# for elem in root.getiterator():
# 	if elem.tag == 'text':
# 		print(elem.text)
# fix for css
# print(root[0].attrib)
# root.append(root[0][0]) #copy css ot root
# 

for child in root:
	print(child.tag)
	if child.tag == 'image':
		root.remove(child)
	if child.tag == 'a':
		root.remove(child)
	if child.tag == 'text':
		print(child.text)
		if child.text != None:
			if 'Data source' in child.text:
				root.remove(child)
			if 'Graph production' in child.text:
				root.remove(child)
			if 'International Agency' in child.text:
				root.remove(child)

for child in root:
	# print(child.tag)
	if child.tag == 'text':
		print(child.text)

if template == 1:
	root.set("width", "1194.07649")
	root.set("height", "595.50091")

# group element 

group = etree.Element('g')
for child in root:
	if child.tag != 'defs':
		group.append(child)

root.append(group)
root[1].set("transform", "matrix(0.43424561,0,0,0.43424561,221.08716,113.53036)")

		


dis = etree.parse(open('./base/gco_template_landscape.svg'))
root_dis = dis.getroot()

# remove name space
for elem in root_dis.getiterator():
	elem.tag = etree.QName(elem).localname
etree.cleanup_namespaces(root_dis)

# edit text 
for child in root_dis[3]:
	if child.tag == '{http://www.w3.org/2000/svg}text':
		if child[0].text == 'text1':
			child[0].text = text1
		if child[0].text == 'text2':
			child[0].text = text2
		if child[0].text == 'text3':
			child[0].text = text3

root.insert(root.index(root[0])+1,root_dis)


base.write(file_final, pretty_print=False)
# subprocess.Popen(['inkscape', '-f=' + file_final])
print("look on inkscape")

