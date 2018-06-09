import os
import shutil

for i in range(1981, 2018):
    shutil.copy('demo.xlsx', './data/'+str(i)+'.xlsx')