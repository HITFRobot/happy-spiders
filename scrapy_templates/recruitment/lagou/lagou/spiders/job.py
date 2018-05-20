# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import JobItem, JobItemLoader
from utils.common import get_md5
from datetime import datetime


class JobSpider(CrawlSpider):
    name = 'job'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/" \
            "537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"

    # if not settings, it will be redirect to login
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'user_trace_token=20171015132411-12af3b52-3a51-466f-bfae-a98fc96b4f90; LGUID=20171015132412-13eaf40f-b169-11e7-960b-525400f775ce; SEARCH_ID=070e82cdbbc04cc8b97710c2c0159ce1; ab_test_random_num=0; X_HTTP_TOKEN=d1cf855aacf760c3965ee017e0d3eb96; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsXIrWUxpNGLE2g_bKzlUCXPTRJMHxfCs6L20RqgCpUq%26wd%3D%26eqid%3Dee53adaf00026e940000000559e354cc; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_hotjob; login=false; unick=""; _putrc=""; JSESSIONID=ABAAABAAAFCAAEG50060B788C4EED616EB9D1BF30380575; _gat=1; _ga=GA1.2.471681568.1508045060; LGSID=20171015203008-94e1afa5-b1a4-11e7-9788-525400f775ce; LGRID=20171015204552-c792b887-b1a6-11e7-9788-525400f775ce',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }

    rules = (
        # Rule(LinkExtractor(allow=('zhaopin/.*',)), follow=True),
        # Rule(LinkExtractor(allow=('gongsi/j\d+.html',)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def parse_job(self, response):
        """
        解析拉勾网的职位
        :param response:
        :return:
        """
        item_loader = JobItemLoader(item=JobItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('title', 'body > div.position-head > div > div.position-content-l > div > span::text')
        item_loader.add_xpath('salary', '/html/body/div[2]/div/div[1]/dd/p[1]/span[1]/text()')
        item_loader.add_xpath('job_city', '/html/body/div[2]/div/div[1]/dd/p[1]/span[2]/text()')
        item_loader.add_xpath('work_years', '/html/body/div[2]/div/div[1]/dd/p[1]/span[3]/text()')
        item_loader.add_xpath('degree_need', '/html/body/div[2]/div/div[1]/dd/p[1]/span[4]/text()')
        item_loader.add_xpath('job_type', '/html/body/div[2]/div/div[1]/dd/p[1]/span[5]/text()')
        item_loader.add_css('publish_time', 'body > div.position-head > div > div.position-content-l > dd > p.publish_time::text')
        item_loader.add_css('tags', 'body > div.position-head > div > div.position-content-l > dd > ul > li::text')
        item_loader.add_css('job_advantage', '#job_detail > dd.job-advantage > p::text')
        item_loader.add_css('job_desc', '#job_detail > dd.job_bt > div')
        item_loader.add_css('job_addr', '#job_detail > dd.job-address.clearfix > div.work_addr')
        item_loader.add_css('company_url', '#job_company > dt > a::attr(href)')
        item_loader.add_css('company_name', '#job_company > dt > a > img::attr(alt)')
        item_loader.add_value('crawl_time', datetime.now())
        job_item = item_loader.load_item()
        return job_item