# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import os

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class JsonPipeline(object):

    collection_name = 'DoubanMoiveItem'

    def __init__(self):
        self.file = codecs.open(os.path.join(BASE_DIR, 'data/douban.json'), 'w', encoding='utf-8')

    @classmethod
    def from_crawler(cls, crawler):
        """
            关于该方法的理解：
            crawler对象应该是scrapy中最核心的对象，它贯穿整个框架，无论任何spider与pipelines
            scrapy启动时，通过该方法返回pipeline的实例
        :param crawler:
        :return:
        """
        return cls()

    def process_item(self, item, spider):
        item_json = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(item_json)
        return item

    def open_spider(self, spider):
        pass

    def spider_closed(self, spider):
        self.file.close()


class MongoPipeline(object):
    def __init__(self):
        pass
        # connect db

    def process_item(self, item, spider):
        pass
        # insert

    def spider_closed(self, spider):
        pass