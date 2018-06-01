# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from .util import parse_json_str
import sys
from items import DesignItem


class DesignsSpider(scrapy.Spider):
    name = 'designs'
    # allowed_domains = ['ifworlddesignguide.com']
    start_urls = ['https://ifworlddesignguide.com/design-excellence?time_min=2017&time_max=2017']
    url = 'https://ifworlddesignguide.com/design-excellence?time_min=2017&time_max=2017'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=k2slfu98bvak7ina9pfpkkqboo; _ga=GA1.2.1153730110.1527427959; _gid=GA1.2.1362895861.1527427959',
        'Host': 'ifworlddesignguide.com',
        'Referer': 'https://ifworlddesignguide.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    def start_requests(self):
        yield Request(url=self.url, callback=self.parse)

    def parse(self, response):
        try:
            if response.status == 200:
                json_obj = parse_json_str(response.text)
                # "根据json_obj进入detail"
            else:
                raise Exception('error')
        except Exception as error:
            print('error')
            sys.exit()
        # yield第一次请求的内容的目标url
        articles = json_obj['articles']
        for article in articles:
            href = article['href']
            yield Request(url=response.urljoin(href), callback=self.parse_detail)

        # 获得下一页请求
        next_url = 'https://my.ifdesign.de/WdgService/articles/design_excellence?' \
                   'time_min=2017&time_max=2017&cursor=30&lang=en&count=30&orderby=' \
                   'date&filter=%7B%22filters%22%3A%5B%5D%7D&time_min=2017&time_max=2017' \
                   '&search='
        # next_url返回json
        # 同样进入主界面

    def parse_detail(self, response):
        item = DesignItem()
        # 1、名称
        name = response.css('body > main > div > div:nth-child(1) > h1 > span.product-name::text').extract_first()
        # 2、分类
        type = response.css(
            'body > main > div > div:nth-child(1) > h1 > span.product-type > span::text').extract_first()
        # 3、类别
        discipline = response.css(
            'body > main > div > div.product-detail-page-images > div:nth-child(3) > div > div > h2::text').extract_first()
        ## 4 5 6 7
        # 4、年份
        year = ''
        # 5、开发时间
        development = ''
        # 6、目标地区
        regions = ''
        # 7、目标群体
        groups = ''
        # 8、评价标准
        criteria = ''
        lis = response.css('body > main > div > div.row.profile-text > div > div > ul > li')
        for li in lis:
            key = li.css('span.column.small-5::text').extract_first()
            value = li.css('span.column.small-6.xxlarge-7').extract_first()
            if 'DATE OF LAUNCH' in key:
                year = value
            elif 'DEVELOPMENT TIME'in key:
                development = value
            elif 'TARGET REGIONS' in key:
                regions = value
            elif 'TARGET GROUPS' in key:
                groups = value
            elif 'ASSESMENT CRITERIA' in key:
                criteria = value
        ## Client/Manufacturer /// University ///
        clients = []
        universities = []
        designs = []
        divs = response.css('body > main > div > div.row.align-right > div')
        for div in divs:
            title = div.css('span::text').extract_first()
            ## Client/Manufacturer
            if title == 'Client / Manufacturer':
                clients_divs = div.css('div')
                for client_div in clients_divs:
                    client = {}
                    # 9、生产企业
                    manufacturer = client_div.css('h2::text').extract_first()
                    # 10、所在地区
                    location = '/'.join(client_div.css('p::text').extract())
                    client['manufacturer'] = manufacturer
                    client['location'] = location
                    clients.append(client)
            ## University
            elif title == 'University':
                university_divs = div.css('div')
                for university_div in university_divs:
                    university = {}
                    # 9、生产企业
                    school = university_div.css('h2::text').extract_first()
                    # 10、所在地区
                    location = '/'.join(client_div.css('p::text').extract())
                    university['school'] = school
                    university['location'] = location
                    universities.append(university)
            ## Design
            elif title == 'Design':
                design_divs = div.css('div')
                for design_div in design_divs:
                    design = {}
                    # 11、设计企业
                    try:
                        design_company = design_div.css('h2::text').extract_first()
                    except:
                        design_company = ''
                    # 12、所在地区
                    try:
                        location = '/'.join(design_divs[0].css('p::text').extract()[0:-1])
                    except:
                        location = ''
                    # 13、设计师
                    try:
                        designer = design_divs[0].css('p::text').extract()[-1]
                    except:
                        designer = ''
                    design['design_company'] = design_company
                    design['location'] = location
                    design['designer'] = designer
                    designs.append(design)
        # 14、作品图片1
        img1 = response.css('body > main > div > div.product-detail-page-images > div:nth-child(1) > div > div > img::attr(data-src)').extract_first()
        # 15、作品图片2
        img2 = response.css('body > main > div > div.product-detail-page-images > div:nth-child(2) > div > div > img::attr(data-src)').extract_first()
        # 16、产品描述
        description = response.css('body > main > div > div:nth-child(3) > div > p::text').extract_first()

        item['name'] = name
        item['type'] = type
        item['discipline'] = discipline
        item['year'] = year
        item['development'] = development
        item['regions'] = regions
        item['groups'] = groups
        item['criteria'] = criteria
        item['clients'] = clients
        item['universities'] = universities # 没找到在哪
        item['designs'] = designs
        item['img1'] = img1
        item['img2'] = img2
        item['description'] = description
        yield item