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


data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')


class DownlodImagePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        img_urls = [item['img1'], item['img2'], item['img3']]
        name = item['name']
        i = 1
        for img_url in img_urls:
            if img_url is not None:
                image_name = name + '_' + str(i)
                i += 1
                yield scrapy.Request(url=img_url, meta={'image_name': image_name})

    def file_path(self, request, response=None, info=None):
        image_name = request.meta['image_name']
        image_name = re.sub(r'/', ' ', image_name)
        path = '%s/%s.jpg' % ('1954', image_name)
        return path


class DesignPipeline(object):
    def __init__(self):
        self.file = os.path.join(data_dir, '1954.xlsx')
        self.excel = load_workbook(self.file)
        self.ws = self.excel.active

    def process_item(self, item, spider):
        name = item['name']
        type = item['type']
        discipline = item['discipline']
        year = item['year']
        development = item['development']
        regions = item['regions']
        groups = item['groups']
        criteria = item['criteria']
        clients = item['clients']
        universities = item['universities']
        designs = item['designs']
        img1 = item['img1']
        img2 = item['img2']
        img3 = item['img3']
        description = item['description']

        clients_length = len(clients)
        if clients_length > 5:
            sys.exit()
        all_clients = []
        for client in clients:
            all_clients.append(client['manufacturer'])
            all_clients.append(client['location'])
        for i in range(5-clients_length):
            all_clients.append('')
            all_clients.append('')

        universities_length = len(universities)
        all_universities = []
        for universitie in universities:
            all_universities.append('')
            all_universities.append('')
        for i in range(3 - universities_length):
            all_universities.append('')
            all_universities.append('')

        designs_length = len(designs)
        if designs_length > 5:
            sys.exit()
        all_designs = []
        for design in designs:
            all_designs.append(design['designer'])
            all_designs.append(design['design_company'])
            all_designs.append(design['location'])
        for i in range(5 - designs_length):
            all_designs.append('')
            all_designs.append('')
            all_designs.append('')

        client_uni_design = all_clients + all_universities + all_designs

        all_data = [name, type, discipline, year, development, regions, groups, criteria] + client_uni_design
        all_data.extend([img1, img2, img3, description])
        self.ws.append(all_data)
        self.excel.save(self.file)
        return item

    def close_spider(self, spider):
        self.excel.close()
