# encoding = utf-8
import scrapy
from scrapy.http import Request
import re
from datetime import datetime
from ..items import HuaceItem
from urllib import parse
from scrapy.loader import ItemLoader


class GubaSpider(scrapy.Spider):
    name = 'guba'

    allowed_domains = ['http://guba.eastmoney.com/']
    start_urls = ['http://guba.eastmoney.com/list,300133_1.html']
    current_page = 1
    Chinese_New_Year = ['2018-02-15', '2017-01-27', '2016-02-07',
                        '2015-02-18', '2014-01-30', '2013-02-09',
                        '2012-01-22', '2011-02-02']

    def parse(self, response):
        """
        1: get url list for further analysis
        2: get url of next page
        :param response:
        :return:
        """
        for info in response.xpath('//div[@id="articlelistnew"]/div[contains(@class, "articleh")]'):
            url = info.xpath('span[@class="l3"]/a/@href').extract_first()
            if url is not None and 'news' in url:
                yield Request(url=parse.urljoin(response.url, url), callback=self.parse_detail, dont_filter=True)

        GubaSpider.current_page += 1
        if GubaSpider.current_page <= 267:
            next_page_url = 'http://guba.eastmoney.com/list,300133_' + \
                            str(GubaSpider.current_page) + '.html'

            yield Request(url=next_page_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        if '404.aspx' not in response.url:
            # check time
            time_str = response.xpath('//div[@class="zwfbtime"]/text()').extract_first().strip()
            if self.check_time(time_str.split(" ")[1]):
                item = ItemLoader(item=HuaceItem())

                time = time_str.split(" ")[1] + " " + time_str.split(" ")[2]
                item.add_value('time', time)

                title = re.sub(r'\s', '', response.xpath('//div[@id="zwconttbt"]/text()').extract_first().strip())
                item.add_value('title', title)

                content_path = response.xpath('//div[@id="zwconbody"]/div[@class="stockcodec"]')
                content = re.sub(r'\s', '', content_path[0].xpath('string(.)').extract_first())
                item.add_value('content', content)

                for info in response.xpath('//div[@id="zwlist"]/div[@class="zwli clearfix"]'):
                    commment = re.sub(r'\s', '', info.xpath('div[@class="zwlitx"]/div[@class="zwlitxt"]/'
                                                            'div[contains(@class, "stockcodec")]/text()').
                                      extract_first().strip())
                    item.add_value('comment', commment)
                return item.load_item()

    def check_time(self, publish_time):
        """
        check the time
        :param publish_time:
        :return:
        """
        for year in GubaSpider.Chinese_New_Year:
            if publish_time[0:4] in year:
                start_time = datetime.strptime(year, '%Y-%m-%d')
                end_time = datetime.strptime(publish_time, '%Y-%m-%d')
                days = abs((start_time - end_time).days)
                if days <= 30:
                    return True
        return False

