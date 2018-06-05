# encoding = utf-8

import hashlib
import os
import re
import requests
from requests.cookies import cookielib
import time


class ArticlesUrls(object):

    """
    获取公众号的链接
    """

    def __init__(self, username=None, password=None, cookie=None, token=None):

        self.s = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
        }

        self.params = {
            'lang': 'zh_CN',
            'f': 'json'
        }

        # 手动输入cookie 和　token　登录
        if cookie is not None and token is not None:
            self.__versify_str(cookie, 'cookies')
            self.__versify_str(token, 'token')
            self.headers['Cookie'] = cookie
            self.params['token'] = token
        elif username is not None and password is not None:
            self.__versify_str(username, 'username')
            self.__versify_str(password, 'password')
            # 加载cookie与token并判断是否有效
            if self.__versify_cookie_token(username=username):
                print('使用存储的cookie和token登录成功～～')
            else:
                self.__startlogin(username, password)
        else:
            print('please check your params')
            raise SyntaxError

    def __versify_cookie_token(self, username):
        """
        加载cookie与token并判断是否有效
        :return:
        """
        if self.__read_cookie(username=username) and self.__read_token(username):
            profile_url = 'https://mp.weixin.qq.com/cgi-bin/home'
            self.params['t'] = 'home/index'
            if self.s.get(url=profile_url, headers=self.headers, params=self.params).status_code == 200:
                return True
            else:
                self.params.pop('t')
                self.params.pop('token')
                self.s.cookies = None
                return False
        else:
            return False

    def __versify_str(self, input_string, param_name):
        """
        check whether is string
        :param input_string:
        :param param_name:
        :return:
        """
        if not isinstance(input_string, str):
            raise TypeError('{} is not str'.format(param_name))

    def __md5_password(self, password):
        """将密码进行md5加密"""
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        pwd = md5.hexdigest()
        return pwd

    def __save_cookie(self, username):
        """
        save cookies
        :param username:
        :return:
        """
        new_cookie_jar = cookielib.LWPCookieJar()

        # 将转化成字典格式的cookie保存到LWPcookiejar中
        requests.utils.cookiejar_from_dict(
            {c.name: c.value
                for c in self.s.cookies}, new_cookie_jar
        )

        new_cookie_jar.save(os.path.join(os.path.dirname(__file__), 'cookies/' + username + '.txt'),
                            ignore_discard=True, ignore_expires=True)

    def __read_cookie(self, username):
        """
        读取cookie
        :param username:
        :return:
        """
        load_cookiejar = cookielib.LWPCookieJar()
        try:
            load_cookiejar.load(
                os.path.join(os.path.dirname(__file__), 'cookies/' + username + '.txt'),
                ignore_discard=True
            )
            load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
            self.s.cookies = requests.utils.cookiejar_from_dict(load_cookies)
            return True
        except Exception as e:
            return False

    def __save_token(self, username):
        """
        save token
        :param username:
        :return:
        """
        with open(os.path.join(os.path.dirname(__file__), 'tokens/' + username + '.txt'), 'w') as fp:
            fp.write(self.params['token'])

    def __read_token(self, username):

        try:
            with open(os.path.join(os.path.dirname(__file__), 'tokens/' + username + '.txt'), 'r') as fp:
                self.params['token'] = re.sub('\s', '', fp.read())
                return True
        except Exception:
            return False

    def __save_login_qrcode(self, img):
        """
        存储和显示登录二维码
        :param img:
        :return:
        """
        import matplotlib.pyplot as plt
        from PIL import Image
        with open('login.jpg', 'wb+') as fp:
            fp.write(img.content)

        # 显示二维码
        try:
            img = Image.open('login.jpg')
        except Exception:
            raise TypeError(u'账号密码输入错误，请重新输入')
        plt.figure()
        plt.imshow(img)
        plt.show()

    def __startlogin(self, username, password):
        """
        begin login
        :param username:
        :param password:
        :return:
        """
        pwd = self.__md5_password(password)
        data = {
            'username': username,
            'userlang': 'zh_CN',
            'token': '',
            'pwd': pwd,
            'lang': 'zh_CN',
            'imgcode': '',
            'f': 'json',
            'ajax': '1'
        }

        self.headers['Host'] = 'mp.weixin.qq.com'
        self.headers['Origin'] = 'https://mp.weixin.qq.com'
        self.headers['Referer'] = 'https://mp.weixin.qq.com/'

        bizlogin_url = 'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin'
        qrcode_url = "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300&rd=928"

        # 获取二维码，等待用户扫描二维码
        self.s.post(url=bizlogin_url, headers=self.headers, data=data)
        img = self.s.get(qrcode_url)
        self.__save_login_qrcode(img)

        # 获取token
        self.__login(username, password)

    def __login(self, username, password):
        """
        login
        :param username:
        :param password:
        :return:
        """
        referer = 'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=validate&lang=zh_CN&account={}'.format(
            username)
        self.headers['Referer'] = referer

        data = {
            'userlang': 'zh_CN',
            'token': '',
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1'
        }

        # 获取token的url
        bizlogin_url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login"
        response = self.s.post(url=bizlogin_url, headers=self.headers, data=data).ｉjson()

        try:
            # 获取返回参数中的token参数
            token = response['redirect_url'].split('=')[-1]
            self.params['token'] = token
            # 持久化cookie与token
            self.__save_cookie(username)
            self.__save_token(username)
            print('登录成功～～')

            self.headers.pop('Host')
            self.headers.pop('Origin')
        except Exception:
            print('please try again')
            self.__startlogin(username, password)

    def articles_nums(self, official_info):
        """
        获取公众号的总共发布的文章数量
        :param nickname:
        :return:
        """
        try:
            return self.__get_articles_data(official_info, begin='0')['app_msg_cnt']
        except Exception:
            raise Exception(u'公众号名称错误或cookie、token错误，请重新输入')

    def articles(self, official_info, begin=0, count=5):
        """
        获取公众号每一页所对应的文章信息
        :param official_info:
        :param begin:
        :param count:
        :return:
        list:
            由每个文章信息所构成的list
            [
                {
                    'aid': 文章的唯一id,
                    'appmsgid': 每一天发布的文章对应一个唯一的id,
                    'cover': 文章封面链接,
                    'itemidx': 1,
                    'link': 文章的url,
                    'title': 文章标题,
                    'update_time': 文章更新时间戳
        """
        try:
            return self.__get_articles_data(official_info, begin=str(begin), count=str(count))['app_msg_list']
        except Exception:
            raise Exception(u'公众号名称错误或者cookie、token错误，请重新输入')

    def query_articles_nums(self, nickname, query):
        """
        获取公众号指定了关键字的文章的数目
        :param nickname:
        :param query:
        :return:
        """
        self.__versify_str(nickname, 'nickname')
        self.__versify_str(query, 'nickname')
        try:
            return self.__get_articles_data(nickname, begin='0', query=query)['app_msg_cnt']
        except Exception:
            raise Exception(u'公众号名名称错误或cookie、token错误，请重新输入')

    def query_articles(self, nickname, query, begin, count=5):
        """
        获取公众号指定了关键词的文章信息
        :param nickname:
        :param query:
        :param begin:
        :param count:
        :return:
        返回数据格式和articles()返回类型相同
        """
        self.__versify_str(query, 'query')
        self.__versify_str(nickname, 'nickname')
        try:
            return self.__get_articles_data(nickname, begin=str(begin), count=str(count), query=query)['app_msg_list']
        except Exception:
            raise Exception(u'公众号名称错误或cookie、token错误，请重新输入')

    def official_info(self, nickname, begin=0, count=5):
        """
        获取公众号的一些信息
        :param nickname:
        :param begin:
        :param count:
        :return:
        json:
            公众号的一些信息
            {
                'alias': 公众号别名,
                'fakeid': 公众号唯一id,
                'nickname': 公众号名称,
                'round_head_img': 公众号头像的url,
                'service_type': 公众号类型
        """
        self.__versify_str(nickname, 'nickname')
        # 搜索公众号的url
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz'

        # 设置请求参数
        params = {
            'action': 'search_biz',
            'ajax': '1',
            'query': nickname,
            'begin': str(begin),
            'count': str(count)
        }
        self.params.update(params)
        flag = True
        while flag:
            try:
                # 返回与输入公众号名称最接近的公众号信息
                official = self.s.get(url=search_url, headers=self.headers, params=self.params).ｉjson()
                if official['err_msg'] == 'freq contorl':
                    print('操作太频繁，请稍后再试，等10分钟')
                    time.sleep(600)
                else:
                    return official['list'][0]
            except Exception:
                raise Exception(u'公众号名称错误或cookie、token错误，请重新输入')

    def __get_articles_data(self, official_info, begin, count='5', type_='9', action='list_ex', query=None):
        """
        获取公众号文章的一些信息
        :param nickname:
        :param begin:
        :param count:
        :param type_:
        :param action:
        :param query:
        :return:
        json:
            文章信息的json
            {
                'app_msg_cnt': 公众号发文章总数，
                'app_msg_list': 当前页文章信息
                'base_resp': {
                    'err_msg': 'ok',
                    'ret': 0
                }
            }
        """
        # 获取文章信息的url
        appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'

        try:
            # 获取公众号的fakeid
            self.params['fakeid'] = official_info['fakeid']
        except Exception:
            raise Exception(u'公众号名称错误或cookie、token错误，请重新输入')

        # 更新请求参数
        params = {
            'query': str(query) if query is not None else '',
            'begin': str(begin),
            'count': str(count),
            'type': str(type_),
            'action': 'list_ex'
        }
        self.params.update(params)

        data = self.s.get(url=appmsg_url, headers=self.headers, params=self.params).ｉjson()
        return data

if __name__ == '__main__':
    articlesUrls = ArticlesUrls(username='sun1252058937@163.com', password='hong1252058937')
    # 获取公众号的fakeId
    official_info = articlesUrls.official_info('杨毅侃球')
    articlesUrls.articles_nums(official_info)
