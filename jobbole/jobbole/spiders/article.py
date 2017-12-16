# -*- coding:utf-8 -*-
__author__ = 'neuclil'

import scrapy
from scrapy.http import Request
import re
from urllib import parse
from jobbole.items import JobBoleArticleItem, ArticleItemLoader
from jobbole.utils.common import get_md5
import datetime
from scrapy.loader import ItemLoader

class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页中的文章url并交给解析函数进行具体字段的解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        :param response:
        :return:
        """
        # 1. 获取每个目标页面的url
        post_nodes = response.css('#archive > div.floated-thumb .post-thumb > a')
        for post_node in post_nodes:
            # 获取缩略图
            image_url = post_node.css('img::attr(src)').extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_img_url':image_url}, callback=self.parse_detail)

        # 2. 获取下一页的url
        next_url = response.css('a.next.page-numbers::attr(href)').extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        """
        解析目标页面的内容
        :param response:
        :return:
        """
        # 方式一: 新建一个Item，直接往里面填value(不推荐，可扩展性不强)
        # article_item = JobBoleArticleItem()
        #
        # front_image_url = response.meta.get('front_img_url', '')
        # title = response.css('div.entry-header > h1::text').extract()[0]
        # create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·', '').strip()
        # praise_nums = int(response.css('div.post-adds h10::text').extract()[0])
        # fav_nums = response.css('.bookmark-btn::text').extract()[0]
        # match_re = re.match('.*?(\d+).*', fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        # comment_nums = response.css("a[href='#jobbole-comment'] > span::text").extract()[0]
        # match_re = re.match('.*?(\d+).*', comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        # content = response.css('div.entry').extract()[0]
        # tags = '-'.join([tag for tag in response.css('p.entry-meta-hide-on-mobile a::text').extract() if not tag.endswith(" ")])
        #
        # article_item['url'] = response.url
        # article_item['url_object_id'] = get_md5(response.url)
        # article_item['title'] = title
        # try:
        #     create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()
        # except:
        #     create_date = datetime.datetime.now().date()
        # article_item['create_date'] = create_date
        # article_item['front_image_url'] = [front_image_url]
        # article_item['praise_nums'] = praise_nums
        # article_item['fav_nums'] = fav_nums
        # article_item['comment_nums'] = comment_nums
        # article_item['content'] = content
        # article_item['tags'] = tags

        # 方式二: 通过ItemLoader加载Item，建立processors流水线来处理数据
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('title', 'div.entry-header > h1::text')
        item_loader.add_css('create_date', 'p.entry-meta-hide-on-mobile::text')
        item_loader.add_value('front_image_url', [response.meta.get('front_img_url', '')])
        item_loader.add_css('praise_nums', 'div.post-adds h10::text')
        item_loader.add_css('fav_nums', '.bookmark-btn::text')
        item_loader.add_css('comment_nums', "a[href='#jobbole-comment'] > span::text")
        item_loader.add_css('content', 'div.entry')
        item_loader.add_css('tags', 'p.entry-meta-hide-on-mobile a::text')

        article_item = item_loader.load_item()

        yield article_item
