# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import os
import pymysql
import json
from datetime import date, datetime

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class CsdnblogPipeline(object):
    def process_item(self, item, spider):
        return item


# 主要是python 中 list转换成json时对时间报错：datetime.datetime(2014, 5, 23, 9, 33, 3) is not JSON serializable。解决方案
# 就是重写构造json类，遇到日期特殊处理，其余的用内置的就行。
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class JsonExporterPipeline(object):
    # 初始化时指定要操作的文件

    def __init__(self):
        self.file = codecs.open(os.path.join(BASE_DIR, 'csdnblog/data/blog.json'), 'w', encoding='utf-8')

    # 存储数据，将 Item 实例作为 json 数据写入到文件中
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False, cls=MyEncoder) + '\n'
        self.file.write(lines)
        return item

    # 处理结束后关闭 文件 IO 流
    def close_spider(self, spider):
        self.file.close()


class MysqlPipeline(object):
    # 初始化数据库配置信息
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1234',
            db='csdn_blog',
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    # 插入操作
    def process_item(self, item, spider):
        print(item['push_date'])
        insert_sql = "insert into blog_detail(url, title, push_date, original, viewtime, blog_content, comment_num) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cur.execute(insert_sql, (
            item['url'], item['blog_title'], item['push_date'], item['original'], item['view_times'],
            item['blog_content'], item['comment_num']))
        self.conn.commit()
        return item
