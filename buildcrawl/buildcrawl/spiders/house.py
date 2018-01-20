# coding=utf-8

import scrapy
from scrapy.http import Request
from urllib import parse

#获取房源信息的爬虫项目

class HouseSpider(scrapy.Spider):
    name = "housecrewling"
    allowed_domins = ['']
    start_urls = ['http://61.144.226.84/bol/']
    global page_num
    page_num = 1

    def parse(self, response):
        # 获取每个目标页面的URL
        global page_num
        postnodes=response.css('#DataList1 tr a')

        #postnodes = response.xpath('//tr[@bgcolor="#F5F9FC"]//a/@href').extract()

        for postnode in postnodes:
            #截取url判断
            post_url = postnode.css('a::attr(href)').extract()[0]

            #获取的文本
            #text=postnide.css('a::text').extract()[0]

            if "projectdetail" in post_url:
                #第一个表格页面
                yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_projectdetail)
            else:
                #第二个表格页面
                yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_centerdetail)
                #utf8string = text.encode("utf-8")
                #print utf8string


        #获取下一页，先得到post请求的各种参数
        next_url='http://61.144.226.84/bol/index.aspx'
        next_VIEWSTATE = response.css('#__VIEWSTATE::attr(value)').extract_first()
        next_IEWSTATEGENERATOR = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract_first()
        next_EVENTVALIDATION = response.css('#__EVENTVALIDATION::attr(value)').extract_first()
        next_AspNetPager1 = 'go'
        page_num+=1
        AspNetPager1_input = page_num
        #总共104页
        if page_num<=104:
            #发送post请求
            yield scrapy.FormRequest(url=next_url, formdata={'__VIEWSTATE': next_VIEWSTATE
                , '__IEWSTATEGENERATOR': next_IEWSTATEGENERATOR, '__EVENTVALIDATION': next_EVENTVALIDATION,
                                                             'AspNetPager1_input': str(AspNetPager1_input),
                                                             'AspNetPager1': next_AspNetPager1,
                                                             '__EVENTTARGET':'',
                                                             '__EVENTARGUMENT':'',
                                                             '__VIEWSTATEENCRYPTED':'',
                                                             'site_address':'',
                                                             'tep_name':'',
                                                             'organ_name':''},
                                     callback=self.parse)

    def parse_projectdetail(self, response):
        #获取project页面的具体内容
        all_td = response.css('.a1 td')
        all_keytd = all_td.css('td[bgcolor="#D0E8FB"]')
        #all_valuetd=all_td.xpath('//td[@bgcolor="#EFF6FB"] | //td[@bgcolor="#F5F9FC"]')[2:]
        all_valuetd = all_td.css('td[bgcolor="#EFF6FB"],td[bgcolor="#F5F9FC"]')[2:]
        td_count = len(all_keytd)

        for i in range(td_count):
            key = all_keytd[i].css('div::text').extract_first('none')
            #value = all_valuetd[i].xpath('div/text()').extract_first('none')
            value = all_valuetd[i].css('div::text').extract_first('none')
            if value=='none':
                value = all_valuetd[i].css('td::text').extract_first('none')
            print(key + "--" + value)


    def parse_centerdetail(self,response):
        # 获取center页面的具体内容
        all_td = response.css('.a1 td')
        all_keytd =all_td.css('td[bgcolor="#FFFFFF"]')
        all_valuetd = all_td.css('td[bgcolor="#F5F9FC"]')[1:]
        td_count=len(all_keytd)
        for i in range(td_count):
            key = all_keytd[i].css('td::text').extract()[0]
            value = all_valuetd[i].css('td::text').extract()[0]
            print(key+ "---" + value)



