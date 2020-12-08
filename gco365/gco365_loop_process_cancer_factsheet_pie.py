import sys
import os
import re
from lxml import etree
import subprocess

regex = r"(.*)\.pdf"
regex_cancer_name = r".*?-(.*)-fact.*\.pdf"


# #page of the graph
page = '1'

# # graphic number 1: pie chart new cases
# # graphic number 2: pie chart deaths
graphic_number = 1

if graphic_number == 1 :
	graph_type = 'pie_bar_rank_incidence'
elif graphic_number == 2 :
	graph_type = 'pie_bar_rank_mortality'


files = [f for f in os.listdir('C:/Data/Globocan2020/factsheet/cancers') if os.path.isfile(os.path.join('C:/Data/Globocan2020/factsheet/cancers',f))]
# files = [f for f in os.listdir('C:/Data/Globocan2020/factsheet/cancers') if f == "1-Lip-oral-cavity-fact-sheet.pdf"]
for filebase in files:

	# print(filebase)

	print(filebase)


	cancer_name = re.sub(regex_cancer_name, r"\1", filebase)  
	cancer_file = re.sub(r"\W", r"", cancer_name)  
	filename =  "tw_factsheet_" + graph_type + "_"+cancer_file
	print(filename)

	title = cancer_name.replace('-', ' ') + ' cancer'
	title = re.sub(r"(.*cancer) cancer", r"\1", title)
	print(title)

	# name of the final file
	# filename = "031_gco365"


	# height of the graph can be edit
	# format is 16:9 (1200*)
	heigth = 1200 


	file_svg = './temp/temp_result.svg'
	file_png = 'C:/Projects/tweetO/img_sort/cancer/'+graph_type+'/'+ filename + '.png'

	print(file_svg)
	print('C:/Data/Globocan2020/factsheet/cancers/'+ filebase)

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

	counter = 0

	group = etree.Element('g')


	for child in root[1]:


		if child.tag == 'path':

			if ('rgb(11.759949%,25.878906%,45.098877%)' in child.get('style')):
				counter = counter+1
				if (counter == graphic_number):
					group.append(child)

		if (counter == graphic_number):
			# stop for last graph of the page
			if len(child)==1:
				if (child[0].tag == "path"):
					if ('rgb(4.309082%,50.19989%,71.759033%)' in child[0].get('style')):
						break

			group.append(child)
		if (counter != graphic_number):
			if (child.getparent() == root[1]):
				root[1].remove(child)



	for child in root:
		if (child.get('id') != None):
			if 'surface' in child.get('id'):
				root.remove(child)

	#position of graphic

	if graphic_number == 1: 
		group.set("transform", "matrix(3.1738315,0,0,3.1738315,-311.8713,-254.95541)")
	elif graphic_number == 2: 
		group.set("transform", "matrix(3.1738315,0,0,3.1738315,-1625.0069,-254.95541)")

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
				if elem[0].text == 'title':
					elem[0].text = title

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

graphic_number = 2

if graphic_number == 1 :
	graph_type = 'pie_bar_rank_incidence'
elif graphic_number == 2 :
	graph_type = 'pie_bar_rank_mortality'


files = [f for f in os.listdir('C:/Data/Globocan2020/factsheet/cancers') if os.path.isfile(os.path.join('C:/Data/Globocan2020/factsheet/cancers',f))]
# files = [f for f in os.listdir('C:/Data/Globocan2020/factsheet/cancers') if f == "1-Lip-oral-cavity-fact-sheet.pdf"]
for filebase in files:

	# print(filebase)

	print(filebase)


	cancer_name = re.sub(regex_cancer_name, r"\1", filebase)  
	cancer_file = re.sub(r"\W", r"", cancer_name)  
	filename =  "tw_factsheet_" + graph_type + "_"+cancer_file
	print(filename)

	title = cancer_name.replace('-', ' ') + ' cancer'
	title = re.sub(r"(.*cancer) cancer", r"\1", title)
	print(title)

	# name of the final file
	# filename = "031_gco365"


	# height of the graph can be edit
	# format is 16:9 (1200*)
	heigth = 1200 


	file_svg = './temp/temp_result.svg'
	file_png = 'C:/Projects/tweetO/img_sort/cancer/'+graph_type+'/'+ filename + '.png'

	print(file_svg)
	print('C:/Data/Globocan2020/factsheet/cancers/'+ filebase)

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

	counter = 0

	group = etree.Element('g')


	for child in root[1]:


		if child.tag == 'path':

			if ('rgb(11.759949%,25.878906%,45.098877%)' in child.get('style')):
				counter = counter+1
				if (counter == graphic_number):
					group.append(child)

		if (counter == graphic_number):
			# stop for last graph of the page
			if len(child)==1:
				if (child[0].tag == "path"):
					if ('rgb(4.309082%,50.19989%,71.759033%)' in child[0].get('style')):
						break

			group.append(child)
		if (counter != graphic_number):
			if (child.getparent() == root[1]):
				root[1].remove(child)



	for child in root:
		if (child.get('id') != None):
			if 'surface' in child.get('id'):
				root.remove(child)

	#position of graphic

	if graphic_number == 1: 
		group.set("transform", "matrix(3.1738315,0,0,3.1738315,-311.8713,-254.95541)")
	elif graphic_number == 2: 
		group.set("transform", "matrix(3.1738315,0,0,3.1738315,-1625.0069,-254.95541)")

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
				if elem[0].text == 'title':
					elem[0].text = title

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


