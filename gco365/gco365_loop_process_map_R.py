import sys
import os
import re
import csv
import pandas as pd
from lxml import etree
import subprocess


regex = r"map_(.+?)_(.+?)_(.+?)_(.+)"
cancer_name = pd.read_csv('./template/map_R_cancer_name.csv')

regex_cancer = r".*_(.*)"

regex_svg = r"(.*)\.svg"


folder_base = 'C:/Projects/globocan2020_graph/map/prevalence/svg'
folder_tweet = 'world_prevalence'





for file in os.listdir(folder_base):
# parameter 
# name of the base file in the folder base

	# if not re.search(r"absolute",file):
	# 	continue

	matches = re.search(regex_svg,file)
	if matches:
		filebase = re.sub(regex_svg, r"\1", file)

		filename = "tw_"+filebase

		# height of the graph can be edit
		# format is 16:9 (1200*)
		heigth = 675 

		title_sex = re.sub(regex, r"\1", filebase)
		if title_sex == 'both':
			title_sex = 'both sexes'
		else:
			title_sex = title_sex+'s'

		# title_type = re.sub(regex, r"\2", filebase)
		title_type = "5-year prevalence"



		print(filebase)

		title_cancer = cancer_name[cancer_name["file_cancer"] == re.sub(regex_cancer, r"\1", filebase)]['cancer_name'].values[0].capitalize()

		if not re.search(r"cancer", title_cancer):
			title_cancer = title_cancer + ' cancer'
			
		title = title_cancer + ', ' + title_type + ', ' + title_sex

		print(title +'\n' )
		file_svg = './temp/temp_result.svg'
		file_png = 'C:/Projects/tweetO/img_sort/map/'+folder_tweet+'/'+ filename + '.png'


		base = etree.parse(open(folder_base+'/'+ filebase +'.svg'))
		root = base.getroot()

		# remove name space
		for elem in root.getiterator():
			elem.tag = etree.QName(elem).localname
		etree.cleanup_namespaces(root)

		# drop other style
		# root[0].remove( root[0][1])  # drop other .css


		root[2].remove(root[2][2])
		root[2].remove(root[2][1])
		root[2].remove(root[2][0])

		






		# group element 

		group = etree.Element('g')
		for child in root:
			if child.tag != 'defs':
				group.append(child)

		root.append(group)
		root[1].set("transform", "matrix(0.96858294,0,0,0.96858294,13.080029,7.3815728)")



		root.set("width", "1200")
		root.set("height", "675")

		dis = etree.parse(open('./template/gco_template_map_R.svg'))
		root_dis = dis.getroot()

		# remove name space
		for elem in root_dis.getiterator():
			elem.tag = etree.QName(elem).localname
		etree.cleanup_namespaces(root_dis)

		# edit text 
		for child in root_dis[3][1]:
			if child.tag == 'text':
				if child[0].text == 'title':
					child[0].text = title

		root.insert(root.index(root[0])+1,root_dis[3])
		base.write(file_svg, pretty_print=False)


		# export to png
		subprocess.call(['inkscape', 
					'--without-gui', 
					'--export-height=' + str(heigth), 
					'--export-png=' + file_png, 
					file_svg], shell=True)


		print(filename + ' is processed')

	# 