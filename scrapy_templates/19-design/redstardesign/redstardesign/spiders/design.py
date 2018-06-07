import scrapy
from scrapy.http import Request
import json
import urllib
import requests
import re
from .util import unicode_trans
from bs4 import BeautifulSoup
from ..items import RedstardesignItem


class DesignSpider(scrapy.Spider):
    name = 'redstarspider'
    # global page_num
    # page_num = 1
    year_id = {
        '2017': '5773',
        '2016': '5452',
        '2015': '4475',
        '2014': '3398',
        '2013': '2653',
        '2012': '804',
        '2011': '803',
        '2010': '802',
        '2009': '807',
        '2008': '808',
        '2007': '809',
        '2006': '810'
    }
    award = ['至尊金奖', '银奖', '最佳团队奖', '原创奖金奖', '原创奖', '未来之星奖', '金奖', '红星奖', '最佳新人奖', '原创奖银奖', '优秀设计师奖']
    awardnum = {'至尊金奖': 0, '银奖': 1, '最佳团队奖': 2, '原创奖金奖': 3, '原创奖': 4, '未来之星奖': 5, '金奖': 6, '红星奖': 7, '最佳新人奖': 8,
                '原创奖银奖': 9, '优秀设计师奖': 10}
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'Cookie': 'ASP.NET_SessionId=a01rcs45gkechneweavvnz45; UM_distinctid=163d3fc2a81a9-0f9784b7c2a90a-3a760e5d-1aeaa0-163d3fc2a82340; CNZZDATA1000368224=1350957283-1528265226-%7C1528270679; support@hongru.com=lao=15',
        'Host': 'www.redstaraward.org',
        'Origin': 'http://www.redstaraward.org',
        'Referer': 'http://www.redstaraward.org/museum/new_award.html',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    def start_requests(self):
        this_year = '2017'
        form_data_one = {
            'cmd': 'getProTypeList',
            'type': '0',
            'yearid': self.year_id[this_year]
        }
        yield scrapy.FormRequest(url='http://www.redstaraward.org/ajax/AjaxHandler_HXJGW_GW.ashx',
                                 meta={'this_year': this_year},
                                 formdata=form_data_one, callback=self.get_num)

    def get_num(self, response):
        soup = BeautifulSoup(unicode_trans(response.text), "html.parser")
        numbers = soup.select('p > span')
        temp = []
        this_year = response.meta.get('this_year')
        for num in numbers:
            temp.append(num.text.split('个')[0])
        for key, value in self.awardnum.items():
            print(key, temp[self.awardnum[key]])
            # global page_num
            # 为了get总页数
            page_num = 1
            form_data = {
                'cmd': 'getProList',
                'page': str(page_num),
                'key': key,
                'type': '1',
                'yearid': self.year_id[this_year]
            }
            yield scrapy.FormRequest(url='http://www.redstaraward.org/ajax/AjaxHandler_HXJGW_GW.ashx',
                                     formdata=form_data,
                                     meta={'this_year': this_year, 'award_name': key, 'num': temp[self.awardnum[key]], 'page_num': page_num},
                                     callback=self.parse)

    def parse(self, response):
        # global page_num
        # page_num 即为current_page
        page_num = response.meta['page_num']
        this_year = response.meta.get('this_year')
        key = response.meta.get('award_name')
        num = response.meta.get('num')
        url_past = 'http://www.redstaraward.org'
        design_lists = response.text.split(',')[2]
        html = unicode_trans(design_lists)
        pages_html = unicode_trans(response.text.split(',')[3])
        try:
            # get the total_pages
            total_pages = int(re.findall(".*value\)>(.*)\)\{alert.*", pages_html)[0])
        except:
            total_pages = 0
        print('total pages:', total_pages)

        soup = BeautifulSoup(html, "html.parser")
        urls = soup.select('p > a')
        for url in urls:
            print(url.get('href'))
            yield Request(url=url_past + url.get('href'), meta={'this_year': this_year, 'award_name': key, 'num': num},
                          headers=self.headers, callback=self.detail_parse)
        if total_pages > 1 and page_num < total_pages:
            page_num += 1
            print('will crawl the page_num:', page_num)
            form_data = {
                'cmd': 'getProList',
                'page': str(page_num),
                'key': key,
                'type': '1',
                'yearid': self.year_id[this_year]
            }
            yield scrapy.FormRequest(url='http://www.redstaraward.org/ajax/AjaxHandler_HXJGW_GW.ashx',
                                     formdata=form_data,
                                     meta={'this_year': this_year, 'award_name': key, 'num': num, 'page_num': page_num},
                                     callback=self.parse)

    def detail_parse(self, response):

        try:
            # 图片路径
            img_path = response.css('.only img::attr(src)').extract_first()
        except:
            img_path = ''

        try:
            # 作品名称
            design_name = response.css('.zuopin > div:nth-child(1) > div::text').extract_first()
        except:
            design_name = ''

        try:
            # 生产者
            product_name = response.css('.zuopin > div:nth-child(2) > div::text').extract_first()
        except:
            product_name = ''

        try:
            # 设计单位
            design_unit = response.css('.zuopin > div:nth-child(3) > div::text').extract_first()
        except:
            design_unit = ''

        try:
            # 奖项
            awards = response.css('.zuopin > div:nth-child(4) > div::text').extract_first()
        except:
            awards = ''

        try:

            # 产品介绍
            description = response.css('.zuopin > div:nth-child(6) > div::text').extract_first()
        except:
            description = ''

        item = RedstardesignItem()
        item['year'] = response.meta.get('this_year')
        item['awards_name'] = response.meta.get('award_name')
        item['num'] = response.meta.get('num')

        item['img_path'] = img_path
        item['design_name'] = design_name
        item['product_name'] = product_name
        item['design_unit'] = design_unit
        item['awards'] = awards
        item['description'] = description
        yield item
