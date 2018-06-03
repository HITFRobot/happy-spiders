# encoding = utf-8

from bs4 import BeautifulSoup

with open('result.txt') as fp:
    res_content = fp.read()
soup = BeautifulSoup(res_content, 'lxml')
js_content = soup.find(id='js_content')
for img in js_content.find_all('img'):
    print(img.get('data-src'))
# result = re.sub('\s+', '', soup.find(id='js_content').get_text())