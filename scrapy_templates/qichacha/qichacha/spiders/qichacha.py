import scrapy
import logging.config
from bs4 import BeautifulSoup
import time
import xlrd
import random
from scrapy.http import Request
from urllib.parse import quote
import os
from items import QichachaItem

logger = logging.getLogger('soccer')

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')


class QichachaSpider(scrapy.Spider):
    name = 'qichachaspider'
    allowed_domains = ['qichacha.com']
    start_urls = ['https://www.qichacha.com/firm_9e0b9df2f89dfe544d15fc16655d520c.html']
    header = {
        'Host': 'www.qichacha.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.5',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=bmmq40ipoiq3aglhs6i3ca7356; _umdata=E2AE90FA4E0E42DEDC258EB4B5D49A775C9FC424C2F48864C90B287E9158115B2DBA00354522D74BCD43AD3E795C914CD8851C0CAE10D6EC91956A76D0322B25; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201525402723891%2C%22updated%22%3A%201525402957095%2C%22info%22%3A%201525402723893%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1525402811; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1525402724; CNZZDATA1254842228=1442659497-1525399389-https%253A%252F%252Fwww.baidu.com%252F%7C1525399389; _uab_collina=152540281087230668241435; zg_did=%7B%22did%22%3A%20%221632916662d185-04267612bf12478-1d451b27-1fa400-1632916662e625%22%7D; acw_tc=AQAAAFuF2U0EwAwAHAE8Osl5mM8ZeM3e; hasShow=1; UM_distinctid=1632916656e90e-09196927cc1b29-1d451b27-1fa400-1632916656f80a',
        'referer': 'http://www.qichacha.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'

    }
    search_url = 'https://www.qichacha.com/search?key='
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
