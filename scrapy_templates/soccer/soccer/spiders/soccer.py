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
    start_urls = ['https://www.dszuqiu.com/race_xc/178576']

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
        # search 现场数据
        return_data = None
        final_time = None
        soup = BeautifulSoup(response.text, "html.parser")
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string is not None:
                if 'draw_half_line' in script.string:
                    return_data, final_time = main_extract(script.string)

        # 请求 四合一数据
        siheyi_data = None
        session = requests.session()
        session.cookies = cookielib.LWPCookieJar(
            filename='/home/sunlianjie/PycharmProjects/happy-spiders/scrapy_templates/soccer/soccer/spiders/cookie')
        try:
            session.cookies.load(ignore_discard=True)
            re = session.get('https://www.dszuqiu.com/race_sp/178576', headers=self.headers,
                             allow_redirects=False)
            siheyi_data = getSiheyi(re.text)
        except BaseException as e:
            raise e

        # 请求红牌数据
        soup = BeautifulSoup(response.text, "html.parser")
        zhudui_name = soup.select('a.red-color')[0].text.strip()
        kedui_name = soup.select('a.blue-color')[0].text.strip()
        race_events = soup.select('#race_events')[0]
        race_events = race_events.select('li')

        pai_data = getpai_event(race_events=race_events, max_minute=final_time,
                                zhudui_name=return_data['shezheng'][0]['name'], kedui_name=return_data['shezheng'][1]['name'])

        # 请求main data
        infor_detail = get_mian(soup=soup)


        write_excel(return_data, final_time, siheyi_data, pai_data, infor_detail, path=None)

