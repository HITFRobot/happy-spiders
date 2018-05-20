__author__ = 'Lijian Sun'

import scrapy
from urllib import parse
from scrapy.http import Request
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor


class houseSpider(scrapy.Spider):
    """
    这是关于深圳市一手房源的爬虫程序
    version1：全市
    """
    name = 'houseSpider'
    # allowed_domains = ['']
    start_url = 'http://61.144.226.84/bol/'
    start_urls = ['http://61.144.226.84/bol/']
    current_page = 2

    def parse(self, response):
        """
        1. 获取文章列表页中的文章url并交给解析函数进行具体字段的解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        :param response:
        :return:
        """

        # 获取要爬取的目标页面的URL
        url_tags = response.xpath('//tr[contains(@bgcolor, "#F5F9FC")]/td/a')
        for url_tag in url_tags:
            url = parse.urljoin(response.url, url_tag.css('::attr(href)').extract_first(''))
            if 'projectdetail' in url:
                # print("项目信息：%s" % url)
                yield Request(url=url, callback=self.parse_project)
            else:
                # print("预售证号：%s" % url)
                yield Request(url=url, callback=self.parse_cert)
        # 获取总页数
        total_num = int(response.css('#AspNetPager1 b::text').extract()[2])
        # 进入下一页
        __VIEWSTATE = response.css('#__VIEWSTATE::attr(value)').extract_first('')
        __VIEWSTATEGENERATOR = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract_first('')
        __EVENTVALIDATION = response.css('#__EVENTVALIDATION::attr(value)').extract_first('')
        if houseSpider.current_page <= total_num:
            yield scrapy.FormRequest(
                url=houseSpider.start_url,
                formdata={'__VIEWSTATE': __VIEWSTATE,
                          '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                          '__EVENTVALIDATION': __EVENTVALIDATION,
                          'AspNetPager1_input': str(houseSpider.current_page),
                          'AspNetPager1': 'go',
                          '__EVENTTARGET': '',
                          '__EVENTARGUMENT': '',
                          '__VIEWSTATEENCRYPTED': '',
                          'tep_name': '',
                          'organ_name': '',
                          'site_address': ''},
                callback=self.parse
            )
            houseSpider.current_page += 1
        else:
            pass

    def parse_project(self, response):
        """
        爬取解析project页面的信息
        :param response:
        :return:
        """
        all_tr = response.xpath('//tr[@class="a1"]')[1:-1]
        for tr in all_tr:
            # 提取每一行中的内容
            key_td_list = tr.xpath('td[@bgcolor="#D0E8FB"]')
            value_td_list = tr.xpath('td[re:test(@bgcolor, "#[EFF6FB|F5F9FC]")]')
            # print(len(key_td_list), len(value_td_list))
            for i in range(len(key_td_list)):
                print(key_td_list[i].xpath('div/text()').extract_first('None').strip() + '-->',
                      value_td_list[i].xpath('text()').extract_first('None').strip()
                      if value_td_list[i].xpath('text()').extract_first('None').strip() != '' else
                      value_td_list[i].xpath('div/text()').extract_first('None').strip())

    def parse_cert(self, response):
        """
        爬取cert页面的信息
        :param response:
        :return:
        """
        all_tr = response.xpath('//tr[@class="a1"]')[1:]
        for tr in all_tr:
            # 提取每一行中的内容
            key_td_list = tr.xpath('td[@bgcolor="#FFFFFF"]')
            value_td_list = tr.xpath('td[re:test(@bgcolor, "#F5F9FC")]')
            # print(len(key_td_list), len(value_td_list))
            for i in range(len(key_td_list)):
                print(key_td_list[i].xpath('text()').extract_first('None').strip() + ' --> ',
                      value_td_list[i].xpath('text()').extract_first('None').strip())

