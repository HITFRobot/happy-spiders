# encoding = utf-8
import requests
from bs4 import BeautifulSoup
import re
import time


def get_ariticle_info(url):
    s = requests.session()
    s.trust_env = False
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
                'Host': 'mp.weixin.qq.com',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Upgrade-Insecure-Requests': '1',
                'Connection': 'keep-alive',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cookie': 'rewardsn=; wxtokenkey=777'
            }
    flag = True
    while flag:
        try:
            res_content = s.get(url=url, timeout=50, headers=headers).content.decode('utf-8')
            soup = BeautifulSoup(res_content, 'lxml')
            js_content = soup.find(id='js_content')
            img_list = []
            for img in js_content.find_all('img'):
                img_list.append(img.get('data-src'))
            result = re.sub('\s+', '', js_content.get_text())
            return result, ';'.join(img_list)
        except requests.exceptions.ConnectionError:
            print('与目标服务器连接超时，10s后尝试再次请求 ...')
            time.sleep(10)
