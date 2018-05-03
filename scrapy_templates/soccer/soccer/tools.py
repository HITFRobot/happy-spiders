# encoding = utf-8

import re
import json
import os
import xlsxwriter
from bs4 import BeautifulSoup


def extract_data(text, repl, final_time=None):
    """

    :param text: 需要正则提取的文本
    :param pattern: 通过该字段判断提取哪个表格数据
    :param final_time: 全场结束时间
    :return:
    """
    if repl == 'jingong':
        aa = re.findall(r'(shepian_chart_options.series[^;]+;)', text)[2]
    elif repl == 'weixian':
        aa = re.findall(r'(shepian_chart_options.series[^;]+;)', text)[1]
    elif repl == 'shepian':
        aa = re.findall(r'(shepian_chart_options.series[^;]+;)', text)[0]
    elif repl == 'shezheng':
        aa = re.findall(r'(shezheng_chart_options.series[^;]+;)', text)[0]
    bb = re.sub('\s', '', re.search(r'\[[^;]+;', aa).group()[0:-1])[1:-1]
    cc = re.search(r'(^\{.+\}\}),(.+})', bb)
    home = cc.group(1)
    visit = cc.group(2)

    def _change(mathed):
        return mathed.group()[0] + '$' + mathed.group()[-1]

    home = re.sub(r"([a-zA-Z]'[a-zA-Z])", _change, home)
    home = re.sub(r"'", '"', home)
    home = re.sub(r'\$', "'", home)

    visit = re.sub(r"([a-zA-Z]'[a-zA-Z])", _change, visit)
    visit = re.sub(r"'", '"', visit)
    visit = re.sub(r'\$', "'", visit)

    try:
        home_data = json.loads(home)
    except json.decoder.JSONDecodeError:
        with open('error_home.txt', mode='w', encoding='utf-8') as fp:
            fp.write(home)
        print('home' + home)
    try:
        visit_data = json.loads(visit)
    except json.decoder.JSONDecodeError:
        with open('error_visit.txt', mode='w', encoding='utf-8') as fp:
            fp.write(home)
        print('visit' + visit)

    """
    进攻数据
    1: 首先获得最终结束时间
    """
    if final_time is None:
        final_time = max(home_data['data'][-1]['x'], visit_data['data'][-1]['x'])

    """
        :return格式 [{name: '', 0: , 1: } {'name': '', 0: , 1: }]
    """
    return_data = []

    dict_data = dict()
    dict_data['name'] = home_data['name']
    dict_data[0] = 0
    for item in home_data['data']:
        if item['x'] not in dict_data:
            dict_data[item['x']] = item['y']
    # 判断是否有中断数据
    for i in range(final_time + 1):
        if i not in dict_data:
            dict_data[i] = dict_data[i - 1]
    return_data.append(dict_data)

    dict_data = dict()
    dict_data[0] = 0
    dict_data['name'] = visit_data['name']
    for item in visit_data['data']:
        if item['x'] not in dict_data:
            dict_data[item['x']] = item['y']
    # 判断是否有中断数据
    for i in range(final_time + 1):
        if i not in dict_data:
            dict_data[i] = dict_data[i - 1]
    return_data.append(dict_data)

    return return_data, final_time


