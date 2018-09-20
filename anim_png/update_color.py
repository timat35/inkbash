import sys
import os
from lxml import etree
from subprocess import call

dir_update = 'C:/Projects/globocan2018_graph/map by site/asr_abs'

color_mortality =["rgb(64.705882%,5.882353%,8.235294%)","rgb(87.058824%,17.647059%,14.901961%)","rgb(98.431373%,41.568627%,29.019608%)", "rgb(98.823529%,68.235294%,56.862745%)","rgb(99.607843%,89.803922%,85.098039%)"]
color_incidence= ["rgb(3.137255%,31.764706%,61.176471%)","rgb(25.490196%,47.45098%,70.588235%)", "rgb(48.235294%,63.529412%,80.392157%)","rgb(70.980392%,79.215686%,90.196078%)", "rgb(93.72549%,95.294118%,100%)"]

for file_sites in os.listdir(dir_update):
    if 'incidence' in file_sites:
        if '.svg' in file_sites:
            path_file = os.path.join(dir_update, file_sites)
            print(path_file)
            path_pdf = path_file.replace(".svg", ".pdf")
            base = etree.parse(path_file)
            root = base.getroot()
            map = root[1]
            for child in map:
                temp = child.get("style")
                for i in range(0,5) :
                    temp = temp.replace(color_mortality[i], color_incidence[i])
                child.set("style", temp)

            base.write(path_file, pretty_print=False)


            call(["inkscape", "--without-gui", "--export-pdf="+path_pdf, path_file])

