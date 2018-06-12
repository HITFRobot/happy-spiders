# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GooddesignawardItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    year = scrapy.Field()  # 1. 获奖年份
    award = scrapy.Field()  # 2. 奖项名称
    name = scrapy.Field()  # 3. 作品名称
    business = scrapy.Field()  # 4. 主要实施业务
    category = scrapy.Field()  # 5. 产品分类
    company = scrapy.Field()  # 6. 公司 国家
    number = scrapy.Field()  # 7. 奖项编号
    outline = scrapy.Field()  # 8. 作品描述
    producer = scrapy.Field()  # 9. 制作商
    director = scrapy.Field()  # 10. 负责人
    designer = scrapy.Field()  # 11. 设计师
    information = scrapy.Field()  # 12. 更多信息
    date = scrapy.Field()  # 13. 投放市场时间
    images = scrapy.Field()  # 14. 作品图片