def main_extract(text):
    """

    :param text: 需要正则提取的文本
    :return: [ [{name..}, {name...}],  [...] ...]
     按照 进攻 危险 射偏 射正 顺序
    """
    repl_list = ['jingong', 'weixian', 'shepian', 'shezheng']
    return_data = dict()
    final_time = None
    for repl in repl_list:
        data, final_time = extract_data(text, repl, final_time)
        return_data[repl] = data
    """
    然后计算 射正差 射正率 危险比 进攻比
    """
    shezhengcha = []
    home_dict_data = {'name': return_data['shezheng'][0]['name']}
    visit_dict_data = {'name': return_data['shezheng'][1]['name']}
    for i in range(final_time + 1):
        home_dict_data[i] = return_data['shezheng'][0][i] - return_data['shezheng'][1][i]
        visit_dict_data[i] = return_data['shezheng'][1][i] - return_data['shezheng'][0][i]
    shezhengcha.append(home_dict_data)
    shezhengcha.append(visit_dict_data)
    return_data['shezhengcha'] = shezhengcha

    shezhenglv = []
    home_dict_data = {'name': return_data['shezheng'][0]['name']}
    visit_dict_data = {'name': return_data['shezheng'][1]['name']}
    for i in range(final_time + 1):
        if (return_data['shezheng'][0][i] + return_data['shepian'][0][i]) == 0:
            home_dict_data[i] = 'div/0'
        else:
            home_dict_data[i] = round(
                return_data['shezheng'][0][i] / (return_data['shezheng'][0][i] + return_data['shepian'][0][i]), 2)
        if (return_data['shezheng'][1][i] + return_data['shepian'][1][i]) == 0:
            visit_dict_data[i] = 'div/0'
        else:
            visit_dict_data[i] = round(
                return_data['shezheng'][1][i] / (return_data['shezheng'][1][i] + return_data['shepian'][1][i]), 2)
    shezhenglv.append(home_dict_data)
    shezhenglv.append(visit_dict_data)
    return_data['shezhenglv'] = shezhenglv

    weixianbi = []
    home_dict_data = {'name': return_data['shezheng'][0]['name']}
    visit_dict_data = {'name': return_data['shezheng'][1]['name']}
    for i in range(final_time + 1):
        if return_data['weixian'][1][i] == 0:
            home_dict_data[i] = 'div/0'
        else:
            home_dict_data[i] = round(return_data['weixian'][0][i] / return_data['weixian'][1][i], 2)
        if return_data['weixian'][0][i] == 0:
            visit_dict_data[i] = 'div/0'
        else:
            visit_dict_data[i] = round(return_data['weixian'][1][i] / return_data['weixian'][0][i], 2)
    weixianbi.append(home_dict_data)
    weixianbi.append(visit_dict_data)
    return_data['weixianbi'] = weixianbi

    jingongbi = []
    home_dict_data = {'name': return_data['shezheng'][0]['name']}
    visit_dict_data = {'name': return_data['shezheng'][1]['name']}
    for i in range(final_time + 1):
        if return_data['jingong'][1][i] == 0:
            home_dict_data[i] = 'div/0'
        else:
            home_dict_data[i] = round(return_data['jingong'][0][i] / return_data['jingong'][1][i], 2)
        if return_data['jingong'][0][i] == 0:
            visit_dict_data[i] = 'div/0'
        else:
            visit_dict_data[i] = round(return_data['jingong'][1][i] / return_data['jingong'][0][i], 2)
    jingongbi.append(home_dict_data)
    jingongbi.append(visit_dict_data)
    return_data['jingongbi'] = jingongbi

    return return_data, final_time


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

    rangqiu_table[0]=0
    sort_table[0] = 0
    max_key = max(rangqiu_table.keys())
    rangqiu_table[0] = ['0', '0', '0']
    sort_table[0] = '0:0'
    for i in range(1, max_key):
        if i not in rangqiu_table:
            rangqiu_table[i] = rangqiu_table[i - 1]

    for i in range(1, max_key):
        if i not in sort_table:
            sort_table[i] = sort_table[i - 1]

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

    daxiaoqiu_table[0] = ['0', '0', '0']
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
    shengpingfu_table[0] = ['0', '0', '0']
    max_key = max(shengpingfu_table.keys())
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

    return [zhudui_jinqiu, kedui_jinqiu, zhudui_qiucha, kedui_qiucha, rangqiu_table, daxiaoqiu_table, shengpingfu_table]


