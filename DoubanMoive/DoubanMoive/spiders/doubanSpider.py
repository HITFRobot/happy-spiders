# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import DoubanmoiveItem
from urllib import parse

__author__ = 'HIT Lianjie Sun'


class DoubanSpider(scrapy.Spider):
    """
        爬取豆瓣250电影，以json文件形式存储
    """
    name = 'doubanSpider'
    allowed_domains = ['douban.com']
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):
        for info in response.xpath('//div[@class="item"]'):
            item = DoubanmoiveItem()
            item['rank'] = info.xpath('div[@class="pic"]/em/text()').extract_first()
            print(item['rank'])
            item['title'] = info.xpath('div[@class="pic"]/a/img/@alt').extract_first()
            print(item['title'])
            item['link'] = info.xpath('div[@class="pic"]/a/@href').extract_first()
            print(item['link'])
            item['rate'] = info.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/'
                                      'span[@class="rating_num"]/text()').extract_first()
            print(item['rate'])
            item['comment_num'] = info.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]'
                                             '/span[4]/text()').extract_first()[:-3]
            print(item['comment_num'])
            item['quote'] = info.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/'
                                       'text()').extract_first()
            print(item['quote'])
            yield item

            # next page
            next_url = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract_first()
            if next_url is not None:
                yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)




