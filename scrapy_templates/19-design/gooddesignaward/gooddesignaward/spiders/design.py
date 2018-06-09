# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import GooddesignawardItem
from urllib import parse
from ..utils import *
import re


class DesignSpider(scrapy.Spider):
    name = 'design'
    # allowed_domains = ['http://www.g-mark.org/award/search?from=2016&to=2016&prizeCode=GOLD&keyword=']
    code_name_map = {
        'GOLD': 'Good Design Gold Award',
        'GRAND': 'Good Design Grand Award',
        'FUTURE_DESIGN': 'Good Design Special Award [Design for the Future]',
        'SME': 'Good Design Prize of Small and Medium Enterprises',
        'JCCI': 'Good Design Prize of the Japan Chamber of Commerce and Industry',
        'JDP_CHAIRMAN': 'Good Design Special Award [Disaster Recovery Design]',
        'BEST100': 'Good Design Best100',
        'LONGLIFE': 'Good Design Long Life Design Award',
        'JDP_GLOBAL_DESIGN_2013': 'Global Design 2013',
        'LONGLIFE_SPECIAL': 'Good Design Long Life Design Special Award',
        'SUSTAINABLE_DESIGN': 'Good Design Sustainable Design Award',
        'FRONTIER': 'Good Design Frontier Design Award',
        'LIFE_SCAPE_DESIGN': 'Good Design Life-Scape Design Award',
        'UNIVERSAL_DESIGN': 'Universal Design Prize',
        'ECOLOGY_DESIGN': 'Ecology Design Prize',
        'INTERACTION_DESIGN': 'Interaction Design Prize',
        'JUDGEING_COMMITTEE_CHAIRMAN': 'Good Design Special Award of Judging Committee Chairman',
        'DESIGN_MANAGEMENT': 'Design Management Prize',
        'MEDIA_DESIGN': 'Media Design Prize',
        'PRESENTATION': 'Good Design Presentation Special Prize',
        'URBAN_DESIGN': 'Urban Design Prize',
        'ANNUAL_MANAGEMENT': 'Annual Management Prize',
        'SME_20TH': '20th Anniversary Prize for Small and Medium Enterprises',
        'MITI_20TH': '20th Anniversary Prize of Minister of Ministry of International Trade and Industry',
        'ITA_20TH': '20th Anniversary Prize of International Trade Administration Bureau',
        'LONGLIFE_20TH': '20th Anniversary Prize for Long-selling',
        'INTERFACE': 'Prize for Interface',
        'FOREIGN_PRODUCTS': 'Prize for Foreign Products',
        'LANDSCAPE': 'Prize for Items in Harmony with the Landscape',
        'SOCIAL_CONSCIOUS_PRODUCTS': 'Prize for Social-Conscious Products',
        'JIDPO_INSTRUCTION': 'JIDPO Special Prize -Prize for Instruction of Domestic Media Equipment-',
        'JIDPO_ECOLOGY': 'JIDPO Special Prize -Prize for Ecology-Conscious Products-'
    }
    # start_urls = ['http://http://www.g-mark.org/award/search?from=2016&to=2016&prizeCode=GOLD&keyword=/']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        # 'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '__utmz=8664483.1528363251.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SESSION=981abe1b-608b-4c86-bde4-b954cee51014; __utma=8664483.143095238.1528363251.1528441590.1528509701.5; __utmc=8664483; __utmt=1; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=zh_CN; __utmb=8664483.8.10.1528509701',
        'Host': 'www.g-mark.org',
        'Referer': 'http://www.g-mark.org/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    def start_requests(self):
        for year in range(2017, 2018):  # 遍历年份
            for code in self.code_name_map:
                url = 'http://www.g-mark.org/award/search?from={}&to={}&prizeCode={}&keyword='.format(year, year, code)
                yield Request(url=url, headers=self.headers, callback=self.parse_award,
                              meta={'year': year, 'code': code})
            # time.sleep(random.randint(10, 20))
            # 其他奖项
            yield Request(url='http://www.g-mark.org/award/search/standard?year={}&lastAwardNo='.format(year),
                          callback=self.parse_more, meta={'year': year})

    def parse_award(self, response):
        item_urls = response.css('.itemList > li > a[data-pjax="#result"]::attr(href)').extract()
        for item_url in item_urls:
            yield Request(url=parse.urljoin(response.url, item_url),
                          headers=self.headers, callback=self.parse_detail,
                          meta={'year': response.meta['year'], 'code': response.meta['code']})

    def parse_more(self, response):
        if 'Nothing matched to the condition.' in response.text:
            return
        item_urls = response.css('.itemList > li > a[data-pjax="#result"]::attr(href)').extract()
        for item_url in item_urls:
            yield Request(url=parse.urljoin(response.url, item_url),
                          headers=self.headers, callback=self.parse_detail,
                          meta={'year': response.meta['year']})
        ## 再次点击more
        last_url = response.css('.itemList > li:last-child > a > figure > img::attr(data-original)').extract_first()
        lastNum = last_url.split('/')[-2]
        yield Request(url='http://www.g-mark.org/award/search/standard?year={}&lastAwardNo={}'
                      .format(response.meta['year'], lastNum),
                      callback=self.parse_more,
                      meta={'year': response.meta['year']})

    def parse_detail(self, response):
        item = GooddesignawardItem()
        # 0. url
        url = response.url
        # 1. 获奖年份
        try:
            year = response.css('#detailArea > h1 > img::attr(alt)').extract_first()
        except:
            year = response.meta['year']
        # 2. 奖项名称
        try:
            if 'code' in response.meta:
                award = self.code_name_map[response.meta['code']]
            else:
                award = response.css('#detailArea > section > h2 > img::attr(alt)').extract_first()
        except:
            award = ''
        name = ''
        business = ''
        category = ''
        company = ''
        number = ''
        outline = ''
        producer = ''
        director = ''
        designer = ''
        information = ''
        date = ''
        ## basicinfo
        ## 包含 3, 4, 5, 6, 7 页面上可能缺失 通过关键字匹配
        elements = response.css('#detailArea > section > dl > *')
        for i in range(len(elements)):
            cur = elements[i]
            # 3. 作品名称
            try:
                if 'Award-winning item' in cur.xpath('string(.)').extract_first():
                    next = elements[i + 1]
                    name = next.xpath('string(.)').extract_first()
            except:
                name = ''
            # 4. 主要实施业务
            try:
                if 'Principal implementing business' in cur.xpath('string(.)').extract_first():
                    next = elements[i + 1]
                    business = next.xpath('string(.)').extract_first()
            except:
                business = ''
            # 5. 产品分类
            try:
                if 'Category' in cur.xpath('string(.)').extract_first():
                    next = elements[i + 1]
                    category = next.xpath('string(.)').extract_first()
            except:
                category = ''
            # 6. 公司 国家
            try:
                if 'Company(Nationality)' in cur.xpath('string(.)').extract_first():
                    next = elements[i + 1]
                    company = next.xpath('string(.)').extract_first()
                    company = re.sub('\s', '', company)
            except:
                company = ''
            # 7. 奖项编号
            try:
                if 'Award Number' in cur.xpath('string(.)').extract_first():
                    next = elements[i + 1]
                    number = next.xpath('string(.)').extract_first()
            except:
                number = ''
        ## 概要信息块
        ## 包含 8, 9, 10, 11,12,13
        elements = response.css('#detailArea > article:nth-child(3) > dl > *')
        for i in range(len(elements)):
            cur = elements[i]
            # 8. 作品描述
            try:
                if 'Outline' in cur.xpath('string(.)').extract_first():
                    next = elements[i + 1]
                    outline = next.xpath('string(.)').extract_first()
            except:
                outline = ''
            # 9. 制作商
            try:
                if 'Producer' in cur.xpath('string(.)').extract_first():
                    next = elements[i + 1]
                    producer = next.xpath('string(.)').extract_first()
            except:
                producer = ''
            # 10. 负责人
            try:
                if 'Director' in cur.xpath('string(.)').extract_first():
                    next = elements[i + 1]
                    director = next.xpath('string(.)').extract_first()
            except:
                director = ''
            # 11. 设计师
            try:
                if 'Designer' in cur.xpath('string(.)').extract_first():
                    next = elements[i + 1]
                    designer = next.xpath('string(.)').extract_first()
            except:
                designer = ''
            # 12. 更多信息
            try:
                if 'More information' in cur.xpath('string(.)').extract_first():
                    next = elements[i + 1]
                    information = next.xpath('string(.)').extract_first()
                    information = clean_text(information)
            except:
                information = ''
            # 13. 投放市场时间
            try:
                if 'Already on the market' in cur.xpath('string(.)').extract_first() \
                    or '発売' in cur.xpath('string(.)').extract_first():
                    next = elements[i + 1]
                    date = next.xpath('string(.)').extract_first()
            except:
                date = ''
        try:
            image_urls = response.css('#mainphoto > ul.thumnail > li > a > img::attr(src)').extract()
            if image_urls is None or len(image_urls) == 0:
                image_urls = response.css('#mainphoto > ul > li > a > img::attr(src)').extract()
            images = [url for url in image_urls if 'youtube' not in url]
        except:
            images = []

        item['url'] = url
        item['year'] = year  # 1. 获奖年份
        item['award'] = award  # 2. 奖项名称
        item['name'] = name  # 3. 作品名称
        item['business'] = business  # 4. 主要实施业务
        item['category'] = category  # 5. 产品分类
        item['company'] = company  # 6. 公司 国家
        item['number'] = number  # 7. 奖项编号
        item['outline'] = outline  # 8. 作品描述
        item['producer'] = producer  # 9. 制作商
        item['director'] = director  # 10. 负责人
        item['designer'] = designer  # 11. 设计师
        item['information'] = information  # 12. 更多信息
        item['date'] = date  # 13. 投放市场时间
        item['images'] = images  # 14. 作品图片
        yield item
