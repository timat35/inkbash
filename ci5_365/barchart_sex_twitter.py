import sys
import os
from lxml import etree



dir_folder = os.path.dirname(__file__)

base = etree.parse(open(sys.argv[1]))
root = base.getroot()



# #position of graphic

# if graphic_number == 3: 
# 	group.set("transform", "matrix(2.9939928,0,0,2.9939928,-269.43608,-2416.1767)")
# elif graphic_number == 4: 
# 	group.set("transform", "matrix(2.9939928,0,0,2.9939928,-1508.1655,-2416.1767)")

# root.append(group)

root.set("width", "1200")
root.set("height", "1200")

root[1].set("transform", "matrix(0.9,0,0,0.9,43.2,72)")


dis = etree.parse(open('./template/gco_template_square.svg'))
root_dis = dis.getroot()

# remove name space
for elem in root_dis.getiterator():
	elem.tag = etree.QName(elem).localname
etree.cleanup_namespaces(root_dis)


#manage banner
for child in root_dis[3]:
	for elem in child:
		if (elem.tag == "text"):
			for child_elem in elem:
				child_elem.text = sys.argv[2]
			

			
root_dis[3].set("transform", "matrix(2.7212598,0,0,2.7212598,1358.3042,708.80085)")

root.insert(root.index(root[0])+1,root_dis[3])


base.write(sys.argv[1], pretty_print=False)
# subprocess.Popen(['inkscape', '-f=' + file_svg])

# export to png
# subprocess.call(['inkscape', 
# 			'--without-gui', 
# 			'--export-height=' + str(heigth), 
# 			'--export-png=' + file_png, 
# 			file_svg], shell=True)


# print(filename + ' is processed')
