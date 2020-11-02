import sys
import os
import re
from lxml import etree
import subprocess


regex = r"(.*)\.pdf"
regex_title = r"\d+-(.+)-fact-sheets.pdf"

for filebase in os.listdir('C:/Data/Globocan2020/factsheet/populations'):
# parameter 
# name of the base file in the folder base
	

	print(filebase)
	country_name = re.sub(regex_title, r"\1", filebase)  
	country_file = re.sub(r"\W", r"", country_name)  
	filename =  "panel_incidence_" +country_file
	print(filename)

	title =  re.sub(regex_title, r"\1", filebase).replace("-", " ")

	#page of the graph
	page = '1'

	# graphic number 2: pie chart new cases both sexes
	# graphic number 3: pie chart new cases males
	# graphic number 4: pie chart new cases females

	#2,3,4

	# height of the graph can be edit
	# format is 16:9 (1200*)
	heigth = 1200 


	file_svg = 'C:/Data/Globocan2020/factsheet/populations/panel/' + 'temp'+ '.svg'
	file_png = 'C:/Data/Globocan2020/factsheet/populations/panel/'+ filename + '.png'

	print('convert pdf to svg...')
	# PDF factsheet to svg
	subprocess.call([os.path.dirname(__file__) + '/pdf2svg/pdf2svg.exe', 
				'C:/Data/Globocan2020/factsheet/populations/'+ filebase, 
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

	counter = 0

	group = etree.Element('g')



	# regroup element

	counter = 0
	bool_add = False
	bool_mark = False
	group = etree.Element('g')


	for child in root[1]:


		if child.tag == 'path':
			if ('rgb(11.799622%,25.898743%,45.098877%)' in child.get('style')) | ('rgb(11.759949%,25.878906%,45.098877%)' in child.get('style')):
				counter = counter+1
				if (counter == 2):
					bool_add = True
					group.append(child)
		
		if child.tag == 'g':
			if child[0].tag == 'use':
				if ('rgb(4.299927%,50.19989%,71.798706%)' in child.get('style')) | ('rgb(4.309082%,50.19989%,71.759033%)' in child.get('style')):
					bool_mark = True

		if child.tag == 'g':
			if child[0].tag == 'use':
				if ('rgb(100%,100%,100%)' in child.get('style')):
					if (bool_mark):
						break



		if bool_add:
			group.append(child)
		else:
			root[1].remove(child)


	# remove some element
	counter_line = 0
	counter = 0

	for child in group:
		if child.tag == 'path':
			if ('rgb(79.998779%,79.998779%,79.998779%)' in child.get('style')):
				counter_line = counter_line+1
				if (counter_line == 4):
					group.remove(child)
				if (counter_line > 7):
					group.remove(child)

			if ('rgb(11.799622%,25.898743%,45.098877%)' in child.get('style')) | ('rgb(11.759949%,25.878906%,45.098877%)' in child.get('style')):
				counter = counter+1
				if (counter == 6):
					group.remove(child)

	for child in root:
		if (child.get('id') != None):
			if 'surface' in child.get('id'):
				root.remove(child)

	nb_rect = 0
	for child in group:
		if child.tag == 'path':
			if ('rgb(11.799622%,25.898743%,45.098877%)' in child.get('style')) | ('rgb(11.759949%,25.878906%,45.098877%)' in child.get('style')):
				nb_rect = nb_rect+1
				if nb_rect == 6:
					group.remove(child)



	#position of graphic
	group.set("transform", "matrix(1.4475401,0,0,1.4475401,-199.62875,-122.28937)")

	root.append(group)

	root.set("width", "1200")
	root.set("height", "1200")


	dis = etree.parse(open('./template/gco_template_square_panel.svg'))
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



	root_dis[3].set("transform", "matrix(3.9748031,0,0,3.9748031,1799.5046,1140.4753)")

	root.insert(root.index(root[0])+1,root_dis[3])

	base.write(file_svg, pretty_print=False)
	# subprocess.Popen(['inkscape', '-f=' + file_svg])

	# export to png
	subprocess.call(['inkscape', 
				'--without-gui', 
				'--export-height=' + str(heigth), 
				'--export-png=' + file_png, 
				file_svg], shell=True)


	print(filename + ' is processed')
				