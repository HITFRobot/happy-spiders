# -*- coding:utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
import json
from scrapy.http import Request

from PIL import Image
from urllib.request import urlretrieve


class SoccerSpider(scrapy.Spider):
    name = 'soccercrawl'
    allowed_domains = ['dszuqiu.com']
    a = 'https://www.dszuqiu.com'
    start_urls = ['https://www.dszuqiu.com/race_xc/178576']
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.5',
            'Connection': 'keep - alive',
            'Host': 'www.dszuqiu.com',
            'Cookie': 'Hm_lvt_a68414d98536efc52eeb879f984d8923=1524142601; _ga=GA1.2.698961977.1524142601; _gid=GA1.2.1986324845.1524142601',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
        }
    }

    def start_requests(self):
        return [Request("https://www.dszuqiu.com/login",
                        callback=self.post_login)]  # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数

    def post_login(self, response):
        print('login')
        image_url = self.a + response.css('#img_captcha::attr(src)').extract_first()
        print(image_url)
        urlretrieve(image_url, 'captcha.jpg')
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
        captcha = input(u'输入验证码:')

    # def parse(self, response):
    #     soup = BeautifulSoup(response.text, "html.parser")
    #     scripts = soup.find_all('script')
    #     cont = ''
    #     for script in scripts:
    #         if script.string is not None:
    #             if 'draw_half_line' in script.string:
    #                 print(script.string)
