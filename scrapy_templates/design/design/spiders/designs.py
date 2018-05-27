# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from .util import parse_json_str
import sys


class DesignsSpider(scrapy.Spider):
    name = 'designs'
    allowed_domains = ['ifworlddesignguide.com']
    start_urls = ['https://ifworlddesignguide.com/design-excellence?time_min=2017&time_max=2017']
    url = 'https://ifworlddesignguide.com/design-excellence?time_min=2017&time_max=2017'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=k2slfu98bvak7ina9pfpkkqboo; _ga=GA1.2.1153730110.1527427959; _gid=GA1.2.1362895861.1527427959',
        'Host': 'ifworlddesignguide.com',
        'Referer': 'https://ifworlddesignguide.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    def start_requests(self):
        yield Request(url=self.url, callback=self.parse)

    def parse(self, response):
        try:
            if response.status == 200:
                json_obj = parse_json_str(response.text)
                # "根据json_obj进入detail"
            else:
                raise Exception('error')
        except Exception as error:
            print('error')
            sys.exit()

        next_url = 'https://my.ifdesign.de/WdgService/articles/design_excellence?' \
                   'time_min=2017&time_max=2017&cursor=30&lang=en&count=30&orderby=' \
                   'date&filter=%7B%22filters%22%3A%5B%5D%7D&time_min=2017&time_max=2017' \
                   '&search='
        # next_url返回json
        # 同样进入主界面
