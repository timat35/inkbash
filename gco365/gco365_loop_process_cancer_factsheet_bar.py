import sys
import os
import re
from lxml import etree
import subprocess


regex = r"(.*)\.pdf"
regex_cancer_name = r".*?-(.*)-fact.*\.pdf"




#page of the graph
page = '2'

# graphic number 3: bar chart by sex
# graphic number 4: bar chart by type
graphic_number = 3

if graphic_number == 3 :
	graph_type = 'bar_male_female_incidence_region'
elif graphic_number == 4 :
	graph_type = 'bar_incidence_mortality_region'



for filebase in os.listdir('C:/Data/Globocan2020/factsheet/cancers'):
# parameter 
# name of the base file in the folder base
	
	print(filebase)

	cancer_name = re.sub(regex_cancer_name, r"\1", filebase)  
	cancer_file = re.sub(r"\W", r"", cancer_name)  

	

	filename =  "tw_factsheet_" + graph_type + "_"+cancer_file

	

	# height of the graph can be edit
	# format is 16:9 (1200*)
	heigth = 1200 


	file_svg = './temp/temp_result.svg'
	file_png = 'C:/Projects/tweetO/img_sort/cancer/'+graph_type+'/'+ filename + '.png'

	print('convert pdf to svg...')
	# PDF factsheet to svg
	subprocess.call([os.path.dirname(__file__) + '/pdf2svg/pdf2svg.exe', 
				'C:/Data/Globocan2020/factsheet/cancers/'+ filebase , 
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
			if ('rgb(11.759949%,25.878906%,45.098877%)' in child.get('style')):
				counter = counter+1
				if (counter == graphic_number):
					group = etree.Element('g')
					group.append(child)

		if (counter == graphic_number):
			# stop for last graph of the page
			if len(child)==1:
				if (child[0].tag == "path"):
					if ('rgb(4.309082%,50.19989%,71.759033%)' in child[0].get('style')):
						break
			# stop for last graph of the page
			if (child.get('style') != None):
				if ('rgb(4.309082%,50.19989%,71.759033%)' in child.get('style')):
					break

			group.append(child)
		if (counter != graphic_number):
			root[1].remove(child)


	for child in root:
		if (child.get('id') != None):
			if 'surface' in child.get('id'):
				root.remove(child)

	#position of graphic

	if graphic_number == 3: 
		group.set("transform", "matrix(2.9939928,0,0,2.9939928,-269.43608,-2416.1767)")
	elif graphic_number == 4: 
		group.set("transform", "matrix(2.9939928,0,0,2.9939928,-1508.1655,-2416.1767)")

	root.append(group)

	root.set("width", "1200")
	root.set("height", "1200")


	dis = etree.parse(open('./template/gco_template_square.svg'))
	root_dis = dis.getroot()



	# remove name space
	for elem in root_dis.getiterator():
		elem.tag = etree.QName(elem).localname
	etree.cleanup_namespaces(root_dis)

	#manage banner
	for child in root_dis[3]:
		for elem in child:
			if elem.tag == 'text':
				child.remove(elem)
			if elem.tag == 'path':
				child.remove(elem)
					

	root_dis[3].set("transform", "matrix(3.9745509,0,0,3.9745509,1799.4387,1140.4029)")

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

graphic_number = 4

if graphic_number == 3 :
	graph_type = 'bar_male_female_incidence_region'
elif graphic_number == 4 :
	graph_type = 'bar_incidence_mortality_region'



for filebase in os.listdir('C:/Data/Globocan2020/factsheet/cancers'):
# parameter 
# name of the base file in the folder base
	
	print(filebase)

	cancer_name = re.sub(regex_cancer_name, r"\1", filebase)  
	cancer_file = re.sub(r"\W", r"", cancer_name)  

	

	filename =  "tw_factsheet_" + graph_type + "_"+cancer_file

	

	# height of the graph can be edit
	# format is 16:9 (1200*)
	heigth = 1200 


	file_svg = './temp/temp_result.svg'
	file_png = 'C:/Projects/tweetO/img_sort/cancer/'+graph_type+'/'+ filename + '.png'

	print('convert pdf to svg...')
	# PDF factsheet to svg
	subprocess.call([os.path.dirname(__file__) + '/pdf2svg/pdf2svg.exe', 
				'C:/Data/Globocan2020/factsheet/cancers/'+ filebase , 
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
			if ('rgb(11.759949%,25.878906%,45.098877%)' in child.get('style')):
				counter = counter+1
				if (counter == graphic_number):
					group = etree.Element('g')
					group.append(child)

		if (counter == graphic_number):
			# stop for last graph of the page
			if len(child)==1:
				if (child[0].tag == "path"):
					if ('rgb(4.309082%,50.19989%,71.759033%)' in child[0].get('style')):
						break
			# stop for last graph of the page
			if (child.get('style') != None):
				if ('rgb(4.309082%,50.19989%,71.759033%)' in child.get('style')):
					break

			group.append(child)
		if (counter != graphic_number):
			root[1].remove(child)


	for child in root:
		if (child.get('id') != None):
			if 'surface' in child.get('id'):
				root.remove(child)

	#position of graphic

	if graphic_number == 3: 
		group.set("transform", "matrix(2.9939928,0,0,2.9939928,-269.43608,-2416.1767)")
	elif graphic_number == 4: 
		group.set("transform", "matrix(2.9939928,0,0,2.9939928,-1508.1655,-2416.1767)")

	root.append(group)

	root.set("width", "1200")
	root.set("height", "1200")


	dis = etree.parse(open('./template/gco_template_square.svg'))
	root_dis = dis.getroot()



	# remove name space
	for elem in root_dis.getiterator():
		elem.tag = etree.QName(elem).localname
	etree.cleanup_namespaces(root_dis)

	#manage banner
	for child in root_dis[3]:
		for elem in child:
			if elem.tag == 'text':
				child.remove(elem)
			if elem.tag == 'path':
				child.remove(elem)
					

	root_dis[3].set("transform", "matrix(3.9745509,0,0,3.9745509,1799.4387,1140.4029)")

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


