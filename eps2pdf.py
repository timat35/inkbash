
import os
import subprocess

dir_base = 'C:/Projects/collignon/_figs'

for file_base in os.listdir(dir_base):
    if file_base[-3:] == 'eps':

        file_svg = file_base.replace(".eps", ".svg")
        file_pdf = file_base.replace(".eps", ".pdf")
        path_eps = os.path.join(dir_base, file_base)
        path_svg = os.path.join(dir_base, file_svg)
        path_pdf = os.path.join(dir_base, file_pdf)

        subprocess.call(['inkscape', '--without-gui', '--export-plain-svg='+path_svg, path_eps], shell=True)
        print(file_base + " svg convert")
        subprocess.call(['inkscape', '--without-gui', '--export-pdf='+path_pdf, path_svg], shell=True)
        print(file_base + " pdf convert")
