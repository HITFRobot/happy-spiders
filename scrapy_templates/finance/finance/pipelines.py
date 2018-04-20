# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb.cursors
import MySQLdb
from scrapy.pipelines.files import FilesPipeline
from twisted.enterprise import adbapi
import os
import json
import scrapy

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class FinancePipeline(object):
    def process_item(self, item, spider):
        return item


class PDFDownloadPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['files_urls_field'], meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        path = '%s/%s_%s_%s.pdf' %(item['site'], item['name'], item['date'], item['title'])
        return path


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        if spider.name == 'stock_exchange':
            query = self.dbpool.runInteraction(self.do_insert, item)
            query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class MyJsonPipline(object):
    def __init__(self, current_dir):
        self.huace_file = open(os.path.join(current_dir, 'json/huace.json'), 'a', encoding='utf-8')
        self.xueqiu_file = open(os.path.join(current_dir, 'json/xueqiu.json'), 'w', encoding='utf-8')

    @classmethod
    def from_crawler(cls, crawler):
        """
            关于该方法的理解：
            crawler对象应该是scrapy中最核心的对象，它贯穿整个框架，无论任何spider与pipelines
            scrapy启动时，通过该方法返回pipeline的实例
        :param crawler:
        :return:
        """
        return cls(crawler.settings.get('CURRENT_DIR'))

    def process_item(self, item, spider):
        if spider.name == 'guba':
            item_json = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.huace_file.write(item_json)
            return item
        if spider.name == 'xueqiu':
            item_json = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.xueqiu_file.write(item_json)
            return item

    def close_spider(self, spider):
        self.huace_file.close()
        self.xueqiu_file.close()
