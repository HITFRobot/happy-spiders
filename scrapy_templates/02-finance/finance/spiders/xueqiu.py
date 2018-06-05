# -*- coding: utf-8 -*-

import scrapy
import json
import time
from scrapy.http import Request
from ..items import IceItem
from scrapy.loader import ItemLoader
from urllib import parse


class XueqiuSpider(scrapy.Spider):
    """
    雪球投资网头条模块页面解析类
    https://xueqiu.com/
    """
    name = 'xueqiu'
    # allowed domains
    # allowed_domains = ['http://xueqiu.com/']
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'aliyungf_tc=AQAAAEJmyl2YUgoABlLFI/x3bKzp7B0d; xq_a_token=19f5e0044f535b6b1446bb8ae1da980a48bbe850; xq_a_token.sig=aaTVFAX9sVcWtOiu-5L8dL-p40k; xq_r_token=6d30415b5f855c12fd74c6e2fb7662ea40272056; xq_r_token.sig=rEvIjgpbifr6Q_Cxwx7bjvarJG0; u=961520767527050; device_id=be04e574ee404d4a38c72d4b97155892; __utma=1.121698064.1520767527.1520767527.1520767527.1; __utmc=1; __utmz=1.1520767527.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=1.1.10.1520767527; Hm_lvt_1db88642e346389874251b5a1eded6e3=1520767528; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1520767528',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }
    start_urls = [
        'https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=-1&count=10&category=-1']

    def parse(self, response):

        """
        此网站全为异步加载，使用json数据格式
        1. get every announcement's target url for further analysis
        2. get next page url
        :param response:
        :return:
        """
        js = json.loads(response.body.decode('utf-8'))
        next_max_id = js['next_max_id']
        for item in js['list']:
            data = json.loads(item['data'])
            title = data['title']
            create_time = data['created_at']
            yield Request(url=parse.urljoin(response.url, data['target']),
                          meta={'title': title, 'create_time': create_time}, callback=self.parse_detail,
                          dont_filter=True)

        if next_max_id != -1:
            next_url = 'https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=' + str(
                next_max_id) + '&count=10&category=-1'
            yield Request(url=next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):

        item = ItemLoader(item=IceItem(), response=response)

        title = response.meta.get('title')
        create_time = response.meta.get('create_time')
        item.add_value('title', title)
        item.add_value('create_time', create_time)
        item.add_css('author_name', '.avatar__name a::attr(data-screenname)')
        content = "".join(
            list(response.css('.article__bd__detail p::text,.article__bd__detail img::attr(src)').extract()))
        item.add_value('content', content)
        return item.load_item()
