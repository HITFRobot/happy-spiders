<<<<<<< HEAD
# -*- coding: utf-8 -*-
import scrapy
from ..items import SanXiaItem
=======
# -*- coding:utf-8 -*-  
__author__ = 'conghuai'

# -*- coding: utf-8 -*-
import scrapy
from items import SanXiaItem
>>>>>>> 7d97e3de2fb932a06384b491f0ac30b2208d2248
import json
from datetime import date
from dateutil.rrule import rrule, DAILY
import time
import datetime


class XiluoduSpider(scrapy.Spider):
    name = 'xiluodu'
<<<<<<< HEAD
    url = 'http://www.ctg.com.cn/eportal/ui?moduleId=8a2bf7cbd37c4d4f961ed1a6fbdf1ea8&&struts.portlet.' \
          'mode=view&struts.portlet.action=/portlet/waterFront!getDatas.action'

=======
    url = 'http://www.ctg.com.cn/eportal/ui?moduleId=8a2bf7cbd37c4d4f961ed1a6fbdf1ea8&&struts.portlet.mode=view&struts.portlet.action=/portlet/waterFront!getDatas.action'
>>>>>>> 7d97e3de2fb932a06384b491f0ac30b2208d2248

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
        sx = SanXiaItem()
        sx['name'] = 'xiluodu'
        sx['time'] = response.meta.get('time', '')
        data = json.loads(response.body.decode())
        # 入库
        try:
            rkList = data['rkList']
        except:
            rkList = []
        try:
            sx['rk02'] = rkList[-1]['v']
        except:
            sx['rk02'] = ''
        try:
            sx['rk08'] = rkList[-2]['v']
        except:
            sx['rk08'] = ''
        try:
            sx['rk14'] = rkList[-3]['v']
        except:
            sx['rk14'] = ''
        try:
            sx['rk20'] = rkList[-4]['v']
        except:
            sx['rk20'] = ''
        # 出库
        try:
            ckList = data['ckList']
        except:
            ckList = []
        try:
            sx['ck02'] = ckList[-1]['v']
        except:
            sx['ck02'] = ''
        try:
            sx['ck08'] = ckList[-2]['v']
        except:
            sx['ck08'] = ''
        try:
            sx['ck14'] = ckList[-3]['v']
        except:
            sx['ck14'] = ''
        try:
            sx['ck20'] = ckList[-4]['v']
        except:
            sx['ck20'] = ''
        # 上游
        try:
            syList = data['syList']
        except:
            syList = []
        try:
            sx['sy02'] = syList[-1]['v']
        except:
            sx['sy02'] = ''
        try:
            sx['sy08'] = syList[-2]['v']
        except:
            sx['sy08'] = ''
        try:
            sx['sy14'] = syList[-3]['v']
        except:
            sx['sy14'] = ''
        try:
            sx['sy20'] = syList[-4]['v']
        except:
            sx['sy20'] = ''
        # 下游
        try:
            xyList = data['xyList']
        except:
            xyList = []
        try:
            sx['xy02'] = xyList[-1]['v']
        except:
            sx['xy02'] = ''
        try:
            sx['xy08'] = xyList[-2]['v']
        except:
            sx['xy08'] = ''
        try:
            sx['xy14'] = xyList[-3]['v']
        except:
            sx['xy14'] = ''
        try:
            sx['xy20'] = xyList[-4]['v']
        except:
            sx['xy20'] = ''
        yield sx

    def start_requests(self):
        start = '2016-01-01'
        end = '2018-04-28'
        datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
        while datestart < dateend:
            dt = datestart.strftime('%Y-%m-%d')
            print(dt)
            formdata = {'time': dt}
            post = scrapy.FormRequest(
                url=self.url,
                meta={'time': dt},
                headers=self.headers,
                formdata=formdata,
                callback=self.parse
            )
            datestart += datetime.timedelta(days=1)
            time.sleep(5)
            yield post

<<<<<<< HEAD
=======
        # if type(requests) is list:
        #     for request in requests:
        #         yield request
        # else:
        #     yield requests


>>>>>>> 7d97e3de2fb932a06384b491f0ac30b2208d2248
