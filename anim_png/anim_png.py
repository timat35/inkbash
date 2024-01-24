from lxml import etree
import subprocess

dpi = 300


base = etree.parse('./base_svg.svg')
base.write('./temp.svg', pretty_print=False)

root = base.getroot()
map = root[(len(root) - 1)]
nb_png = len(map)

print(nb_png)

output = etree.parse('./temp.svg')
base_temp = output.getroot()
map_png = base_temp[(len(base_temp) - 1)]


for i in range(0, (nb_png)):

    map_png.remove(map_png[0])


for i in range(0, (nb_png)):

    map_png.append(map[0])
    output.write('./anim_png.svg', pretty_print=False)
    subprocess.call(['inkscape', '--export-dpi=' + str(dpi),  '--export-filename=./anim_png/anim_png'+ str(i) + '.png', './anim_png.svg'], shell=True)
    map_png.remove(map_png[0])


print("annnnnd done!")

#subprocess.Popen(r'explorer  /select,"C:\Projects\inkbash\anim_png\anim_png\gitkeep.txt"')










