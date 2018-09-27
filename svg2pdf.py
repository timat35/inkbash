
import os
import subprocess

dir_base = './svg2pdf'

for file_base in os.listdir(dir_base):
    if file_base[-3:] == 'svg':

        file_pdf =  file_base.replace(".svg", ".pdf")
        path_svg = os.path.join(dir_base, file_base)
        path_pdf = os.path.join(dir_base, file_pdf)

        subprocess.call(['inkscape','--without-gui', '--export-pdf='+path_pdf, path_svg], shell=True)
        print(file_base + " convert")




