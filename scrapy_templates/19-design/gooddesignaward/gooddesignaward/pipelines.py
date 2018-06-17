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
year_dict = {'1957': 1, '1987': 1, '1965': 1, '2002': 1, '1977': 1, '1994': 1, '1998': 1, '1959': 1, '1967': 1,
             '1990': 1, '1986': 1, '1962': 1, '1978': 1, '1971': 1, '1984': 1, '2010': 1, '2000': 1, '2004': 1,
             '1975': 1, '1995': 1, '2014': 1, '1976': 1, '1973': 1, '1968': 1, '2005': 1, '1964': 1, '1966': 1,
             '1974': 1, '1989': 1, '1960': 1, '1970': 1, '1996': 1, '1969': 1, '1980': 1, '1991': 1, '2003': 1,
             '1997': 1, '1988': 1, '2001': 1, '1999': 1, '2017': 1, '1992': 1, '2008': 1, '1979': 1, '1982': 1,
             '2012': 1, '2013': 1, '1993': 1, '1958': 1, '2011': 1, '1972': 1, '2015': 1, '1963': 1, '1985': 1,
             '1981': 1, '2006': 1, '2009': 1, '2007': 1, '1983': 1, '2016': 1, '1961': 1}



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

        if name == ' ':
            for img_url in images:
                if 'http' in img_url:
                    image_name = year + '_' + str(year_dict[year])
                    year_dict[year] += 1
                    i += 1
                    yield scrapy.Request(url=img_url,
                                         meta={'image_name': image_name, 'year': year})
        else:
            for img_url in images:
                if 'http' in img_url:
                    image_name = name + '_' + str(i)
                    i += 1
                    yield scrapy.Request(url=img_url,
                                         meta={'image_name': image_name, 'year': year})

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
        self.numbers = set()

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

        if number in self.numbers:
            return item
        self.numbers.add(number)
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

