
import os
import subprocess
import shutil
import fitz

bool_update_PDF = False
bool_group_pdf = True
bool_slide = False


dir_base = 'C:/Users/laversannem/Desktop/perso/photo/album_felix'
# dir_base = './svg2pdf'
dir_pdf2ppt = 'C:/tools/pdf2ppt/pdf'



if bool_group_pdf:
	result = fitz.open() 

if bool_slide:
	for file_old in os.listdir(dir_pdf2ppt):
		if file_old[-3:] == 'pdf':
			os.unlink(os.path.join(dir_pdf2ppt,file_old))

for file_base in os.listdir(dir_base):
    if file_base[-3:] == 'svg':

        file_pdf = file_base.replace(".svg", ".pdf")
        path_svg = os.path.join(dir_base, file_base)
        path_pdf = os.path.join(dir_base, file_pdf)

        if bool_update_PDF:
        	subprocess.call(['inkscape', '--export-filename='+path_pdf, path_svg], shell=True)
        print(file_base + " convert")

        if bool_group_pdf:
        	with fitz.open(path_pdf) as mfile:
        		result.insert_pdf(mfile)



        if bool_slide: 
        	path_dst = os.path.join(dir_pdf2ppt,file_pdf)
        	shutil.copy(path_pdf, path_dst)

if bool_slide:
	os.chdir('C:/tools/pdf2ppt/')
	subprocess.check_call(['node', 'C:/tools/pdf2ppt/pdf2ppt.js'])
	os.startfile('pdf2pptx.pptx', 'open')

if bool_group_pdf:
	result.save(os.path.join(dir_base, "album_felix.pdf"))


