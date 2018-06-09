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


class RedstardesignPipeline(object):
    def __init__(self):
        self.file = os.path.join(data_dir, '2014.xlsx')
        self.excel = load_workbook(self.file)
        self.ws = self.excel.active

    def process_item(self, item, spider):
        year = item['year']
        awards_name = item['awards_name']
        num = item['num']
        # img_path = item['img_path'].split('/')[-1]
        img_path = item['design_name']+ item['img_path'].split('/')[-1]
        design_name = item['design_name']
        productor_name = item['product_name']
        design_unit = item['design_unit']
        awards = item['awards']
        description = item['description']

        all_data = [year, awards_name, num, design_name, productor_name, design_unit, awards, description, img_path]
        # self.ws.append(all_data)
        # self.excel.save(self.file)
        self.ws.append(all_data)
        self.excel.save(self.file)
        return item

    def close_spider(self, spider):
        self.excel.close()


class DownlodImagePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        host = 'http://www.redstaraward.org'
        img_path = host + item['img_path']
        img_name = item['design_name'] + item['img_path'].split('/')[-1]
        year = item['year']
        yield scrapy.Request(url=img_path, meta={'img_name': img_name, 'year': year})

    def file_path(self, request, response=None, info=None):
        img_name = re.sub('/', '_', request.meta['img_name'])
        year = request.meta['year']
        path = '%s/%s' % (year, img_name)
        return path
