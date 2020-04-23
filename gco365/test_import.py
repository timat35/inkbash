import sys
from lxml import etree
import subprocess


# pour l'instant un seul template available: 1: landscape
template = 1

# "png" our "svg"
import_base = "png"
text1 = "upper title"
text2 = "main title"
text3 = "subtitle"
filename = "tweet_test_bar"
filebase = 'base_bar'


file_final = './result/'+ filename + '.svg'


if import_base == "svg":
	base = etree.parse(open('./base/'+ filebase +'.svg'))
	root = base.getroot()

	# remove name space
	for elem in root.getiterator():
		elem.tag = etree.QName(elem).localname
	etree.cleanup_namespaces(root)

	#drop other style
	root[0].remove( root[0][1])  # drop other css


	for child in root:
		if child.tag == 'image':
			root.remove(child)
		if child.tag == 'a':
			root.remove(child)
		if child.tag == 'text':
			if child.text != None:
				if 'Data source' in child.text:
					root.remove(child)
				if 'Graph production' in child.text:
					root.remove(child)
				if 'International Agency' in child.text:
					root.remove(child)

	

	# group element 

	group = etree.Element('g')
	for child in root:
		if child.tag != 'defs':
			group.append(child)

	root.append(group)
	root[1].set("transform", "matrix(0.43424561,0,0,0.43424561,221.08716,113.53036)")


	if template == 1:
		root.set("width", "1194.07649")
		root.set("height", "595.50091")


if import_base == "png":
	subprocess.run(['inkscape', 
		'-z',
		'-f', './base/'+ filebase + '.png',
		'-l', './temp/temp.svg'])

	base = etree.parse(open('./temp/temp.svg'))
	root = base.getroot()
	for elem in root.getiterator():
		elem.tag = etree.QName(elem).localname
	etree.cleanup_namespaces(root)


	for child in root:
		if (child.tag == 'image'):
			temp_img = child
			base_width = int(temp_img.get('width'))
			base_height = int(temp_img.get('height'))
			new_width = 197.9231
			new_heigth = new_width*base_height/base_width
			temp_img.set("width", str(new_width))
			temp_img.set("height", str(new_heigth))
			temp_img.set("x", "59.004814")
			temp_img.set("y", "16.536493")



if template == 1:
	dis = etree.parse(open('./base/gco_template_landscape.svg'))

root_dis = dis.getroot()

# remove name space
for elem in root_dis.getiterator():
	elem.tag = etree.QName(elem).localname
etree.cleanup_namespaces(root_dis)

# edit text 
for child in root_dis[3]:
	if child.tag == 'text':
		if child[0].text == 'text1':
			child[0].text = text1
		if child[0].text == 'text2':
			child[0].text = text2
		if child[0].text == 'text3':
			child[0].text = text3



# root.append(root_dis)
if import_base == "svg":
	root.insert(root.index(root[0])+1,root_dis)
	base.write(file_final, pretty_print=False)
	subprocess.Popen(['inkscape', '-f=' + file_final])
	print("look on inkscape")


if import_base == "png":
	root_dis.append(temp_img)

	dis.write(file_final, pretty_print=False)
	subprocess.Popen(['inkscape', '-f=' + file_final])
	print("look on inkscape")

