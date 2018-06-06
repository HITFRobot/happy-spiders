import scrapy
from scrapy.http import Request
import json
import urllib
import requests
import re
from bs4 import BeautifulSoup
from ..items import RedstardesignItem


class DesignSpider(scrapy.Spider):
    name = 'redstarspider'
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

        award = ['至尊金奖', '银奖', '最佳团队奖', '原创奖金奖', '原创奖', '未来之星奖', '金奖', '红星奖', '最佳新人奖', '原创奖银奖', '优秀设计师奖', ]
        form_data_one = {
            'cmd': 'getProTypeList',
            'type': '0',
            'yearid': self.year_id[this_year]
        }
        response = requests.post(url='http://www.redstaraward.org/ajax/AjaxHandler_HXJGW_GW.ashx',
                                 data=form_data_one)
        print(urllib.parse.unquote(response.text))


        # form_data = {
        #     'cmd': 'getProList',
        #     'page': '1',
        #     'key': '原创奖',
        #     'type': '0',
        #     'yearid': self.year_id[this_year]
        # }
        # yield scrapy.FormRequest(url='http://www.redstaraward.org/ajax/AjaxHandler_HXJGW_GW.ashx', formdata=form_data,
        #                          callback=self.parse)

    def parse(self, response):

        url_past = 'http://www.redstaraward.org'
        # print(urllib.parse.unquote(response.text))

        design_lists = response.text.split(',')[2]
        html = urllib.parse.unquote(design_lists)
        print(html)
        soup = BeautifulSoup(html, "html.parser")
        urls = soup.select('p > a')
        for url in urls:
            print(url.get('href'))

        yield Request(url=url_past + '/details26_6172.html', headers=self.headers, callback=self.detail_parse)

        # design_lists = eval(response.body.decode('utf-8'))
        # print(design_lists)

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
            description = response.css('.zuopin > div:nth-child(5) > div::text').extract_first()
        except:
            description = ''

        item = RedstardesignItem()

        item['year'] = year
        item['awards_name'] = awards_name
        item['num'] = num

        item['img_path'] = img_path
        item['design_name'] = design_name
        item['product_name'] = product_name
        item['design_unit'] = design_unit
        item['awards'] = awards
        item['description'] = description
