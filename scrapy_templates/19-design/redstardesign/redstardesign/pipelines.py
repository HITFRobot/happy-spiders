# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import load_workbook
from scrapy.pipelines.files import FilesPipeline
import os
import scrapy
import re
import sys

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

print(data_dir)


class RedstardesignPipeline(object):
    def __init__(self):
        self.file = os.path.join(data_dir, '2017.xlsx')
        self.excel = load_workbook(self.file)
        self.ws = self.excel.active

    def process_item(self, item, spider):

        year = item['year']
        awards_name = item['awards_name']
        num = item['num']
        img_path = item['img_path']
        design_name = item['design_name']
        product_name = item['product_name']
        design_unit = item['design_unit']
        awards = item['awards']
        description = item['description']

        all_data = [year, awards_name, num, img_path, design_name, product_name, design_unit, awards, description]
        self.ws.append(all_data)
        self.excel.save(self.file)
        return item
