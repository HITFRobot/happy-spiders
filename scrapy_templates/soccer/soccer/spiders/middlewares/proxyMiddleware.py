#! -*- coding: utf-8 -*-
'''
    scrapy代理中间件
    ----------------------------------------------------------------------------------------------
    作为爬虫下载器的一部分，代理中间件实现在请求前更换代理。
    从国内的免费代理ip供给网站爬取ip进行校检，动态维护，为下载器提供可用ip
    ----------------------------------------------------------------------------------------------
'''
import math
import re
import logging.config
from .getProxy import getProxy
from .testProxy import testProxy
from twisted.internet import defer
from twisted.internet.error import TimeoutError, ConnectionRefusedError, \
    ConnectError, ConnectionLost, TCPTimedOutError, ConnectionDone
logger = logging.getLogger('ahu')


class proxyMiddleware(object):

    EXCEPTIONS_TO_CHANGE = (defer.TimeoutError, TimeoutError, ConnectionRefusedError, ConnectError, ConnectionLost, TCPTimedOutError, ConnectionDone)
    _settings = [
        ('enable', True),
        ('allow_spider', ['MOHRSSjob']),
        ('test_urls', [('http://www.w3school.com.cn', '06004630'), ]),
        ('test_proxy_timeout', 5),
        ('download_timeout', 60),
        ('test_threadnums', 20),
        ('ban_code', [503, ]),
        ('ban_re', r''),
        ('proxy_least', 5),
        ('init_valid_proxys', 2),
        ('invalid_limit', 200),
    ]

    def __init__(self, proxy_set=None):

        self.proxy_set = proxy_set or {}
        for k, v in self._settings:
            setattr(self, k, self.proxy_set.get(k, v))

        # 代理列表和当前的代理指针，couter_proxy用作该代理下载的网页数量
        self.proxy = []
        self.proxy_index = 0
        self.proxyes = {}
        self.counter_proxy = {}
        self.fecth_new_proxy()
        self.test_proxyes(self.proxyes, wait=True)
        logger.info('使用代理 : %s', self.proxy)

    def process_request(self, request, spider):
        '''
        请求前通过该方法
        :param request: 单次请求
        :param spider: 爬虫对象
        '''
        if spider.name not in self.allow_spider:
            logger.info("爬虫%s设置不使用代理" % spider.name)
            return
        if not self._is_enabled_for_request(request, spider):
            logger.debug('不使用代理，直连')
            return

        if self.len_valid_proxy() > 0:
            self.set_proxy(request)
            # if 'download_timeout' not in request.meta:
            request.meta['download_timeout'] = self.download_timeout
        else:
            # 没有可用代理，直连
            if 'proxy' in request.meta:
                del request.meta['proxy']

    def process_respose(self, request, response, spider):
        '''
        请求返回对象
        :param request: 单次请求
        :param response: 请求响应
        :param spider: 爬虫对象
        :return: 请求成功返回请求对象，失败则重试
        '''
        if spider.name not in self.allow_spider:
            return response
        if not self._is_enabled_for_request(request,spider):
            return response

        if response.status in self.ban_code:
            self.invaild_proxy(request.meta['proxy'])
            logger.debug("代理[%s]被扳,返回状态码:[%s]. ", request.meta['proxy'], str(response.status))
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request

        if self.ban_re:
            try:
                pattern = re.compile(self.ban_re)
            except TypeError:
                return response
            match = re.search(pattern, response.body)
            if match:
                self.invaild_proxy(request.meta['proxy'])
                logger.debug("代理[%s]被扳,由于:[%s]. ", request.meta['proxy'], str(match))
                new_request = request.copy()
                new_request.dont_filter = True
                return new_request

        p = request.meta['proxy']
        self.counter_proxy[p] = self.counter_proxy.setdefault(p, 1) + 1
        return response

    def process_exception(self, request, exception, spider):
        '''
        异常处理函数，处理请求异常，
        :param request: 单次请求
        :param exception: 请求异常
        :param spider: 爬虫对象
        :return: 重试
        '''
        if isinstance(exception, self.EXCEPTIONS_TO_CHANGE) \
                and request.meta.get('proxy', False):
            self.invaild_proxy(request.meta['proxy'])
            logger.debug("代理[%s] 连接异常[%s].", request.meta['proxy'], exception)
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request

    def invaild_proxy(self, proxy):
        """
        将代理设为不可用。如果之前该代理已下载超过200页（默认）的资源，则暂时不设置，仅切换代理，并减少其计数。
        """
        if self.counter_proxy.get(proxy, 0) > self.invalid_limit:
            self.counter_proxy[proxy] = self.counter_proxy.get(proxy, 0) - 50
            if self.counter_proxy[proxy] < 0:
                self.counter_proxy[proxy] = 0
            self.change_proxy()
        else:
            self.proxyes[proxy] = False

    def set_proxy(self, request):
        """
        设置代理。
        """
        proxy_valid = self.proxyes[self.proxy[self.proxy_index]]
        if not proxy_valid:
            self.change_proxy()
        request.meta['proxy'] = self.proxy[self.proxy_index]
        logger.debug('已设置代理request.meta: %s', request.meta)

    def change_proxy(self):
        """
        切换代理。
        """
        while True:
            # 从代理储备列表中检索一个可用代理
            self.proxy_index = (self.proxy_index + 1) % len(self.proxy)
            proxy_valid = self.proxyes[self.proxy[self.proxy_index]]
            if proxy_valid:
                break
            if self.len_valid_proxy() == 0:
                logger.info('已无可用代理，等待爬取')
                break
        logger.info('已切换代理到 %s', self.proxy[self.proxy_index])
        logger.info('可用代理[%s]: %s', self.len_valid_proxy(), self.valid_proxyes())

        # 可用代理数量小于预设值则扩展代理
        if self.len_valid_proxy() < self.proxy_least:
            self.extend_proxy()

    def len_valid_proxy(self):
        """
        计算可用代理的数量
        """
        count = 0
        for p in self.proxy:
            if self.proxyes[p]:
                count += 1
        return count

    def valid_proxyes(self):
        """
        返回可用代理列表
        """
        proxyes = []
        for p in self.proxy:
            if self.proxyes[p]:
                proxyes.append(p)
        return proxyes

    def extend_proxy(self):
        """
        代理池为空或单次请求失败
            扩展代理"""
        self.fecth_new_proxy()
        self.test_proxyes(self.proxyes)

    def append_proxy(self, p):
        """
        将测试通过的代理添加到列表
        """
        if p not in self.proxy:
            self.proxy.append(p)

    def fecth_new_proxy(self):
        """
        获取新的代理，目前从两个网站抓取代理，每个网站开一个线程抓取代理，后续增加
        """
        logger.debug('开始爬取代理')
        urls = ['xici', 'ip3336']
        threads = []
        for url in urls:
            t = getProxy(self.proxyes, url)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    def test_proxyes(self, proxyes, wait=False):
        """
        测试代理是否可用
        """
        list_proxy = proxyes.items()
        threads = []
        n = int(math.ceil(len(list_proxy) / self.test_threadnums))
        for i in range(self.test_threadnums):
            # 将待测试的代理平均分给测试线程
            list_part = list_proxy[i * n: (i + 1) * n]
            part = {k: v for k, v in list_part}
            t = testProxy(self, part)
            threads.append(t)
            t.start()

        # 初始化该中间件时，等待有可用的代理
        if wait:
            while True:
                for t in threads:
                    t.join(0.2)
                    if self._has_valid_proxy():
                        break
                if self._has_valid_proxy():
                        break

    def _has_valid_proxy(self):
        '''
        检查可用代理数据是否足够
        '''
        if self.len_valid_proxy() >= self.init_valid_proxys:
            return True

    def _is_enabled_for_request(self, request, spider):
        '''
        查看是否开启代理
        '''
        return self.enable and 'dont_proxy' not in request.meta