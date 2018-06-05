# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QichachaItem(scrapy.Item):
    # define the fields for your item here like:
    company = scrapy.Field()
    websiteList = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    regNumber = scrapy.Field()
    estiblishTime = scrapy.Field()
    regLocation = scrapy.Field()
    range = scrapy.Field()
    english = scrapy.Field()
