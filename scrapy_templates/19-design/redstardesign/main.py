# -*- coding:utf-8 -*-  
__author__ = 'neuclil'

from scrapy.cmdline import execute
from urllib.parse import unquote
import sys
import os
import urllib
from bs4 import BeautifulSoup


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "redstarspider"])
