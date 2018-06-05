# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
import MySQLdb
import MySQLdb.cursors



class ArticleSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'front_image_url' in item:
            for status, value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self) -> None:
        self.file = codecs.open('jobbole.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    def __init__(self) -> None:
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item=item)
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class MysqlPipeline(object):
    def __init__(self) -> None:
        self.conn = MySQLdb.connect('', '', '', '',  charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into articles(title, create_date, url, url_object_id, front_image_url, front_image_path, praise_nums, fav_nums, comment_nums, content, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"], item["front_image_path"], item["praise_nums"], item["fav_nums"], item["comment_nums"], item["content"], item["tags"]))
        # insert_sql = """
        #     insert into articles(title, create_date, url, url_object_id, front_image_url, front_image_path)
        #     VALUES (%s, %s, %s, %s, %s, %s)
        # """
        # self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"], item["front_image_path"]))
        self.conn.commit()
        return item
