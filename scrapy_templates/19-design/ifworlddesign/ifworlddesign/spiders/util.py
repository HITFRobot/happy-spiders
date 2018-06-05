# encoding = utf-8
from bs4 import BeautifulSoup
import re
import json


def parse_json_str(text):
    html_doc = BeautifulSoup(text, 'lxml')
    json_html = html_doc.find('script', attrs={'type': 'application/json'})
    dealed_json = re.sub(r'<script data-type="bootstrap-data" type="application/json">', '', str(json_html))
    dealed_json = re.sub(r'</script>', '', dealed_json)
    # 去除字符串中自带的引号   \\"
    dealed_json = re.sub(r'\\"', '', dealed_json)
    dealed_json = re.sub(r'\\', '', dealed_json)
    json_obj = json.loads(dealed_json, encoding='utf-8')
    return json_obj
