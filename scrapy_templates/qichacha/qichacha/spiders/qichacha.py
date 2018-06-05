import logging.config
import os
import time
from urllib.parse import quote

import scrapy
import xlrd
from bs4 import BeautifulSoup
from scrapy.http import Request
from urllib.parse import quote


from items import QichachaItem

logger = logging.getLogger('soccer')

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')


class QichachaSpider(scrapy.Spider):
    name = 'qichachaspider'
    allowed_domains = ['qichacha.com']
    header = {
        'Host': 'www.qichacha.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.5',
        'Cache-Control': 'max-age=0',
        'Cookie': 'acw_tc=AQAAAPsPx14riAgAF3zfdgPnXspofkC7; PHPSESSID=fh1a4sk2upjqdr5nq4dvl3krs2; UM_distinctid=16325c83aa814c-09293b2b255171-3b7c015b-1fa400-16325c83aa9168d; zg_did=%7B%22did%22%3A%20%2216325c83ab4619-0892953ddee5b2-3b7c015b-1fa400-16325c83ab716a%22%7D; _uab_collina=152534727141551053723082; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1525347270,1525355036; _umdata=0712F33290AB8A6DE8A6A7E152EBF34BA30F072D4F4B7B4D9C3E1542E897D7C5AEF7A60E7F69AD9ACD43AD3E795C914CA03AB50BBA5C73EFC5E2AD409966215D; hasShow=1; CNZZDATA1254842228=1479707132-1525343680-%7C1525430717; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1525431420; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201525430472062%2C%22updated%22%3A%201525431518084%2C%22info%22%3A%201525347269308%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%228a6f8caea6f05d464d5d1cea1ec36ea2%22%7D',
        'Referer': 'https://www.qichacha.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
    }
    search_url = 'http://www.qichacha.com/search?key='
    target_hrefs = []
    companys = []

    # fs = open('/home/sunlianjie/PycharmProjects/happy-spiders/scrapy_templates/qichacha/qichacha/data/test.txt', 'a')

    def start_requests(self):
        data = xlrd.open_workbook(os.path.join(data_dir, 'Firm_May02.xlsx'))
        table = data.sheets()[0]
        row = 101
        for i in range(1, row):
            rowValues = table.row_values(i)  # 某一行数据
            self.companys.append(rowValues[0].strip())
        for company in self.companys:
            time.sleep(3)
            keywords_encode = quote(company)
            yield Request(url=self.search_url + keywords_encode, meta={'company': company}, dont_filter=True,
                          headers=self.header,
                          callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            result = soup.select('.m_srchList > tbody > tr')[0]
            taget_url = 'https://www.qichacha.com/' + result.find('a').get('href').strip()
            logger.info('已抓取ip https://www.qichacha.com/' + result.find('a').get('href').strip() + '\n')
            yield Request(url=taget_url, dont_filter=True, meta={'company': response.meta['company']},
                          headers=self.header,
                          callback=self.get_detail)
        except BaseException as error:
            print('搜不到 ', error, response.text)

    # 获取细节信息函数
    def get_detail(self, response):
        basic_list = {}
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find('section', id='Cominfo').find_all('table')[-1].find_all('tr')
        # 企业名
        basic_list['name'] = response.meta['company']
        # 官网
        try:
            basic_list['websiteList'] = soup.find('div', 'content').find_all('div', 'row')[2].find_all('span', 'cvlu')[
                -1].get_text()
        except:
            basic_list['websiteList'] = ''

        # 邮箱
        try:
            basic_list['email'] = \
                soup.find('div', 'content').find_all('div', 'row')[2].find_all('span', 'cvlu')[
                    0].get_text()
        except:
            basic_list['email'] = ''

        # 联系方式
        try:
            basic_list['phone'] = soup.find('div', 'content').find_all('div', 'row')[1].find('span',
                                                                                             'cvlu').span.get_text().strip()
        except:
            basic_list['phone'] = ''

        # 注册号：
        try:
            basic_list['regNumber'] = content[2].find_all('td')[1].get_text().strip()
        except:
            basic_list['regNumber'] = ''

        # 成立日期：
        try:
            basic_list['estiblishTime'] = content[1].find_all('td')[3].get_text().strip()
        except:
            basic_list['estiblishTime'] = ''

        # 企业地址：
        try:
            basic_list['regLocation'] = content[9].find_all('td')[1].get_text().strip().split('查看地图')[0].strip()
        except:
            basic_list['regLocation'] = ''
        # 经营范围：
        try:
            basic_list['range'] = content[-1].find_all('td')[1].get_text().strip()
        except:
            basic_list['range'] = ''
        # 英文名称
        try:
            basic_list['english'] = content[-5].find_all('td')[3].get_text().strip()
        except:
            basic_list['english'] = ''
        item = QichachaItem()
        item['company'] = response.meta['company']
        item['websiteList'] = basic_list['websiteList']
        item['email'] = basic_list['email']
        item['phone'] = basic_list['phone']
        item['regNumber'] = basic_list['regNumber']
        item['estiblishTime'] = basic_list['estiblishTime']
        item['regLocation'] = basic_list['regLocation']
        item['range'] = basic_list['range']
        item['english'] = basic_list['english']
        yield item
        # 英文名称
        # 注册时间 1
        # 注册号  1
        # 注册地址 1
        # 经营范围 1
        # 官网  1
        # 电话 1
        # 邮箱 1
