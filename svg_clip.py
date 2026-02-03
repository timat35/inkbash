from lxml import etree
import subprocess
import re
import sys

# test = "_figs/draft/temp.svg"
# base = etree.parse(open('./'+ test, encoding='utf-8-sig'))

base = etree.parse(open('./'+ sys.argv[1], encoding='utf-8-sig'))
root = base.getroot()

for elem in root:
	if ('rect' in elem.tag):
		root.remove(elem)
	if ('clip-path' in elem.attrib):
		elem.attrib.pop("clip-path")

		for child in elem:
			if ('}g' in child.tag):
				root.append(child)
				root.remove(elem)



print(sys.argv[1])
	  			

base.write('./'+ sys.argv[1], pretty_print=False)


