# -*- coding:utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
import requests
import http.cookiejar as cookielib
from ..tools import main_extract, write_excel, getSiheyi, getpai_event, get_mian
from scrapy.http import Request


class SoccerSpider(scrapy.Spider):
    name = 'soccercrawl'
    allowed_domains = ['dszuqiu.com']
    start_urls = ['https://www.dszuqiu.com/diary/20171108']
    global page_num
    global total_page
    total_page = 0
    global pages_number
    pages_number = []
    page_num = 1

    headers = {
        'referer': 'https://www.dszuqiu.com/login',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        'origin': 'https://www.dszuqiu.com',
        'content-type': 'application/x-www-form-urlencoded',
        'accept-encoding': 'gzip, deflate, br'}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # global page_num
        # global pages_number
        # global total_page
        # soup = BeautifulSoup(response.text, "html.parser")
        # if total_page == 0:
        #     total_page = int(soup.select('#pager > ul > li')[-2].text.strip())
        # all_tr = response.css('#diary_info > table > tbody > tr')
        #
        # for tr in all_tr:
        #     a = tr.css('tr > td:nth-child(12) > a')
        #     url = a.css('a::attr(href)').extract()[0]
        #     url_num = url.split('/')[-1]
        #     pages_number.append(url_num)
        # page_num += 1
        # if page_num <= total_page:
        #     yield Request(url=self.start_urls[0] + '/p.' + str(page_num), callback=self.parse,
        #                   dont_filter=True)
        # for number in pages_number:
        #     url = 'https://www.dszuqiu.com/race_xc/' + number
        #     yield Request(url=url, callback=self.parse_one, dont_filter=True, meta={'number': number})
        yield Request(url='https://www.dszuqiu.com/race_xc/413968', callback=self.parse_one)

    def parse_one(self, response):
        # number = response.meta['number']
        # search 现场数据
        return_data = None
        final_time = None
        soup = BeautifulSoup(response.text, "html.parser")
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string is not None:
                if 'draw_half_line' in script.string:
                    return_data, final_time = main_extract(script.string)
                # else:
                #     return
        # 请求红牌数据
        try:
            race_events = soup.select('#race_events')[0]
        except IndexError:
            print('error' + response.meta['number'])
        race_events = race_events.select('li')

        try:
            pai_data = getpai_event(race_events=race_events, max_minute=final_time,
                                zhudui_name=return_data['shezheng'][0]['name'],
                                kedui_name=return_data['shezheng'][1]['name'])
        except BaseException as e:
            raise e

        # 请求main data
        infor_detail = get_mian(soup=soup)

        #请求 四合一数据
        siheyi_data = None
        session = requests.session()
        session.cookies = cookielib.LWPCookieJar(
            filename='/home/sunlianjie/PycharmProjects/happy-spiders/scrapy_templates/soccer/soccer/spiders/cookie')
        try:
            session.cookies.load(ignore_discard=True)
            sp_url = 'https://www.dszuqiu.com/race_sp/413968'
            re = session.get(sp_url, headers=self.headers,
                             allow_redirects=False)
            siheyi_data = getSiheyi(re.text,race_events)
        except BaseException as e:
            raise e
        # if return_data is not None:
        #     write_excel(return_data, final_time, siheyi_data, pai_data, infor_detail, name=number + '.xlsx')

