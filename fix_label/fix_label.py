from lxml import etree
import subprocess
import re

file_eps = './temp/temp.eps'
file_svg = file_eps.replace('.eps', '.svg')
file_final = './graph.svg'


subprocess.call(['inkscape', '--without-gui', '--export-plain-svg='+file_svg, file_eps], shell=True)
print("file convert to svg")

base = etree.parse(open(file_svg, encoding='utf-8-sig'))
root = base.getroot()

for elem in root.iter():
    if ('tspan' in elem.tag):
        temp_y = re.sub(r"(\d.*?)\s.+$", r"\1", elem.get('y'))
        temp_x = re.sub(r"(\d.*?)\s.+$", r"\1", elem.get('x'))
        elem.set('x', temp_x)
        elem.set('y', temp_y)


base.write('./graph.svg', pretty_print=False)

subprocess.Popen(['inkscape', '-f=' + file_final])
print("look on inkscape")
