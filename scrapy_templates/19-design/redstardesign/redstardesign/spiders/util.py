# encoding = utf-8

from urllib.parse import unquote

def unicode_trans(text):
    b = unquote(text).replace('%u', '\\u')
    string = b.encode('utf-8').decode('unicode_escape')
    return string


