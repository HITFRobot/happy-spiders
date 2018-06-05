#! -*- coding: utf-8 -*-

'''
    scrapy代理中间件
    ----------------------------------------------------------------------------------------------
    接收从免费代理ip网站爬取的待检测ip, 测试代理IP是否可用，目前只用w3school进行检测，可在设置中拓展测试网站
    ----------------------------------------------------------------------------------------------
'''

import logging.config
import threading
import urllib.request
import requests
from urllib.request import ProxyHandler, build_opener
logger = logging.getLogger('soccer')


class testProxy(threading.Thread):
    def __init__(self, proxyMiddleware, part):
        super(testProxy, self).__init__()
        self.proxyMiddleware = proxyMiddleware
        self.part = part

    def run(self):
        self.test_proxyes(self.part)

    def test_proxyes(self, proxyes):
        '''
        检测代理ip是否可用，可用则修改ip标识为Ture
        :param proxyes: 代理ip
        '''
        for proxy, valid in proxyes.items():
            if self.check_proxy(proxy):
                self.proxyMiddleware.proxyes[proxy] = True
                self.proxyMiddleware.append_proxy(proxy)

    def check_proxy(self, proxy):
        '''检测代理是否可用'''
        logger.info('proxy is %s' % proxy)
        proxies = {
            'http': proxy,
            'https': proxy
        }
        # proxy_handler = ProxyHandler({'http': proxy})
        # # 挂载opener
        # opener = build_opener(proxy_handler, urllib.request.HTTPHandler)
        try:
            for url, code in self.proxyMiddleware.test_urls:
                # rep = opener.open(url, timeout=self.proxyMiddleware.test_proxy_timeout)
                rep = requests.get(url, proxies=proxies)
                if code not in rep.text:
                    logger.info("IP_1:%s不可用" % proxy)
                    return False
                logger.info("IP_2:%s可用" % proxy)
            return True
        except Exception as e:
            logger.info(type(proxy))
            logger.info(e)
            logger.info("IP_3:%s不可用" % proxy)
            return False