def write_excel(return_data, final_time, siheyi_data, pai_data, infor_detail, name):
    """
    将现场数据写入excel
    :param return_data:
    :param final_time
    :param path:
    :return:
    """
    savepath = os.path.join(os.path.dirname(__file__), 'excel/' + name)

    # 创建工作簿
    workbook = xlsxwriter.Workbook(filename=savepath)
    worksheet = workbook.add_worksheet(name=u'数据统计')

    # 生成第一行
    row_header = ['赛事', '开赛时间', '角球初盘', '大小球初盘', '亚盘初盘', '半场比分', '全场比分', '', '']
    for i in range(50, final_time + 1):
        row_header.append(i)
    row = 0
    column = 0
    for value in row_header:
        worksheet.write(row, column, value)
        column += 1

    # 写入 射正 射正差等标示
    flag_column = ['射正', '射正', '射正差', '射正差', '射偏', '射偏', '射正率', '射正率', '危险进攻', '危险进攻', '危险比',
                   '危险比', '进攻', '进攻', '进攻比', '进攻比', '进球', '进球', '球差', '球差', '红牌', '红牌', '红牌差',
                   '胜', '平', '负', '主队水位', '亚盘盘口', '客队水位', '大球水位', '大小盘口', '小球水位']
    column = 8
    row = 1
    for value in flag_column:
        worksheet.write(row, column, value)
        row += 1

    # 按照顺序写入 射正 射正差 射偏 射正率 危险进攻 危险比 进攻 进攻比
    # 均按照先主后客的顺序
    # 均是从第7列开始
    row = 1
    data = return_data['shezheng']
    row = write_50_final_sun(worksheet, data, col=7, row=row, final_time=final_time)

    data = return_data['shezhengcha']
    row = write_50_final_sun(worksheet, data, col=7, row=row, final_time=final_time)

    data = return_data['shepian']
    row = write_50_final_sun(worksheet, data, col=7, row=row, final_time=final_time)

    data = return_data['shezhenglv']
    row = write_50_final_sun(worksheet, data, col=7, row=row, final_time=final_time)

    data = return_data['weixian']
    row = write_50_final_sun(worksheet, data, col=7, row=row, final_time=final_time)

    data = return_data['weixianbi']
    row = write_50_final_sun(worksheet, data, col=7, row=row, final_time=final_time)

    data = return_data['jingong']
    row = write_50_final_sun(worksheet, data, col=7, row=row, final_time=final_time)

    data = return_data['jingongbi']
    row = write_50_final_sun(worksheet, data, col=7, row=row, final_time=final_time)

    # 开始进球差
    zhudui_jinqiu, kedui_jinqiu, zhudui_qiucha, kedui_qiucha, rangqiu_table, daxiaoqiu_table, shengpingfu_table = siheyi_data

    row = write_50_final_zhang_jinqiu(worksheet, zhudui_jinqiu, column=7, row=row)

    row = write_50_final_zhang_jinqiu(worksheet, kedui_jinqiu, column=7, row=row)

    row = write_50_final_zhang_jinqiu(worksheet, zhudui_qiucha, column=7, row=row)

    row = write_50_final_zhang_jinqiu(worksheet, kedui_qiucha, column=7, row=row)

    # 开始红牌
    zhudui_hongpai, kedui_hongpai, hongpaicha = pai_data

    row = write_50_final_zhang_pai(worksheet, zhudui_hongpai, column=7, row=row, final_time=final_time)

    row = write_50_final_zhang_pai(worksheet, kedui_hongpai, column=7, row=row, final_time=final_time)
    # 红牌差另当别论
    column = 9
    for i in range(50, final_time + 1):
        worksheet.write(row, column, hongpaicha[i])
        column += 1
    row += 1

    # 开始四合一数据
    # 先写个汉字 四合一

    formater = workbook.add_format(
        {'border': 1, 'align': 'center', 'valign': 'vcenter'})

    column = 7
    worksheet.merge_range(row, column, row + 8, column, '四合一', cell_format=formater)

    row = write_50_final_zhang_siheyi(worksheet, shengpingfu_table, column=9, row=row)

    row = write_50_final_zhang_siheyi(worksheet, rangqiu_table, column=9, row=row)

    row = write_50_final_zhang_siheyi(worksheet, daxiaoqiu_table, column=9, row=row)

    # 开始 mian data
    column = 0
    # 赛事
    row_first = 1
    row_end = 32

    worksheet.merge_range(row_first, column, row_end, column, infor_detail['赛事'], cell_format=formater)
    column += 1

    worksheet.merge_range(row_first, column, row_end, column, infor_detail['开赛时间'], cell_format=formater)
    column += 1

    worksheet.merge_range(row_first, column, row_end, column, infor_detail['角球初盘'], cell_format=formater)
    column += 1

    worksheet.merge_range(row_first, column, row_end, column, infor_detail['大小球初盘'], cell_format=formater)
    column += 1

    worksheet.merge_range(row_first, column, row_end, column, infor_detail['亚盘初盘'], cell_format=formater)
    column += 1

    worksheet.merge_range(row_first, column, row_end, column, infor_detail['半场比分'], cell_format=formater)
    column += 1

    worksheet.merge_range(row_first, column, row_end, column, infor_detail['全场比分'], cell_format=formater)
    column += 1

    # save
    workbook.close()


