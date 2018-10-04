import sys
import re
import os
from lxml import etree
import subprocess
import math



area = [14,15,16,17]
y = [0]*len(area)
x = [0]*len(area)

for i in range(0,len(area)):
    y[i] = i


print(y)

t = [0]*len(area)+1
print(t)
