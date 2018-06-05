# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import datetime
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import re


class ArticleSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + 'jobbole'


def date_convert(value):
    try:
        date = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except:
        date = datetime.datetime.now().date()
    return date


def get_nums(value):
    match_re = re.match('.*?(\d+).*', value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field(
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    front_image_url = scrapy.Field(
        output_processor=MapCompose(lambda x: x)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        output_processor=Join('|')
    )