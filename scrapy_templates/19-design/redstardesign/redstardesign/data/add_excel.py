import os
import shutil

for i in range(2006, 2010):
    shutil.copy('demo.xlsx', str(i) + '.xlsx')
