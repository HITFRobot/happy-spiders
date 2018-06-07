import os
import shutil

for i in range(2015, 2016):
    shutil.copy('demo.xlsx', str(i) + '.xlsx')
