import sys
import os
import shutil




folder_base = 'C:/Users/laversannem/Documents/R/win-library'

for folder in os.listdir(folder_base):
    if 'CanReg' in folder:
        print(os.path.join(folder_base,folder))
        shutil.rmtree(os.path.join(folder_base,folder))
