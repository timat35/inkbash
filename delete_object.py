import sys
import os
from lxml import etree
from subprocess import call

dir_update = 'C:/Projects/globocan2018_graph/map_by_site/cumrisk_abs'

bool_change = False

for file_sites in os.listdir(dir_update):
    bool_change = False
    if '.svg' in file_sites:
        path_file = os.path.join(dir_update, file_sites)
        print(path_file)
        path_pdf = path_file.replace(".svg", ".pdf")
        base = etree.parse(path_file)
        root = base.getroot()
        map = root[1]

        for child in map:
            if 'd' in child.attrib:
                if 'M 1329.082031 1337.382813' in child.get("d"):
                    if 'rgb(50.196078%,50.196078%' in child.get("style"):
                        map.remove(child)
                        bool_change = True



    if bool_change:
        base.write(path_file, pretty_print=False)
        call(["inkscape", "--without-gui", "--export-pdf="+path_pdf, path_file])

