# encoding = utf-8

import time
import urllib.parse
import json


class Tools(object):

    def __init__(self):
        pass


def response(flow):
    """
    mitmdumps 调用的脚本函数
    如果请求包含需要的flow，就保存，然后终止运行
    :param flow:
        http.HTTPFlow
        请求流，通过命令调用
    :return:
    """

    from mitmproxy import http

    with open('request.txt', 'w', encoding='utf-8') as fp:
        url = urllib.parse.unquote(flow.request.url)
        if 'taobao.com' in url:
            fp.write(url + '   '+str(flow.response.headers))
            exit()
