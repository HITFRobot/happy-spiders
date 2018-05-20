# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from openpyxl import load_workbook


data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result')


class QichachaPipeline(object):
    def __init__(self) -> None:
        self.file = os.path.join(data_dir, 'firm.xlsx')
        self.excel = load_workbook(self.file)

    def process_item(self, item, spider):
        # 获取指定的sheet
        sheet = self.excel.get_sheet_by_name('Sheet1')
        company = item['company']
        english = item['english']
        estiblishTime = item['estiblishTime']
        regNumber = item['regNumber']
        regLocation = item['regLocation']
        range = item['range']
        websiteList = item['websiteList']
        phone = item['phone']
        email = item['email']

        row = []
        row.append(company)
        row.append(english)
        row.append(estiblishTime)
        row.append(regNumber)
        row.append(regLocation)
        row.append(range)
        row.append(websiteList)
        row.append(phone)
        row.append(email)
        # 插入
        sheet.append(row)
        self.excel.save(self.file)
        return item

    def spider_closed(self, spider):
        self.excel.close()
