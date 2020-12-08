import sys
import os
import re
import csv
import pandas as pd
from lxml import etree
import subprocess

country_info = pd.read_csv('C:/Data/Globocan2020/source/countries.csv')

regex = r"(.*)\.pdf"
regex_title = r"(\d+)-(.+)-fact-sheets.pdf"


#page of the graph
page = '1'

# graphic number 2: pie chart new cases both sexes
# graphic number 3: pie chart new cases males
# graphic number 4: pie chart new cases females
graphic_number = 2

# height of the graph can be edit
# format is 16:9 (1200*)
heigth = 675 

if graphic_number == 2 :
	graph_type = 'pie_top_incidence_both'
elif graphic_number == 3 :
	graph_type = 'pie_top_incidence_male'
elif graphic_number == 4 :
	graph_type = 'pie_top_incidence_female'

for filebase in os.listdir('C:/Data/Globocan2020/factsheet/populations'):
# parameter 
# name of the base file in the folder base
	
	print(filebase)
	country_name = re.sub(regex_title, r"\2", filebase)  
	country_file = re.sub(r"\W", r"", country_name)  
	filename =  "tw_factsheet_" + graph_type + "_"+country_file
	print(filename)

	country_code =  re.sub(regex_title, r"\1", filebase)

	title = country_info[country_info["COUNTRY"] == int(country_code)]['LABEL'].values[0]
	print(title)


	

	# height of the graph can be edit
	# format is 16:9 (1200*)
	heigth = 1200 


	file_svg = './temp/temp_result.svg'
	file_png = 'C:/Projects/tweetO/img_sort/population/'+graph_type+'/'+ filename + '.png'

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



	# drop last element of the page


	for child in root[1]:
		if child.tag == 'path':
			if ('rgb(11.799622%,25.898743%,45.098877%)' in child.get('style')) | ('rgb(11.759949%,25.878906%,45.098877%)' in child.get('style')):
				counter = counter+1
				continue;


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
			if (child.getparent() == root[1]):
				root[1].remove(child)



	for child in root:
		if (child.get('id') != None):
			if 'surface' in child.get('id'):
				root.remove(child)



	#position of graphic

	if graphic_number == 2: 
		group.set("transform", "matrix(3.7498829,0,0,3.7498829,-716.01594,-376.87173)")
	elif graphic_number == 3:
		group.set("transform", "matrix(3.7498829,0,0,3.7498829,-716.01594,-1291.4293)")
	elif graphic_number == 4:
		if (len(group) > 0):
			group.remove(group[len(group)-1])
		group.set("transform", "matrix(3.7498829,0,0,3.7498829,-716.01594,-2205.9869)")

	root.append(group)

	root.set("width", "1200")
	root.set("height", "1200")


	dis = etree.parse(open('./template/gco_template_square_subtitle.svg'))
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

# graphic number 2: pie chart new cases both sexes
# graphic number 3: pie chart new cases males
# graphic number 4: pie chart new cases females
graphic_number = 3

# height of the graph can be edit
# format is 16:9 (1200*)
heigth = 675 

if graphic_number == 2 :
	graph_type = 'pie_top_incidence_both'
elif graphic_number == 3 :
	graph_type = 'pie_top_incidence_male'
elif graphic_number == 4 :
	graph_type = 'pie_top_incidence_female'

