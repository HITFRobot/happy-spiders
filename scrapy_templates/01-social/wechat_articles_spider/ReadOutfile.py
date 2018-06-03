# encoding = utf-8

import os
import re

from mitmproxy import io
from mitmproxy.exceptions import FlowReadException


class Reader:
    """
    命令行运行mitmproxy, 并筛选cookie和appmsg_token,
    command: python get_params outfile
    """

    def __init__(self):
        """
        :Returns None
        """
        pass

    def control(self, outfile):
        """
        执行终端命令保存http请求，并筛选appmsg_token和cookie
        :param outfile:
        :return:
        (str, str)
            appmsg_token, cookie: 需要的参数
        """

        path = os.path.split(os.path.realpath(__file__))[0]
        command = 'mitmdump ' \
                  '-s {}/tools.py'.format(path)
        os.system(command=command)

if __name__ == '__main__':
    Reader().control('request.txt')
