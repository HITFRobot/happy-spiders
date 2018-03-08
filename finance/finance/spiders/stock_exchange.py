# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re
import os

from ..items import SEAItemLoader, StockExchangeAnnouncement
from datetime import datetime
from ..utils.common import get_md5


class StockExchangeSpider(scrapy.Spider):
    """
    深圳证券交易所公告信息页面解析类
    http://www.szse.cn/main/disclosure/bsgg_front/
    """
    name = 'stock_exchange'
    # allowed_domains = ['http://www.szse.cn/']
    start_urls = ['http://www.szse.cn/main/disclosure/bsgg_front/']
    current_page = 1

    def parse(self, response):
        """
        1. get every announcement's target url for further analysis
        2. get next page url
        :param response:
        :return:
        """
        announcement_urls = response.css('#TD1 > table > tbody > tr > td.tdline2 > a::attr(href)').extract()
        for announcement_url in announcement_urls:
            yield Request(url=parse.urljoin(response.url, announcement_url), callback=self.parse_detail)

        # next page
        total_num_text = response.css('#Table1 > tbody > tr > td:nth-child(1)::text').extract()[-1]
        match_re = re.match('.*?共(\d+)页', total_num_text)
        if not match_re:
            print('extract total page number error, please check the page source.')
            return
        total_num = int(match_re.group(1))
        if self.current_page <= total_num:
            form_request_text = re.match(".*'(.*)?'", response.css(
                '#Table1 > tbody > tr > td:nth-child(3) > input.cls-navigate-next::attr(onclick)').extract_first()).group(1)
            next_page_url = form_request_text.split('?')[0]
            form_data = form_request_text.split('?', 1)[1].split('&')
            yield scrapy.FormRequest(
                url=parse.urljoin(response.url, next_page_url),
                formdata={
                    'ISAJAXLOAD': form_data[0].split('=')[1],
                    'displayContentId': form_data[1].split('=')[1],
                    'SHOWTYPE': form_data[2].split('=')[1],
                    'CATALOGTYPE': form_data[3].split('=')[1],
                    'ORIGINAL_CATALOGID': form_data[4].split('=')[1],
                    'HEAD': '本所公告', # todo 第二页返回时发现乱码 经测试该字段是固定的 先这样处理
                    'CATALOGID': form_data[6].split('=')[1],
                    'TYPE': form_data[7].split('=')[1],
                    'COUNT': form_data[8].split('=')[1],
                    'ARTICLESOURCE': form_data[9].split('=')[1],
                    'LANGUAGE': form_data[10].split('=')[1],
                    'REPETITION': form_data[11].split('=')[1],
                    'DATESTYLE': form_data[12].split('=')[1],
                    'DATETYPE': form_data[13].split('=')[1],
                    'SEARCHBOXSHOWSTYLE': form_data[14].split('=')[1],
                    'INHERIT': form_data[15].split('=')[1],
                    'USESEARCHCATALOGID': form_data[16].split('=')[1],
                    'REPORT_ACTION': form_data[17].split('=')[1],
                    'PAGESIZE': form_data[18].split('=')[1],
                    'PAGECOUNT': form_data[19].split('=')[1],
                    'RECORDCOUNT': form_data[20].split('=')[1],
                    'PAGENO': form_data[21].split('=')[1],
                },
                callback=self.parse
            )
            self.current_page += 1

    def parse_detail(self, response):
        """
        parse detail announcement content, see http://www.szse.cn/main/disclosure/bsgg_front/39778182.shtml
        :param response:
        :return:
        """
        loader = SEAItemLoader(item=StockExchangeAnnouncement(), response=response)
        loader.add_value('url_object_id', get_md5(response.url))
        loader.add_value('url', response.url)
        loader.add_css('title', '#setBgColor > div > div.yellow_bt15::text')
        loader.add_css('publish_time', '#setBgColor > div > div.botborder1::text')
        # loader.add_css('number', '#setBgColor > div > div.td10 > div > p:nth-child(1) > span::text')
        loader.add_value('content', response.xpath('//*[@id="setBgColor"]/div/div[3]/div').xpath('string(.)').extract())
        # match = re.search('/main/images.*pdf', response.text)
        # if match:
        #     attachment_url = parse.urljoin(response.url, match.group(0))
        #     yield Request(url=attachment_url, callback=self.save_pdf)
        #     loader.add_value('attachment_url', attachment_url)
        # else:
        #     loader.add_value('attachment_url', '')
        loader.add_value('crawl_time', datetime.now())
        return loader.load_item()

    def save_pdf(self, response):
        path = os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../pdfs/stock_exchange'), response.url.split('/')[-1])
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)