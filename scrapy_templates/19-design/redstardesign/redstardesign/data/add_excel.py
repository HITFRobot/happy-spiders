import os
import shutil

for i in range(2014, 2017):
    shutil.copy('demo.xlsx',str(i)+'.xlsx')