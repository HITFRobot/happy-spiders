# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DesignItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    type = scrapy.Field()
    discipline = scrapy.Field()
    year = scrapy.Field()
    development = scrapy.Field()
    regions = scrapy.Field()
    groups = scrapy.Field()
    criteria = scrapy.Field()
    clients = scrapy.Field()
    universities = scrapy.Field()
    designs = scrapy.Field()
    img1 = scrapy.Field()
    img2 = scrapy.Field()
    img3 = scrapy.Field()
    description = scrapy.Field()
