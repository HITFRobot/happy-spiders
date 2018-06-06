# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RedstardesignItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    year = scrapy.Field()
    awards_name = scrapy.Field()
    num = scrapy.Field()

    img_path = scrapy.Field()
    design_name = scrapy.Field()
    product_name = scrapy.Field()
    design_unit = scrapy.Field()
    awards = scrapy.Field()
    description = scrapy.Field()