def write_50_final_sun(worksheet, data, col, row, final_time):
    for value in data:
        column = col
        # 先写name
        name = value['name']
        worksheet.write(row, column, name)
        column += 2
        # 再写从 50~final_time 的数据
        for i in range(50, final_time + 1):
            worksheet.write(row, column, value[i])
            column += 1
        row += 1
    return row


def write_50_final_zhang_jinqiu(worksheet, data, column, row):
    column = column
    name = data['name']
    worksheet.write(row, column, name)
    data.pop('name')
    max_time = max(data.keys())
    column += 2
    for i in range(50, max_time + 1):
        worksheet.write(row, column, data[i])
        column += 1
    row += 1
    return row


def write_50_final_zhang_pai(worksheet, data, column, row, final_time):
    name = data['name']
    column = column
    worksheet.write(row, column, name)
    column += 2
    for i in range(50, final_time + 1):
        worksheet.write(row, column, data[i])
        column += 1
    row += 1
    return row


def write_50_final_zhang_siheyi(worksheet, data, column, row):
    max_time = max(data.keys())
    for i in range(50, max_time + 1):
        _row = row
        for value in data[i]:
            worksheet.write(_row, column, value)
            _row += 1
        column += 1
    row += 3
    return row


def getpai_event(race_events, max_minute, zhudui_name, kedui_name):
    pai_infor = []
    zhudui_hongpai = {'name': zhudui_name}
    kedui_hongpai = {'name': kedui_name}
    hongpaicha = {}
    for i in range(1, max_minute + 1):
        zhudui_hongpai[i] = 0
        kedui_hongpai[i] = 0
    for event in race_events:
        infor = event.text.strip()
        if '红牌' in infor:
            pai_infor.append(infor)
    for pai in pai_infor:
        if zhudui_name in pai:
            time = pai.split("'")[0]
            if '+'in time:
                real_time = int(time.split('+')[0])+int(time.split('+')[1])
                zhudui_hongpai[real_time] = 1
            else:
                zhudui_hongpai[int(time)] = 1

        if kedui_name in pai:
            time = pai.split("'")[0]
            if '+'in time:
                real_time = int(time.split('+')[0])+int(time.split('+')[1])
                kedui_hongpai[real_time] = 1
            else:
                kedui_hongpai[int(time)] = 1

    for i in range(1, max_minute):
        zhudui_hongpai[i + 1] = zhudui_hongpai[i + 1] + zhudui_hongpai[i]
        kedui_hongpai[i + 1] = kedui_hongpai[i + 1] + kedui_hongpai[i]
    for i in range(1, max_minute + 1):
        hongpaicha[i] = zhudui_hongpai[i] - kedui_hongpai[i]

    return [zhudui_hongpai, kedui_hongpai, hongpaicha]


def get_mian(soup):
    race_name = soup.select('.dsBreadcrumbs > a')[-1].text.strip()
    analysisRaceTime = soup.select('.analysisRaceTime')[0].text.strip()
    livetable = soup.select('.live-list-table > tbody > tr')[0]
    banchang_sort = livetable.select('td')[2].text.strip()
    quanchang_sort = livetable.select('td')[3].text.strip()
    pankou = livetable.select('td')[4].select('a')[0].text.strip().split('/')
    infor_detail = {}
    infor_detail['赛事'] = race_name
    infor_detail['开赛时间'] = analysisRaceTime
    infor_detail['角球初盘'] = pankou[2]
    infor_detail['大小球初盘'] = pankou[1]
    infor_detail['亚盘初盘'] = pankou[0]
    infor_detail['半场比分'] = banchang_sort
    infor_detail['全场比分'] = quanchang_sort

    return infor_detail
