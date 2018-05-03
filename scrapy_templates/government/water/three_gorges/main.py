# -*- coding:utf-8 -*-  
__author__ = 'conghuai'
from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "sanxia"])
execute(["scrapy", "crawl", "gezhouba"])
execute(["scrapy", "crawl", "xiangjiaba"])
execute(["scrapy", "crawl", "xiluodu"])