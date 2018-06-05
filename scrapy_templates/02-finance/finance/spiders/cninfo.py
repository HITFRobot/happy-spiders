# -*- coding: utf-8 -*-
import scrapy
import json
from items import CNInfoItem


class CninfoSpider(scrapy.Spider):
    name = 'cninfo'
    # allowed_domains = ['http://www.cninfo.com.cn/cninfo-new/announcement/show']
    start_urls = ['http://http://www.cninfo.com.cn/cninfo-new/announcement/show/']
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.cninfo.com.cn/cninfo-new/announcement/show',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=8EB1707CEF21628CC4339BD23B0C26DF',
        'Host': 'www.cninfo.com.cn',
        'Origin': 'http://www.cninfo.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    pageNum = 1
    formdata = {
        'stock': '',
        'searchkey': '',
        'plate': '',
        'category': 'category_ndbg_szsh;',
        'trade': '',
        'column': 'szse_main',
        'columnTitle': '历史公告查询',
        'pageNum': str(pageNum),
        'pageSize': '30',
        'tabName': 'fulltext',
        'sortName': '',
        'sortType': '',
        'limit': '',
        'showTitle': '',
        'seDate': '2017-01-01 ~ 2018-01-01'
    }
    cralwered = set()

    def parse(self, response):
        res = json.loads(response.text)
        for announcement in res['announcements']:
            secCode = announcement['secCode']
            secName = announcement['secName']
            announcementTitle = announcement['announcementTitle']
            adjunctUrl = announcement['adjunctUrl']
            if secCode in self.cralwered or '摘要' in announcementTitle:
                continue
            self.cralwered.add(secCode)
            item = CNInfoItem()
            item['site'] = 'cninfo'
            item['files_urls_field'] = 'http://www.cninfo.com.cn/' + adjunctUrl
            item['name'] = secName
            item['date'] = adjunctUrl.split('/')[1]
            item['title'] = announcementTitle
            yield item

        # 获取下一页
        if res['hasMore']:
            self.pageNum += 1
            cookie = response.headers.get('Set-Cookie').decode('utf-8')
            if cookie:
             self.headers['Cookie'] = cookie.split(';')[0]
            self.formdata['pageNum'] = str(self.pageNum)
            yield scrapy.FormRequest(
                url='http://www.cninfo.com.cn/cninfo-new/announcement/query',
                formdata=self.formdata
            )

    def start_requests(self):
        # 第一次post请求
        return [scrapy.FormRequest(
            url='http://www.cninfo.com.cn/cninfo-new/announcement/query',
            headers=self.headers,
            formdata=self.formdata,
            callback=self.parse
        )]
