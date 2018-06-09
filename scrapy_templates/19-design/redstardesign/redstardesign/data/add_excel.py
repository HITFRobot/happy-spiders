import os
import shutil

for i in range(2014, 2018):
    shutil.copy('demo.xlsx', str(i) + '.xlsx')
