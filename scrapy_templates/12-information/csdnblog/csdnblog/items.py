# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.loader.processors import MapCompose


class CsdnblogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 日期转换
def date_convert(value):
    try:
        push_date = datetime.datetime.strptime(value, '%Y年%m月%d日 %H:%M:%S')
    except:
        push_date = datetime.datetime.now()
    return push_date


# Item类
class CsdnArticleItenm(scrapy.Item):
    url = scrapy.Field()
    blog_title = scrapy.Field()
    push_date = scrapy.Field(output_process=MapCompose(date_convert))
    original = scrapy.Field()
    view_times = scrapy.Field()
    comment_num = scrapy.Field()
    blog_content = scrapy.Field()


# 测试函数
if __name__ == '__main__':
    a = '2018年01月17日 06:50:49'
    print(date_convert(a))