for filebase in os.listdir('C:/Data/Globocan2020/factsheet/populations'):
# parameter 
# name of the base file in the folder base
	
	print(filebase)
	country_name = re.sub(regex_title, r"\2", filebase)  
	country_file = re.sub(r"\W", r"", country_name)  
	filename =  "tw_factsheet_" + graph_type + "_"+country_file
	print(filename)

	country_code =  re.sub(regex_title, r"\1", filebase)

	title = country_info[country_info["COUNTRY"] == int(country_code)]['LABEL'].values[0]
	print(title)


	

	# height of the graph can be edit
	# format is 16:9 (1200*)
	heigth = 1200 


	file_svg = './temp/temp_result.svg'
	file_png = 'C:/Projects/tweetO/img_sort/population/'+graph_type+'/'+ filename + '.png'

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



	# drop last element of the page


	for child in root[1]:
		if child.tag == 'path':
			if ('rgb(11.799622%,25.898743%,45.098877%)' in child.get('style')) | ('rgb(11.759949%,25.878906%,45.098877%)' in child.get('style')):
				counter = counter+1
				continue;


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
			if (child.getparent() == root[1]):
				root[1].remove(child)



	for child in root:
		if (child.get('id') != None):
			if 'surface' in child.get('id'):
				root.remove(child)



	#position of graphic

	if graphic_number == 2: 
		group.set("transform", "matrix(3.7498829,0,0,3.7498829,-716.01594,-376.87173)")
	elif graphic_number == 3:
		group.set("transform", "matrix(3.7498829,0,0,3.7498829,-716.01594,-1291.4293)")
	elif graphic_number == 4:
		if (len(group) > 0):
			group.remove(group[len(group)-1])
		group.set("transform", "matrix(3.7498829,0,0,3.7498829,-716.01594,-2205.9869)")

	root.append(group)

	root.set("width", "1200")
	root.set("height", "1200")


	dis = etree.parse(open('./template/gco_template_square_subtitle.svg'))
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

# graphic number 2: pie chart new cases both sexes
# graphic number 3: pie chart new cases males
# graphic number 4: pie chart new cases females
graphic_number = 4

# height of the graph can be edit
# format is 16:9 (1200*)
heigth = 675 

if graphic_number == 2 :
	graph_type = 'pie_top_incidence_both'
elif graphic_number == 3 :
	graph_type = 'pie_top_incidence_male'
elif graphic_number == 4 :
	graph_type = 'pie_top_incidence_female'

for filebase in os.listdir('C:/Data/Globocan2020/factsheet/populations'):
# parameter 
# name of the base file in the folder base
	
	print(filebase)
	country_name = re.sub(regex_title, r"\2", filebase)  
	country_file = re.sub(r"\W", r"", country_name)  
	filename =  "tw_factsheet_" + graph_type + "_"+country_file
	print(filename)

	country_code =  re.sub(regex_title, r"\1", filebase)

	title = country_info[country_info["COUNTRY"] == int(country_code)]['LABEL'].values[0]
	print(title)


	

	# height of the graph can be edit
	# format is 16:9 (1200*)
	heigth = 1200 


	file_svg = './temp/temp_result.svg'
	file_png = 'C:/Projects/tweetO/img_sort/population/'+graph_type+'/'+ filename + '.png'

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



	# drop last element of the page


	for child in root[1]:
		if child.tag == 'path':
			if ('rgb(11.799622%,25.898743%,45.098877%)' in child.get('style')) | ('rgb(11.759949%,25.878906%,45.098877%)' in child.get('style')):
				counter = counter+1
				continue;


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
			if (child.getparent() == root[1]):
				root[1].remove(child)



	for child in root:
		if (child.get('id') != None):
			if 'surface' in child.get('id'):
				root.remove(child)



	#position of graphic

	if graphic_number == 2: 
		group.set("transform", "matrix(3.7498829,0,0,3.7498829,-716.01594,-376.87173)")
	elif graphic_number == 3:
		group.set("transform", "matrix(3.7498829,0,0,3.7498829,-716.01594,-1291.4293)")
	elif graphic_number == 4:
		if (len(group) > 0):
			group.remove(group[len(group)-1])
		group.set("transform", "matrix(3.7498829,0,0,3.7498829,-716.01594,-2205.9869)")

	root.append(group)

	root.set("width", "1200")
	root.set("height", "1200")


	dis = etree.parse(open('./template/gco_template_square_subtitle.svg'))
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
			