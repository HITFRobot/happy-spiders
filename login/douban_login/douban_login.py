#!/usr/bin/env python
# encoding = utf-8

from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from os import remove
import http.cookiejar as cookielib
from PIL import Image


class DoubanLogin(object):
    url = 'https://accounts.douban.com/login'
    login_form_data = {'remember': 'on', 'login': u'登录'}
    headers = {'Host': 'accounts.douban.com',
               'Referer': 'https://www.douban.com/',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding': 'gzip, deflate, br'}
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
            cls.login_form_data['form_email'] = input(u'请输入账号：')
            cls.login_form_data['form_password'] = input(u'请输入密码：')

    @classmethod
    def is_login(cls):
        """
        通过访问个人账户来判断是否已经登录
        :return:
        """
        url = "https://www.douban.com/accounts/"
        login_code = cls.session.get(url, headers=cls.headers,
                                     allow_redirects=False).status_code
        if login_code == 200:
            print("登录成功~")
            return True
        else:
            return False

    @classmethod
    def get_captcha(cls):
        """
        获取验证码，当然登录页面也可能没有验证码
        :return:
        """
        captcha = None
        captcha_id = None
        r = requests.get(cls.url, headers=cls.headers)
        soup = BeautifulSoup(r.text, "html.parser")
        # 利用bs4获得验证码图片地址
        try:
            img_src = soup.find('img', {'id': 'captcha_image'}).get('src')
            urlretrieve(img_src, 'captcha.jpg')
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
            print(u'到本地目录打开captcha.jpg获取验证码')
            captcha = input(u'请输入验证码：')
            remove('captcha.jpg')
            captcha_id = soup.find(
                'input', {'type': 'hidden', 'name': 'captcha-id'}).get('value')
        except BaseException as e:
            print(e)
            print("没有验证码～～")
        finally:
            return captcha, captcha_id

    @classmethod
    def login(cls):
        captcha, captcha_id = cls.get_captcha()
        # 增加表数据
        if captcha is not None:
            cls.login_form_data['captcha-solution'] = captcha
            cls.login_form_data['captcha-id'] = captcha_id
        cls.session.post(cls.url, data=cls.login_form_data, headers=cls.headers)
        # 保存登录cookie
        cls.session.cookies.save()
        # 判断是否登录成功
        if not cls.is_login():
            print("登录失败，请重新尝试～")

    @classmethod
    def main(cls):
        # 加载cookie
        DoubanLogin.load_cookie()
        # 判断是否登录
        if not DoubanLogin.is_login():
            DoubanLogin.login()

if __name__ == '__main__':
    DoubanLogin.main()
