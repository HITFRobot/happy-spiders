# -*- coding:utf-8 -*-  
__author__ = 'neuclil'

from scrapy.cmdline import execute

import sys
import os
import urllib
a = urllib.parse.unquote("%u8F93%u5165%u7684%u6570%u5B57%u8FC7%u5927%uFF01")
print(a)
#
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "redstarspider"])