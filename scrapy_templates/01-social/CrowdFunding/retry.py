# -*- coding:utf8 -*-

# 爬取众筹网的信息
import requests
import codecs
from bs4 import BeautifulSoup
from bs4 import NavigableString
def read_html(url, file_handler):
    i = 0
    html = None
    while i < 5:
        # try5次
        try:
            html = requests.get(url)
        except IOError:
            print(IOError)
            continue

        if html.status_code == 200:
            break
        i += 1

    soup = BeautifulSoup(html.content, "html.parser")

    # loop all the projects
    for div in soup.select("a.siteCardItemImgA.souSuo"):
        detail_url = div.get("href")  # get the href of detailed url
        project_id = detail_url.strip().split("-")[-1]
        details = read_detail_html(detail_url)

        if not details:
            continue
        file_handler.write(",".join([project_id] + details) + "\n")
    # 下一页
    next_page_a = soup.select(".nextPage")
    if next_page_a:
        next_page_url = next_page_a[0].get("href")
        read_html(next_page_url, file_handler)


# 获取具体信息
def read_detail_html(url):
    i = 0
    detail = None
    # retry 5 times, sometimes the pages just not exist
    while i < 5:
        try:
            detail = requests.get(url)
        except IOError:
            print(IOError)
            continue
        if detail.status_code == 200:
            break
        i += 1

    if not detail:
        return []
    soup = BeautifulSoup(detail.content, "html.parser")
    try:
        result = []
        # first get title
        metas = soup.select("html > head > meta")
        if metas and len(metas) <= 1:
            print(soup.select("html > head"))
            result.append(u"")
        else:
            result.append(metas[1].get("content"))

        # then get supports and fund count
        data_box = soup.select(".xqDetailDataBox")[0]
        for div in data_box.children:
            if isinstance(div, NavigableString):
                continue
            result.append(div.p.span.text)

        # finally get the aim fund value
        aim_box = soup.select("div.xqRatioText.clearfix > span")[1]
        result.append(aim_box.b.text)

        # format the text for web, just remove ¥ and , in numbers
        for i in range(len(result)):
            result[i] = result[i].replace(u"¥", "")
            result[i] = result[i].replace(",", "")
    except IndexError:
        print(detail)  # to see where the fault
        return []

    return result


def dump_data(data):
    with codecs.open("data.csv", encoding="utf-8", mode="w") as f:
        f.write(u"项目id,项目标题,支持数,已筹款,目标筹款\n")
        f.writelines(["".join(d) + "\n" for d in data])


# read_detail_html("http://www.zhongchou.com/deal-show/id-159880")
all_data = []
with codecs.open("data/data.csv", encoding="utf-8", mode="w") as f:
    f.write(u"项目id,项目标题,支持数,已筹款,目标筹款\n")
    read_html("http://www.zhongchou.com/browse/id-23-si_c", f)
