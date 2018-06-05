# coding=utf-8

import scrapy
from scrapy.http import Request
from urllib import parse
import json
from ..items import CsdnArticleItenm
import datetime


# 获取csdn某一大V博客文章的爬虫项目

class CsndSpider(scrapy.Spider):
    name = 'csdncrewling'
    allowed_domains = ['blog.csdn.net']
    start_urls = ['http://blog.csdn.net/Uwr44UOuQcNsUQb60zk2/article/list']

    def parse(self, response):
        postnodes = response.css('#main .blog-units a')
        comment_num_list = response.css(

            '#main .blog-units .unit-control.clearfix.bottom-dis-16  div div:nth-child(4) span')
        if postnodes:
            for postnode, comment_num_span in zip(postnodes, comment_num_list):
                # 截取目标url和评论数
                post_url = postnode.css('a::attr(href)').extract()[0]
                comment_num = comment_num_span.css('span::text').extract()[0]

                yield Request(url=post_url, meta={'comment_num': comment_num}, callback=self.parse_blogdetail)

        # 下一页
        next_url = response.css('.blog-detail div:nth-child(4) li:last-child a::attr(href)').extract()[0]
        if next_url is not None:
            yield Request(url=next_url, callback=self.parse)

    def parse_blogdetail(self, response):
        # 获取文章具体内容
        blog_item = CsdnArticleItenm()
        blog_item['url'] = response.url
        blog_item['blog_title'] = response.css('main article > h1::text').extract()[0]
        blog_item['push_date'] = response.css('main article >div >div >span.time::text').extract()[0]
        try:
            blog_item['push_date'] = datetime.datetime.strptime(blog_item['push_date'], '%Y年%m月%d日 %H:%M:%S')
        except:
            blog_item['push_date'] = datetime.datetime.now()
        blog_item['original'] = response.css('main article >div >div >span::text').extract()[0].strip()
        blog_item['view_times'] = response.css('main article >div ul.right_bar span.txt::text').extract()[0]
        blog_item['comment_num'] = response.meta.get('comment_num')
        blog_item['blog_content'] = "".join(
            list(response.css('#article_content p::text,#article_content img::attr(src)').extract()))
        yield blog_item
