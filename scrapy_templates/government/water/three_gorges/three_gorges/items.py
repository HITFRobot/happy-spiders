# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThreeGorgesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SanXiaItem(scrapy.Item):
    name = scrapy.Field()
    time = scrapy.Field()
    # 入库
    rk20 = scrapy.Field()
    rk14 = scrapy.Field()
    rk08 = scrapy.Field()
    rk02 = scrapy.Field()
    # 出库
    ck20 = scrapy.Field()
    ck14 = scrapy.Field()
    ck08 = scrapy.Field()
    ck02 = scrapy.Field()
    # 上游
    sy20 = scrapy.Field()
    sy14 = scrapy.Field()
    sy08 = scrapy.Field()
    sy02 = scrapy.Field()
    # 下游
    xy20 = scrapy.Field()
    xy14 = scrapy.Field()
    xy08 = scrapy.Field()
    xy02 = scrapy.Field()

