from bs4 import BeautifulSoup


def getSiheyi(html):
    rangqiu_table = {}
    sort_table = {}
    soup = BeautifulSoup(html, "html.parser")
    zhudui_name = soup.select('a.red-color')[0].text.strip()
    kedui_name = soup.select('a.blue-color')[0].text.strip()
    # 得到让球表
    rangqiu_aa = soup.select('#sp_rangfen')
    rangqiu_bb = rangqiu_aa[0].select('tr')
    for tr in rangqiu_bb:
        a = []
        tds = tr.select('td')
        a.append(tds[2].text.strip())
        a.append(tds[3].text.strip())
        a.append(tds[4].text.strip())
        if tds[0].text.strip() != '半' and tds[0].text.strip() != '-':
            rangqiu_table[int(tds[0].text.split("'")[0].strip())] = a
            sort_table[int(tds[0].text.split("'")[0].strip())] = tds[1].text.strip()
    max_key = max(rangqiu_table.keys())
    print(max_key)
    for i in range(1, max_key):
        if i not in rangqiu_table:
            rangqiu_table[i] = rangqiu_table[i - 1]

    for i in range(1, max_key):
        if i not in sort_table:
            sort_table[i] = sort_table[i - 1]
    # rangqiu_lists = sorted(rangqiu_table.items(), key=lambda e: e[0], reverse=True)
    # sort_lists = sorted(sort_table.items(), key=lambda e: e[0], reverse=True)
    # for i in sort_lists:
    #     print(i)

    # 得到大小球表
    daxiaoqiu_table = {}

    daxiaoqiu_aa = soup.select('#sp_daxiao')
    daxiaoqiu_bb = daxiaoqiu_aa[0].select('tr')
    for tr in daxiaoqiu_bb:
        a = []
        tds = tr.select('td')
        a.append(tds[2].text.strip())
        a.append(tds[3].text.strip())
        a.append(tds[4].text.strip())
        if tds[0].text.strip() != '半' and tds[0].text.strip() != '-':
            daxiaoqiu_table[int(tds[0].text.split("'")[0].strip())] = a
    max_key = max(daxiaoqiu_table.keys())
    print(max_key)
    for i in range(1, max_key):
        if i not in daxiaoqiu_table:
            daxiaoqiu_table[i] = daxiaoqiu_table[i - 1]
    # 得到胜平复表
    shengpingfu_table = {}
    shengpingfu_aa = soup.select('#sp_bet')
    shengpingfu_bb = shengpingfu_aa[0].select('tr')
    for tr in shengpingfu_bb:
        a = []
        tds = tr.select('td')
        a.append(tds[2].text.strip())
        a.append(tds[3].text.strip())
        a.append(tds[4].text.strip())
        if tds[0].text.strip() != '半' and tds[0].text.strip() != '-':
            shengpingfu_table[int(tds[0].text.split("'")[0].strip())] = a

    max_key = max(shengpingfu_table.keys())
    print(max_key)
    for i in range(1, max_key):
        if i not in shengpingfu_table:
            shengpingfu_table[i] = shengpingfu_table[i - 1]

    zhudui_jinqiu = {'name': zhudui_name}
    zhudui_qiucha = {'name': zhudui_name}

    kedui_jinqiu = {'name': kedui_name}
    kedui_qiucha = {'name': kedui_name}
    for key, value in sort_table.items():
        zhudui_jinqiu[key] = value.split(':')[0].strip()
        kedui_jinqiu[key] = value.split(':')[1].strip()
        zhudui_qiucha[key] = int(zhudui_jinqiu[key]) - int(kedui_jinqiu[key])
        kedui_qiucha[key] = int(kedui_jinqiu[key]) - int(zhudui_jinqiu[key])

    print(zhudui_jinqiu)
    print(kedui_jinqiu)
    print(zhudui_qiucha)
    print(kedui_qiucha)


if __name__ == '__main__':
    with open('/home/zxy/PycharmProjects/untitled/soccerprocess/init.txt', 'r') as f:
        html_data = f.read()
    getSiheyi(html_data)
