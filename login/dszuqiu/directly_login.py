#!/usr/bin/env python
# encoding = utf-8

import urllib
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from os import remove
import http.cookiejar as cookielib
from PIL import Image
import gzip


class DszuqiuLogin(object):
    url = 'https://www.dszuqiu.com/login'
    headers = {
        # ':authority': 'www.dszuqiu.com',
        # ':method': 'https://www.douban.com/',
        # ':path': '/login',
        # ':scheme': 'https',
        'referer': 'https://www.dszuqiu.com/login',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        'origin': 'https://www.dszuqiu.com',
        'content-type': 'application/x-www-form-urlencoded',
        'accept-encoding': 'gzip, deflate, br'}
    login_form_data = {}
    session = None

    @classmethod
    def load_cookie(cls):
        """
        首先加载cookie
        :return:
        """
        cls.session = requests.session()
        cls.session.cookies = cookielib.LWPCookieJar(filename='cookies')
        try:
            cls.session.cookies.load(ignore_discard=True)
        except BaseException as e:
            print(e)
            cls.login_form_data['zhanghu'] = input(u'请输入账号：')
            cls.login_form_data['password'] = input(u'请输入密码：')

    @classmethod
    def get_captcha(cls):
        """
        获取验证码，当然登录页面也可能没有验证码
        :return:
        """
        captcha = None
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'accept-encoding': 'gzip, deflate, br'}
        response = requests.get(cls.url, headers=headers)
        set_cookie = response.headers['set-cookie']
        cls.ds_session = set_cookie.split(';')[0]
        soup = BeautifulSoup(response.text, "html.parser")
        # 利用bs4获得验证码图片地址
        try:
            img_src = soup.find('img', {'id': 'img_captcha'}).get('src')
            opener = urllib.request.build_opener()
            opener.addheaders = [('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'),
                                 ('accept', 'image/webp,image/apng,image/*,*/*;q=0.8'),
                                 ('accept-encoding', 'gzip, deflate, br'),
                                 ('accept-language', 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7'),
                                 ('cookie', cls.ds_session),
                                 ('referer', 'https://www.dszuqiu.com/login')
                                 ]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve("https://www.dszuqiu.com/"+img_src, 'captcha.gzip')
            # im = Image.open('captcha.jpg')
            # im.show()
            # im.close()
            # print(u'到本地目录打开captcha.jpg获取验证码')
            captcha = input(u'请输入验证码：')
            # remove('captcha.jpg')
        except BaseException as e:
            print(e)
            print("没有验证码～～")
        finally:
            return captcha

    @classmethod
    def login(cls):
        captcha = cls.get_captcha()
        headers = {
            'cookie': 'Hm_lpvt_a68414d98536efc52eeb879f984d8923=1524210605; Hm_lvt_a68414d98536efc52eeb879f984d8923=1524210605; _ga=GA1.2.1774534561.1524210605; _gid=GA1.2.1152834466.1524210605;' + cls.ds_session,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.dszuqiu.com',
            'content-length': '69',
            'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
            'referer': 'https://www.dszuqiu.com/login',
            'accept-encoding': 'gzip, deflate, br',
        }
        cls.login_form_data['rememberMe'] = 'on'
        cls.login_form_data['bsubmit'] = '1'
        if captcha is not None:
            cls.login_form_data['captcha_input'] = captcha
        cls.session.post(cls.url, data=cls.login_form_data, headers=headers)
        # 保存登录cookie
        cls.session.cookies.save()
        # 判断是否登录成功
        if not cls.is_login():
            print("登录失败，请重新尝试～")

    @classmethod
    def is_login(cls):
        """
        通过访问个人账户来判断是否已经登录
        :return:
        """
        url = "https://www.dszuqiu.com/user"
        login_code = cls.session.get(url, headers=cls.headers,
                                     allow_redirects=False).status_code
        if login_code == 200:
            print("登录成功~")
            return True
        else:
            return False

    @classmethod
    def main(cls):
        DszuqiuLogin.load_cookie()
        if not DszuqiuLogin.is_login():
            DszuqiuLogin.login()


if __name__ == '__main__':
    DszuqiuLogin.main()
