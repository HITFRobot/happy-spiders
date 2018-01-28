# -*- coding:utf-8 -*-

'''
Required
- requests (必须)
Info
- author : "wuxin"
- email  : "opdss@qq.com"
- date   : "2016.4.18"
    拉勾网登录, 密码采用了md5双重加密
'''

import requests
import http.cookiejar as cookielib

from utils.code_verification import code_verificate
import re
import os
import time
import json
import requests
import hashlib
from bs4 import BeautifulSoup

YUMDAMA_USERNAME='neuclil'
YUMDAMA_PASSWORD='mJzUuKpy6TLfosmRvqgQJAxn'
CaptchaImagePath = QRImgPath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'captcha.jpg'

# 请求对象
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookie未能加载')

# 请求头信息
HEADERS = {
    'Referer': 'https://passport.lagou.com/login/login.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
    'X-Requested-With': 'XMLHttpRequest'
}


# 密码加密
def encryptPwd(passwd):
    # 对密码进行了md5双重加密
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    # veennike 这个值是在js文件找到的一个写死的值
    passwd = 'veenike'+passwd+'veenike'
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    return passwd


# 获取请求token
def getTokenCode():
    login_page = 'https://passport.lagou.com/login/login.html'

    data = session.get(login_page, headers=HEADERS)

    soup = BeautifulSoup(data.content, "html5lib")
    '''
        页面新添加了下面这个东东, 所以要从登录页面提取token，code， 在头信息里面添加
        <!-- 页面样式 --><!-- 动态token，防御伪造请求，重复提交 -->
        <script type="text/javascript">
            window.X_Anti_Forge_Token = 'dde4db4a-888e-47ca-8277-0c6da6a8fc19';
            window.X_Anti_Forge_Code = '61142241';
        </script>
    '''
    anti_token = {'X-Anit-Forge-Token' : 'None', 'X-Anit-Forge-Code' : '0'}

    anti_token_str = soup.findAll('script')[1].getText().splitlines()
    anti_token['X-Anit-Forge-Token'] = anti_token_str[1].split('=')[1].strip(' ;\'')
    anti_token['X-Anit-Forge-Code'] = anti_token_str[2].split('=')[1].strip(' ;\'')
    return anti_token


# 人工读取验证码并返回
def getCaptcha():
    captchaImgUrl = 'https://passport.lagou.com/vcode/create?from=register&refresh=%s' % time.time()
    # 写入验证码图片
    f = open(CaptchaImagePath, 'wb')
    f.write(session.get(captchaImgUrl, headers=HEADERS).content)
    f.close()
    verify_code, yundama_obj, cid = code_verificate(YUMDAMA_USERNAME, YUMDAMA_PASSWORD, CaptchaImagePath)
    return verify_code


# 登陆操作
def login(user, passwd, captchaData=None, token_code=None):
    postData = {
        'isValidate' : 'true',
        'password' : passwd,
        # 如需验证码,则添加上验证码
        'request_form_verifyCode' : (captchaData if captchaData!=None else ''),
        'submit' : '',
        'username' : user
    }
    login_url = 'https://passport.lagou.com/login/login.json'

    # 头信息添加tokena
    login_headers = HEADERS.copy()
    token_code = getTokenCode() if token_code is None else token_code
    login_headers.update(token_code)

    # data = {"content":{"rows":[]},"message":"该帐号不存在或密码错误，请重新输入","state":400}
    response = session.post(login_url, data=postData, headers=login_headers)
    session.cookies.save()
    data = json.loads(response.content.decode('utf-8'))

    if data['state'] == 1:
        return response.content
    elif data['state'] == 10010:
        print(data['message'])
        captchaData = getCaptcha()
        token_code = {'X-Anit-Forge-Code' : data['submitCode'], 'X-Anit-Forge-Token' : data['submitToken']}
        return login(user, passwd, captchaData, token_code)
    else:
        print(data['message'])
        return False


def get_index():
    header = {
        'Host': 'www.lagou.com',
        'Connection': 'keep-alive',
        'Cache-Control' : 'max-age=0',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Upgrade-Insecure-Requests' : '1',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language' : 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
    }
    response = session.get('https://www.lagou.com', headers=header)
    with open('index.html', 'wb') as f:
        f.write(response.text.encode('utf-8'))
    print('ok')


def is_login():
    headers = {
        'Host': 'www.lagou.com',
        'Connection': 'keep-alive',
        'Cache-Control' : 'max-age=0',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Upgrade-Insecure-Requests' : '1',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language' : 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
    }
    zhaopin_url = 'https://www.lagou.com/zhaopin/Java/?labelWords=label'
    response = session.get(zhaopin_url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True

if __name__ == "__main__":

    # username = input("请输入你的手机号或者邮箱\n >>>:")
    # username = "13612819078"
    # passwd = input("请输入你的密码\n >>>:")
    # passwd = "qq13143344"

    # passwd = encryptPwd(passwd)
    #
    # data = login(username, passwd)
    # if data:
    #     print(data)
    #     print('登录成功')
    # else:
    #     print('登录不成功')
    print(is_login())


