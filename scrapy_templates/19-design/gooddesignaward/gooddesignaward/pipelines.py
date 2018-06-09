# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.pipelines.files import FilesPipeline
from openpyxl import load_workbook
import scrapy
import re
import shutil


data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../images')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
if not os.path.exists(images_dir):
    os.makedirs(images_dir)


class DownlodImagePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        year = item['year']
        name = item['name']
        images = item['images']
        i = 1
        for img_url in images:
            if 'http' in img_url:
                image_name = name + '_' + str(i)
                i += 1
                yield scrapy.Request(url=img_url,
                                     meta={'image_name': image_name, 'year': year})

    def file_path(self, request, response=None, info=None):
        image_name = request.meta['image_name']
        image_name = re.sub(r'/', ' ', image_name)
        year = request.meta['year']
        path = '%s/%s.jpg' % (str(year), image_name)
        return path


class ExcelPipeline(object):

    def __init__(self) -> None:
        self.file = None
        self.excel = None
        self.ws = None

    def process_item(self, item, spider):
        year = item['year']
        if self.file is None or year not in self.file:
            if self.file is not None:
                self.excel.close()
            self.file = os.path.join(data_dir, str(year)+'.xlsx')
            if not os.path.isfile(self.file):
                shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../demo.xlsx'),
                            os.path.join(data_dir, str(year) + '.xlsx'))
            self.excel = load_workbook(self.file)
            self.ws = self.excel.active

        award = item['award']
        name = item['name']
        business = item['business']
        category = item['category']
        company = item['company']
        number = item['number']
        outline = item['outline']
        producer = item['producer']
        director = item['director']
        designer = item['designer']
        information = item['information']
        date = item['date']
        images = item['images']

        if len(images) > 3:
            images = images[0:4]
        for i in range(7 - len(images)):
            images.append('')

        entry = [year, award, name, business, category, company, number, outline,
                    producer, director, designer, information, date] + images
        self.ws.append(entry)
        self.excel.save(self.file)
        return item

    def close_spider(self, spider):
        self.excel.close()


if __name__ == '__main__':
    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../demo.xlsx'),
                os.path.join(data_dir, str(2016) + '.xlsx'))