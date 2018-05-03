import scrapy
from scrapy import Request
import requests
from bs4 import BeautifulSoup
import time
import xlrd
import random


class QichachaSpider(scrapy.Spider):
    name = 'qichachaspider'
    allowed_domains = ['qichacha.com']
    start_urls = ['https://www.qichacha.com/firm_9e0b9df2f89dfe544d15fc16655d520c.html']
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.5',
            'Connection': 'keep - alive',
            'Host': 'www.qichacha.com',
            'Cookie': 'acw_tc=AQAAAJaNRg9XdgoAHAE8OhSv82A735R+; PHPSESSID=vo5k1dd26k85u9k37peh076ui3; zg_did=%7B%22did%22%3A%20%2216325bb361a4-058c687e0f5f4f8-7d2c6751-1fa400-16325bb361c986%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201525346416160%2C%22updated%22%3A%201525346972374%2C%22info%22%3A%201525346416166%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%7D; UM_distinctid=16325bb3c74628-0751eee7faacd88-7d2c6751-1fa400-16325bb3c765aa; CNZZDATA1254842228=1890863160-1525345016-%7C1525345016; _uab_collina=152534641801857654209878; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1525346424; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1525346973',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
    }
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.5',
        'Connection': 'keep - alive',
        'Host': 'www.qichacha.com',
        'Cookie': 'acw_tc=AQAAAL7JtHzpCQYABlLFIze+gBmazvF9; PHPSESSID=e2f2q6fk17jlpoum6aon1h4i12; zg_did=%7B%22did%22%3A%20%2216325bb15e8745-002bad24f33e59-3a760e5d-1aeaa0-16325bb15e95f2%22%7D; UM_distinctid=16325bb1721a20-0cb770e116d1ae-3a760e5d-1aeaa0-16325bb17228ca; CNZZDATA1254842228=1356467688-1525344243-%7C1525344243; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1525346643; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1525346643; _uab_collina=152534664346251176687732; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201525346407916%2C%22updated%22%3A%201525347715145%2C%22info%22%3A%201525346407918%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%7D',
        'referer': 'https://www.qichacha.com/firm_9e0b9df2f89dfe544d15fc16655d520c.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

    }
    search_url = 'https://www.qichacha.com/search?key='
    target_hrefs = []
    companys = []

    def start_requests(self):
        data = xlrd.open_workbook('/home/zxy/PycharmProjects/untitled/qichacha/qichacha/data/Firm_May02.xlsx')
        table = data.sheets()[0]
        row = 101
        for i in range(1, row):
            rowValues = table.row_values(i)  # 某一行数据
            self.companys.append(rowValues[0].strip())
        for company in self.companys:
            re = requests.get(self.search_url + company,
                              dont_filter=True, header=self.header)
            soup = BeautifulSoup(re.text, "html.parser")
            try:
                result = soup.select('.m_srchList > tbody > tr')[0]
                search_url = 'https://www.qichacha.com/' + result.find('a').get('href').strip()
            except BaseException:
                print('搜不到 ')
            time.sleep(random.randint(3, 6))
        with open('/home/zxy/PycharmProjects/untitled/qichacha/qichacha/data/test.txt', 'a') as f:
            f.writelines(search_url + '\n')

            # 获取细节信息
            # yield Request('https://www.qichacha.com/firm_a92205d742435c4acd76fe265960cae8.html',
            #               dont_filter=True,
            #               callback=self.get_detail)


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
