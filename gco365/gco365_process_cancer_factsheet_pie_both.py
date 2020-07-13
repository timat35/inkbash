import sys
import os
import re
from lxml import etree
import subprocess

regex = r"(.*)\.pdf"
regex_cancer_name = r".*?-(.*)-fact.*\.pdf"

files = [f for f in os.listdir('./factsheet') if os.path.isfile(os.path.join('./factsheet',f))]
# files = [f for f in os.listdir('./factsheet') if f == "1-Lip-oral-cavity-fact-sheet.pdf"]
for filebase in files:

	# parameter 
	# name of the base file in the folder base
	filename =  "pie-both-" +re.sub(regex, r"\1", filebase)  
	cancer_name = re.sub(regex_cancer_name, r"\1", filebase)  
	cancer_label =cancer_name.replace('-', ' ')
	title = cancer_label + ' cancer'

	title = re.sub(r"(.*cancer) cancer", r"\1", title)
	print(title)


	#page of the graph
	page = '1'


	# height of the graph can be edit
	# format is 16:9 (1200*)
	heigth = 675 


	file_svg = './factsheet/pie-both/' + filename+ '.svg'
	file_png = './factsheet/pie-both/'+ filename + '.png'

	print('convert pdf to svg...')
	# PDF factsheet to svg
	subprocess.call([os.path.dirname(__file__) + '/pdf2svg/pdf2svg.exe', 
				'./factsheet/'+ filebase , 
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
	bool_add = False
	group = etree.Element('g')


	for child in root[1]:


		if child.tag == 'path':
			if ('rgb(11.799622%,25.898743%,45.098877%)' in child.get('style')):
				counter = counter+1
				if (counter == 1):
					bool_add = True
					group.append(child)
				elif (counter == 2):
					bool_add = True
					group.append(child)
				else:
					bool_add = False


		if bool_add:
			group.append(child)
		else:
			root[1].remove(child)





	#position of graphic


	group.set("transform", "matrix(2.5645595,0,0,2.5645595,-465.45645,-13.056053)")

	root.append(group)

	root.set("width", "1200")
	root.set("height", "675")


	dis = etree.parse(open('./template/gco_template_landscape_pie.svg'))
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

	root_dis[3].set("transform", "matrix(4.7146107,0,0,4.7146107,1893.7854,704.13864)")

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


