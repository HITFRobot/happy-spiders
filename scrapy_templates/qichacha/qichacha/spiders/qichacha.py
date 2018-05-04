import scrapy
import logging.config
from bs4 import BeautifulSoup
import time
import xlrd
import random
from scrapy.http import Request

logger = logging.getLogger('soccer')


class QichachaSpider(scrapy.Spider):
    name = 'qichachaspider'
    allowed_domains = ['qichacha.com']
    start_urls = ['https://www.qichacha.com/firm_9e0b9df2f89dfe544d15fc16655d520c.html']
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.5',
        'Connection': 'keep - alive',
        'Host': 'www.qichacha.com',
        'Cookie': 'acw_tc=AQAAAPsPx14riAgAF3zfdgPnXspofkC7; PHPSESSID=fh1a4sk2upjqdr5nq4dvl3krs2; UM_distinctid=16325c83aa814c-09293b2b255171-3b7c015b-1fa400-16325c83aa9168d; zg_did=%7B%22did%22%3A%20%2216325c83ab4619-0892953ddee5b2-3b7c015b-1fa400-16325c83ab716a%22%7D; _uab_collina=152534727141551053723082; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1525347270,1525355036; CNZZDATA1254842228=1479707132-1525343680-%7C1525398269; _umdata=0712F33290AB8A6DE8A6A7E152EBF34BA30F072D4F4B7B4D9C3E1542E897D7C5AEF7A60E7F69AD9ACD43AD3E795C914CA03AB50BBA5C73EFC5E2AD409966215D; hasShow=1; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1525401795; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201525400231778%2C%22updated%22%3A%201525401833516%2C%22info%22%3A%201525347269308%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%228a6f8caea6f05d464d5d1cea1ec36ea2%22%7D',
        'referer': 'https://www.qichacha.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36'

    }
    search_url = 'https://www.qichacha.com/search?key='
    target_hrefs = []
    companys = []

    fs = open('/home/sunlianjie/PycharmProjects/happy-spiders/scrapy_templates/qichacha/qichacha/data/test.txt', 'a')

    def start_requests(self):
        data = xlrd.open_workbook(
            '/home/sunlianjie/PycharmProjects/happy-spiders/scrapy_templates/qichacha/qichacha/data/Firm_May02.xlsx')
        table = data.sheets()[0]
        row = 101
        for i in range(1, row):
            rowValues = table.row_values(i)  # 某一行数据
            self.companys.append(rowValues[0].strip())
        for company in self.companys:
            yield Request(url=self.search_url + company+'/', dont_filter=True, headers=self.header, callback=self.parse)

        time.sleep(random.randint(3, 6))

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        print(response.text)
        try:
            result = soup.select('.m_srchList > tbody > tr')[0]
            self.fs.write('https://www.qichacha.com/' + result.find('a').get('href').strip() + '\n')
            logger.info('已抓取ip https://www.qichacha.com/' + result.find('a').get('href').strip() + '\n')
        except BaseException as error:
            print('搜不到 ')


    # 获取细节信息函数
    def get_detail(self, response):
        basic_list = {}
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find('section', id='Cominfo').find_all('table')[-1].find_all('tr')
        # 企业名
        basic_list['name'] = '西安唯电电气技术有限公司'
        # 官网
        try:
            basic_list['websiteList'] = soup.find('div', 'content').find_all('div', 'row')[2].find_all('span', 'cvlu')[
                -1].get_text()
        except:
            basic_list['websiteList'] = ''

        # 邮箱
        try:
            basic_list['emainl'] = \
                soup.find('div', 'content').find_all('div', 'row')[2].find_all('span', 'cvlu')[
                    0].get_text()
        except:
            basic_list['emainl'] = ''

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
        print(basic_list)


        # 英文名称
        # 注册时间 1
        # 注册号  1
        # 注册地址 1
        # 经营范围 1
        # 官网  1
        # 电话 1
        # 邮箱 1
