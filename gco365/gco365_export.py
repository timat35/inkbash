
import os
from lxml import etree
import subprocess


heigth = 2560 

dir_base = './final_svg/'
dir_png = './final_png/'

for file_base in os.listdir(dir_base):

    if file_base[-3:] == 'svg':
    	print(file_base)
    	# base = etree.parse(open(dir_base+ file_base))
    	# root = base.getroot()
    	# for elem in root.getiterator():
    	# 	elem.tag = etree.QName(elem).localname
    	# etree.cleanup_namespaces(root)
    	# for child in root:
    	# 	if (child.tag[-1] == 'g'):
    	# 		for child2 in child:
    	# 			if child2.tag == 'rect':
    	# 				child.remove(child2)
    	# 				break;
    	# base.write('./temp/temp.svg', pretty_print=False)

    	file_png = file_base.replace(".svg", ".png")
    	subprocess.call(['inkscape', 
			'--without-gui', 
			'--export-height=' + str(heigth), 
			'--export-png=' + dir_png + file_png, 
			dir_base + file_base], shell=True)


print("Done")

