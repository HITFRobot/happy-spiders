# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import DoubanMoiveItem
from urllib import parse


__author__ = 'HIT Lianjie Sun'


class DoubanSpider(scrapy.Spider):
    """
        爬取豆瓣top250电影，以json文件形式存储
        关于Spider中from_crawler，_set_crawler的理解
        框架一旦启动，就会创建crawler对象
        任何一个spider都要绑定crawler对象，这个crawler对象贯穿整个scrapy框架
    """
    name = 'doubanSpider'
    allowed_domains = ['douban.com']
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):
        for info in response.xpath('//div[@class="item"]'):
            item = DoubanMoiveItem()
            item['rank'] = info.xpath('div[@class="pic"]/em/text()').extract_first()
            item['title'] = info.xpath('div[@class="pic"]/a/img/@alt').extract_first()
            item['link'] = info.xpath('div[@class="pic"]/a/@href').extract_first()
            item['rate'] = info.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/'
                                      'span[@class="rating_num"]/text()').extract_first()
            item['comment_num'] = info.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]'
                                             '/span[4]/text()').extract_first()[:-3]
            item['quote'] = info.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/'
                                       'text()').extract_first()
            yield item

            # next page
            next_url = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract_first()
            if next_url is not None:
                yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)




