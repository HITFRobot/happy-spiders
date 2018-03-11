# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
from .settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT


class FinanceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SEAItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def remove_space(value):
    return value.strip()


def date_convert(value):
    try:
        date = datetime.datetime.strptime(value.split('：')[1].strip(), '%Y-%m-%d').date()
    except:
        date = datetime.datetime().date()
    return date


# Unix时间戳(Unix timestamp)转换
def date_convert_two(value):
    format_string = "%Y-%m-%d %H:%M:%S"
    time_array = time.localtime(value / 1000)
    str_date = time.strftime(format_string, time_array)
    return str_date


class StockExchangeAnnouncement(scrapy.Item):
    url_object_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field(
        input_processor=MapCompose(remove_space),
    )
    publish_time = scrapy.Field(
        input_processor=MapCompose(remove_space, date_convert),
    )
    # number = scrapy.Field()
    content = scrapy.Field(
        input_processor=MapCompose(remove_space),
    )
    # attachment_url = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into stock_exchange(url_object_id, url, title, publish_time, content, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            self['url_object_id'],
            self['url'],
            self['title'],
            self['publish_time'],
            self['content'],
            self['crawl_time'].strftime(SQL_DATETIME_FORMAT),
        )
        return insert_sql, params


class HuaceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    comment = scrapy.Field(output_processor=Join(separator='###'))


class IceItem(scrapy.Item):
    title = scrapy.Field()
    create_time = scrapy.Field(input_processor=MapCompose(date_convert_two))
    content = scrapy.Field()
    author_name = scrapy.Field()
