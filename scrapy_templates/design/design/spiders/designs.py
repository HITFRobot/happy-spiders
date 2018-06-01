# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from .util import parse_json_str
import sys
from ..items import DesignItem
import json
import time
import random


class DesignsSpider(scrapy.Spider):
    name = 'designs'
    # allowed_domains = ['ifworlddesignguide.com']
    start_urls = ['https://ifworlddesignguide.com/design-excellence?time_min=1954&time_max=1954']
    url = 'https://ifworlddesignguide.com/design-excellence?time_min=1954&time_max=1954'

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

    cursor = 30

    def start_requests(self):
        yield Request(url=self.url, callback=self.parse)

    def parse(self, response):
        content_type = response.headers['Content-Type'].decode(encoding='utf-8', errors='strict')
        try:
            if response.status == 200 and 'html' in content_type:
                json_obj = parse_json_str(response.text)
                # "根据json_obj进入detail"
            elif response.status == 200 and 'json' in content_type:
                json_obj = json.loads(response.body_as_unicode())
            else:
                raise Exception('error')
        except Exception as error:
            print('error')
            sys.exit()
        # yield第一次请求的内容的目标url
        articles = json_obj['articles']
        if len(articles) != 0:
            for article in articles:
                href = article['href']
                yield Request(url='https://ifworlddesignguide.com/' + href, callback=self.parse_detail)
                time.sleep(random.randint(1, 4))

            # 获得下一页请求
            next_url = 'https://my.ifdesign.de/WdgService/articles/design_excellence?' \
                       'time_min=1954&time_max=1954&cursor='+str(self.cursor)+'&lang=en&count=30&orderby=' \
                       'date&filter=%7B%22filters%22%3A%5B%5D%7D&time_min=1954&time_max=1954' \
                       '&search='
            yield Request(url=next_url, callback=self.parse)
            self.cursor += 30
            # next_url返回json
            # 同样进入主界面

    def parse_detail(self, response):
        item = DesignItem()
        # 1、名称
        name = response.css('body > main > div > div:nth-child(1) > h1 > span.product-name::text').extract_first()
        # 2、分类
        type = response.css(
            'body > main > div > div:nth-child(1) > h1 > span.product-type > span::text').extract_first()
        # 3、类别
        discipline = response.css(
            'body > main > div > div.product-detail-page-images > div:nth-child(3) > div > div > h2::text').extract_first()
        # 4、年份
        year = response.css(
            'body > main > div > div.row.profile-text > div > div > ul > li:nth-child(1) > span.column.small-6.xxlarge-7::text').extract_first()
        # 5、开发时间
        development = response.css(
            'body > main > div > div.row.profile-text > div > div > ul > li:nth-child(3) > span.column.small-6.xxlarge-7::text').extract_first()
        # 6、目标地区
        regions = response.css(
            'body > main > div > div.row.profile-text > div > div > ul > li:nth-child(5) > span.column.small-6.xxlarge-7::text').extract_first()
        # 7、目标群体
        groups = response.css(
            'body > main > div > div.row.profile-text > div > div > ul > li:nth-child(7) > span.column.small-6.xxlarge-7::text').extract_first()
        # 8、评价标准
        try:
            criteria = groups = response.css(
            'body > main > div > div.row.profile-text > div > div > ul > li:nth-child(9) > span.column.small-6.xxlarge-7::text').extract_first()  # 有的目标页面没有
        except:
            criteria = ''
        ## Client/Manufacturer
        clients = []
        clients_divs = response.css('body > main > div > div.row.align-right > div:nth-child(1) > div')
        for client_div in clients_divs:
            client = {}
            # 9、生产企业
            manufacturer = client_div.css('h2::text').extract_first()
            # 10、所在地区
            location = '/'.join(client_div.css('p::text').extract())
            client['manufacturer'] = manufacturer
            client['location'] = location
            clients.append(client)
        ## University （没找到在哪）
        universities = []
        ## Design
        designs = []
        design_divs = response.css('body > main > div > div.row.align-right > div:nth-child(2)')
        for design_div in design_divs:
            design = {}
            # 11、设计企业
            try:
                design_company = design_div.css('h2::text').extract_first()
            except:
                design_company = ''
            # 12、所在地区
            try:
                location = '/'.join(design_divs[0].css('p::text').extract()[0:-1])
            except:
                location = ''
            # 13、设计师
            try:
                designer = design_divs[0].css('p::text').extract()[-1]
            except:
                designer = ''
            design['design_company'] = design_company
            design['location'] = location
            design['designer'] = designer
            designs.append(design)
        # 14、作品图片1
        img1 = response.css('body > main > div > div.product-detail-page-images > div:nth-child(1) > div > div > img::attr(data-src)').extract_first()
        # 15、作品图片2
        img2 = response.css('body > main > div > div.product-detail-page-images > div:nth-child(2) > div > div > img::attr(data-src)').extract_first()
        # 16、作品图片3
        img3 = response.css('body > main > div > div.product-detail-page-images > div:nth-child(3) > div > div > img::attr(data-src)').extract_first()
        # 17、产品描述
        description = response.css('body > main > div > div:nth-child(3) > div > p::text').extract_first()

        item['name'] = name
        item['type'] = type
        item['discipline'] = discipline
        item['year'] = year
        item['development'] = development
        item['regions'] = regions
        item['groups'] = groups
        item['criteria'] = criteria
        item['clients'] = clients
        item['universities'] = universities # 没找到在哪
        item['designs'] = designs
        item['img1'] = img1
        item['img2'] = img2
        item['img3'] = img3
        item['description'] = description
        yield item