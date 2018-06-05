# -*- coding:utf-8 -*-  
__author__ = 'neuclil'

import hashlib
from datetime import date, datetime


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def comparetime(nowtime, stringtime):
    "比较两个时间,并返回两个日期之间相差的天数"
    if isinstance(nowtime, date):
        pass
    else:
        nowtime = convertstringtodate(nowtime)
    if isinstance(stringtime, date):
        pass
    else:
        stringtime = convertstringtodate(stringtime)

    result = nowtime - stringtime
    return result.days