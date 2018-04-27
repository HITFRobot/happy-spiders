# -*- coding: utf-8 -*-
import scrapy


class WaterRegimenSpider(scrapy.Spider):
    name = 'water_regimen'
    # allowed_domains = ['http://www.ctg.com.cn/sxjt/sqqk/index.html']
    start_urls = ['http://http://www.ctg.com.cn/sxjt/sqqk/index.html/']
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=92D39A52B9FDFA4E525288290F0D00C2; Hm_lvt_c1840432ced488aa2e58bd133a0ca7e4=1524624366; Hm_lpvt_c1840432ced488aa2e58bd133a0ca7e4=1524624366',
        'Host': 'www.ctg.com.cn',
        'Origin': 'http://www.ctg.com.cn',
        'Referer': 'http://www.ctg.com.cn/sxjt/sqqk/index.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def parse(self, response):
        pass

    def start_requests(self):
        formdata = 'time=2018-04-27'
        return [scrapy.FormRequest(
            url='http://www.ctg.com.cn/eportal/ui?moduleId=4f104da2afbc4bf59babd925d469491b&&struts.portlet.mode=view&struts.portlet.action=/portlet/waterPicFront!getDatas.action',
            headers=self.headers,
            formdata=formdata,
            callback=self.parse
        )]
