# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import time
import random
from bs4 import BeautifulSoup


class YellowpagesSpider(scrapy.Spider):
    name = 'yellowpages'
    allowed_domains = ['yellowpages.com']
    start_urls = 'https://www.yellowpages.com/search?search_terms=Chinese Restaurants&geo_location_terms=TX'
    headers = {
        'Accept': 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.yellowpages.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
    }
    page = 2

    def start_requests(self):
        yield Request(url=self.start_urls, headers=self.headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        if response.status != 200:
            raise BaseException('状态码不是200')
        soup = BeautifulSoup(response.text, 'lxml')
        if soup.find(id='no-results-main'):
            raise BaseException('没有搜索到结果，当前页数为%d'.format(self.page))
        for div in soup.find_all(class_='phones phone primary'):
            print(div.get_text())
        url = self.start_urls + '&page=' + str(self.page)
        self.page += 1
        yield Request(url=url, headers=self.headers, callback=self.parse, dont_filter=True)
        time.sleep(random.randint(2, 5))
