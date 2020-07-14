import sys
import os
import re
from lxml import etree
import subprocess


regex = r"(.*)\.pdf"
regex_title = r"\d+-(.+)-fact-sheets.pdf"

for filebase in os.listdir('./factsheet/region'):
# parameter 
# name of the base file in the folder base
	
	print(filebase)

	file_title = re.sub(regex, r"\1", filebase)
	title =  re.sub(regex_title, r"\1", filebase).replace("-", " ")


	# name of the final file
	filename = "tw_bar-sex"+file_title

	#page of the graph
	page = '2'

	# graphic number 2: bar chart by sex
	# graphic number 3: bar chart by type
	graphic_number = 2

	# height of the graph can be edit
	# format is 16:9 (1200*)
	heigth = 675 


	file_svg = './factsheet/region/bar-sex/' + 'temp'+ '.svg'
	file_png = './factsheet/region/bar-sex/'+ filename + '.png'

	print('convert pdf to svg...')
	print('./base/'+ filebase)
	# PDF factsheet to svg
	subprocess.call([os.path.dirname(__file__) + '/pdf2svg/pdf2svg.exe', 
				'./factsheet/region/'+ filebase, 
				'./temp/temp.svg',
				page
				], shell=True)
	print('convertion done.')

	base = etree.parse(open('./temp/temp.svg'))
	root = base.getroot()

	# remove name space
	for elem in root.getiterator():
		elem.tag = etree.QName(elem).localname
	etree.cleanup_namespaces(root)

	# regroup element

	bool_group = False 
	counter = 0

	group = etree.Element('g')

	for child in root[1]:
		if child.tag == 'path':
			if ('rgb(11.799622%,25.898743%,45.098877%)' in child.get('style')) | ('rgb(11.759949%,25.878906%,45.098877%)' in child.get('style')):
				counter = counter+1
				if (counter == graphic_number):
					group = etree.Element('g')
					group.append(child)

		if (counter == graphic_number):
			# stop for last graph of the page
			if len(child)==1:
				if (child[0].tag == "path"):
					if ('rgb(4.299927%,50.19989%,71.798706%)' in child[0].get('style')) | ('rgb(4.309082%,50.19989%,71.759033%)' in child[0].get('style')):
						break
			# stop for last graph of the page
			if (child.get('style') != None):
				if ('rgb(4.299927%,50.19989%,71.798706%)' in child.get('style')) | ('rgb(4.309082%,50.19989%,71.759033%)' in child.get('style')):
					break

			group.append(child)
		if (counter != graphic_number):
			root[1].remove(child)



	for child in root:
		if (child.get('id') != None):
			if 'surface' in child.get('id'):
				root.remove(child)



	#position of graphic




	if graphic_number == 2: 
		group.set("transform", "matrix(2.4939928,0,0,2.4939928,-665.73439,-1324.7623)")
	elif graphic_number == 3: 
		group.set("transform", "matrix(2.4939928,0,0,2.4939928,-665.73439,-1961.8593)")

	root.append(group)

	root.set("width", "1200")
	root.set("height", "675")


	dis = etree.parse(open('./template/gco_template_landscape_bar.svg'))
	root_dis = dis.getroot()


	# remove name space
	for elem in root_dis.getiterator():
		elem.tag = etree.QName(elem).localname
	etree.cleanup_namespaces(root_dis)

	#manage banner
	for child in root_dis[3]:
		for elem in child:
			if elem.tag == 'text':
				if elem[0].text == 'title':
					elem[0].text = title

	root_dis[3].set("transform", "matrix(7.3819685,0,0,7.3819685,2942,1075)")

	root.insert(root.index(root[0])+1,root_dis[3])

	base.write(file_svg, pretty_print=False)
	#subprocess.Popen(['inkscape', '-f=' + file_svg])

	# export to png
	subprocess.call(['inkscape', 
				'--without-gui', 
				'--export-height=' + str(heigth), 
				'--export-png=' + file_png, 
				file_svg], shell=True)


	print(filename + ' is processed')
		