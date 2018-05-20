# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import load_workbook
import os

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')


class TripadvisorPipeline(object):
    def __init__(self) -> None:
        self.file = os.path.join(data_dir, 'zh.xlsx')
        self.excel = load_workbook(self.file)

    def process_item(self, item, spider):
        sheet = self.excel.get_sheet_by_name("Sheet1")
        name = item['name']
        title = item['title']
        comment = item['comment']
        row = []
        row.append(name)
        row.append(title)
        row.append(comment)
        # 插入
        sheet.append(row)
        self.excel.save(self.file)
        return item

    def spider_closed(self, spider):
        self.excel.close()