# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import urllib.parse
from items import TripadvisorItem


class CommentSpider(scrapy.Spider):
    name = 'comment'

    headers = {
        'Accept': 'text/html, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-us',
        'Connection': 'keep-alive',
        'Content-Length': '60',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.tripadvisor.cn',
        'Cookie': 'CM=%1%HanaPersist%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CSPHRSess%2C%2C-1%7CHanaSession%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCpmPopunder_1%2C%2C-1%7CCCSess%2C%2C-1%7CCpmPopunder_2%2C1%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CSPHRPers%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7Csh%2C%2C-1%7CLastPopunderId%2C137-1859-null%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCCPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CCPNC%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; TASession=%1%V2ID.5F0C14340ED06BF7E8E6708A200AAA9D*SQ.6*LP.%2FAttraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian%5C.html*LS.DemandLoadAjax*GR.5*TCPAR.81*TBR.56*EXEX.95*ABTR.61*PHTB.50*FS.40*CPU.89*HS.recommended*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.zhCN*FA.1*DF.0*MS.-1*RMS.-1*TRA.true*LD.1131761; TAUD=LA-1526787060111-1*RDD-1-2018_05_20*LG-507596-2.1.F.*LD-507597-.....; ki_r=; ki_t=1526787063034%3B1526787063034%3B1526787063034%3B1%3B1; __gads=ID=8eb37e3580058996:T=1526787061:S=ALNI_MZBnQ4srwY6peqooD00OSdfYXXF5g; _ga=GA1.2.813684519.1526787059; _gid=GA1.2.1514555468.1526787059; WLRedir=requested; roybatty=TNI1625!ACM0cKVzPqchWChBVHK%2BPK%2BEvuAgmcO%2BrDdwPcRXD%2FEkGheCd8ySLHUW%2Bhm3lmJu4jq11AL7KBNMHX%2BNHzppC0sXMK5M2lyHfFm8TAmjkL%2BRy4uCXtcJ6huHmMKK%2FRWsAdncQtYLECvkGSNs%2FpHE1WZnJKFBzn5%2BrbYvtAU8HFhm%2C1; ServerPool=R; TAReturnTo=%1%%2FAttraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian.html; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1; TAUnique=%1%enc%3Ah80T8xLrvFtco26EFYDBjq1%2By%2FtcXqy5b8Cn%2FjigPLU%3D; TART=%1%enc%3A2KWdmqTAjLV5f4OA4S1YYsBC65pCtZ8RjJL6lC4xPB2hPtY47fc81VztCFRa2Pb9; TASSK=enc%3AAGBZBqXe7ZU2PED8vh89iu6QOA6pLqiQN%2BiScK4OceIZeTRwPPgRj7NfaEPTkDH1img%2F78MyexiDpmJeDeUtXhJRx8%2FwRC5%2BASfmnVJXAHleWfML%2FplMadnSQ6Hk9IPKOg%3D%3D',
        'Origin': 'https://www.tripadvisor.cn',
        'Referer': 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-or10-Gulangyu_Island-Xiamen_Fujian.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'X-Puid': 'WwDr8H8AAAEAAH-NQagAAABB',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # def parse(self, response):
    #     # 获取认证的cookie和X_Puid并开始获取评论数据
    #     __gads = '; __gads=ID=1cc6d38d56f3330d:T=1526788672:S=ALNI_Ma0_TgGqqVguU_V5kDj6T70HHnnow'
    #     _ga = '; _ga=GA1.2.820569739.1526788672'
    #     _gid = '; _gid=GA1.2.820569739.1526788672'
    #     WLRedir ='; WLRedir=requested'
    #     ki_r = '; '
    #     ki_t = '; 1526788672230%3B1526788672230%3B1526788672230%3B1%3B1'
    #     cookie = response.meta['cookie']
    #     cookie += __gads
    #     cookie += _ga
    #     cookie += _gid
    #     cookie += WLRedir
    #     cookie += ki_r
    #     cookie += ki_t
    #     X_Puid = response.meta['X_Puid']
    #
    #     next_headers = {
    #         'Accept': 'text/html, */*',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'en-us',
    #         'Connection': 'keep-alive',
    #         'Content-Length': '60',
    #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #         'Host': 'www.tripadvisor.cn',
    #         'Origin': 'https://www.tripadvisor.cn',
    #         'Cookie': cookie,
    #         'Referer': 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian.html',
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    #         'X-Requested-With': 'XMLHttpRequest',
    #         'X-Puid': X_Puid
    #     }
    #     formdata = {
    #         'reqNum': '1',
    #         'changeSet': 'REVIEW_LIST',
    #         'puid': X_Puid
    #     }
    #     yield scrapy.FormRequest(
    #         url='https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-or10-Gulangyu_Island-Xiamen_Fujian.html',
    #         headers=next_headers,
    #         formdata=formdata,
    #         callback=self.parse_detail
    #     )


    # def parse_detail(self, response):
    # 获取前10条
    # names = response.css('div.username.mo > span::text').extract()
    # titles = response.css('span.noQuotes::text').extract()
    # comments = response.css('div.review-container p.partial_entry::text').extract()
    # 进行cookie验证
    # 获取roybatty
    # pattern = re.compile(r'taSecureToken = "(.*?)";')
    # roybatty = pattern.search(response.text).group(1)
    # roybatty += ',1'
    # roybatty = urllib.parse.quote(roybatty)
    # roybatty = '; ' + 'roybatty=' + roybatty
    # # 获取cookie并格式化
    # cookie = response.headers.getlist('Set-Cookie')
    # cookie = [c.decode() for c in cookie]
    # cookie = [c for c in cookie if not c.startswith('SRT')]
    # cookie = '; '.join(cookie)
    # cookie += roybatty
    # # 获取X-Puid
    # pattern = re.compile(r"'X-Puid', '(.*?)'")
    # try:
    #     X_Puid = pattern.search(response.text).group(1)
    # except:
    #     pass
    # # CookiePingback
    # cookie_pingback_headers = {
    #     'Accept': 'text/html, */*',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'en-us',
    #     'Connection': 'keep-alive',
    #     'Content-Length': '0',
    #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #     'Host': 'www.tripadvisor.cn',
    #     'Origin': 'https://www.tripadvisor.cn',
    #     'Cookie': cookie,
    #     'Referer': 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian.html',
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    #     'X-Requested-With': 'XMLHttpRequest'
    # }
    # yield scrapy.FormRequest(
    #     url='https://www.tripadvisor.cn/CookiePingback?early=true',
    #     headers=cookie_pingback_headers,
    #     meta={'cookie': cookie,
    #           'X_Puid': X_Puid},
    #     callback=self.parse
    # )

    def parse(self, response):
        # 获取前10条
        names = response.css('div.username.mo > span::text').extract()
        titles = response.css('span.noQuotes::text').extract()
        comments = response.css('div.review-container p.partial_entry::text').extract()
        for name, title, comment in zip(names, titles, comments):
            item = TripadvisorItem()
            item['name'] = name
            item['title'] = title
            item['comment'] = comment
            yield item

    def start_requests(self):
        # 第一页
        url = 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian.html'
<<<<<<< HEAD:scrapy_templates/social/travel/tripadvisor/tripadvisor/spiders/comment.py
        header = {
=======
        headers = {
            'Host': 'www.tripadvisor.cn',
>>>>>>> bc07d23c48ab57901eafd684c4fd45b7ff6f27f6:scrapy_templates/travel/tripadvisor/tripadvisor/spiders/comment.py
            'Accept': 'text/html, */*',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.tripadvisor.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
            'X-Puid': 'WwEkXMCoCxsAAKEJLKoAAAAb',
            'Connection': 'keep-alive',
            'Referer': 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian.html',
        }
        url = 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian.html'
        # yield Request(url=url, headers=header, callback=self.parse)
        page = 0
        # while page < 481:
        #     if page == 0:
        #         url = 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian.html'
        #         yield Request(url=url, headers=header, callback=self.parse)
        #     else:
        #         url = 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-or{}-Gulangyu_Island-Xiamen_Fujian.html'.format(
        #             page * 10)
        #         yield Request(url=url, headers=header, callback=self.parse)
        #     page += 1

<<<<<<< HEAD:scrapy_templates/social/travel/tripadvisor/tripadvisor/spiders/comment.py
            # 英文 共79页
        cookie_pingback_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'www.tripadvisor.cn',
            'Cookie': 'TASession=%1%V2ID.7F04C1BD202C2FA41FCC25619EEB72D2*SQ.25*LP.%2FAttraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian%5C.html*LS.DemandLoadAjax*GR.8*TCPAR.22*TBR.74*EXEX.74*ABTR.45*PHTB.31*FS.79*CPU.25*HS.recommended*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*MS.-1*RMS.-1*FLO.1131761*TRA.false*LD.1131761; ServerPool=X; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1; CM=%1%HanaPersist%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CSPHRSess%2C%2C-1%7CHanaSession%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCpmPopunder_1%2C1%2C1526886107%7CCCSess%2C%2C-1%7CCpmPopunder_2%2C1%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CSPHRPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7Csh%2C%2C-1%7CLastPopunderId%2C137-1859-null%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCCPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CCPNC%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; TAUD=LA-1526798701478-1*RDD-1-2018_05_20*LG-2086119-2.1.F.*LD-2086120-.....; TAReturnTo=%1%%2FAttraction_Review-g297407-d1131761-Reviews-or10-Gulangyu_Island-Xiamen_Fujian.html; TASSK=enc%3AACl88oFmUTsVbKDRT3FmRAGLxYLfkoLicgStdV5EA8akitf2DgZHdye8PTeSzRoIlq19GO6DwXu9U6oC5mk3rHB9mOyCI3GSf0c31c0aH9rhYgQeeRxyjiNbymzb0QRE5Q%3D%3D; TART=%1%enc%3A2KWdmqTAjLXO%2BMUpmWOT4AISp1TB0NovfZfHbA8oZf6JSMZdl6%2BBjE9EbpOS6JMl; TAUnique=%1%enc%3AZXpLd80PSE09QrF0ZKnWgoAbxw24P5msBpMSXPU3aXI%3D; _ga=GA1.2.329674388.1526798697; _gid=GA1.2.1962382444.1526798697; TALanguage=en; __gads=ID=1d40382bf896456b:T=1526798707:S=ALNI_MYnhzrBzFPDCIdEqhQg8wdq75MN5w; ki_t=1526798720078%3B1526798720078%3B1526800787149%3B1%3B4; ki_r=; roybatty=TNI1625!ANElSaK79p2nZMnQDFsEpvxHxub32COhdMVM6MCBGnJ7mVYek5m4KPb3SSHBoxvZPtkqAU4ENeoUl6II%2BcCSReg1C1mUordDvJ7xrzVm3fa6jo497x2HCuEG25aV3nCqIgMRyYmNCqpj4LM4QCCZjjRGpbl2aetV%2BB1tYfIVV84A%2C1; _gat_UA-79743238-4=1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
         }
        page = 0
        while page < 2:
            if page == 0:
                url = 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian.html'
                yield Request(url=url, headers=cookie_pingback_headers, callback=self.parse)
            else:
                url = 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-or{}-Gulangyu_Island-Xiamen_Fujian.html'.format(
                    page * 10)
                yield Request(url=url, headers=cookie_pingback_headers, callback=self.parse)
            page += 1
=======
        # page = 0
        # while page < 5:
        #     if page == 0:
        #         url = 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian.html'
        #         yield Request(url=url, headers=headers, callback=self.parse)
        #     else:
        #         url = 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-or{}-Gulangyu_Island-Xiamen_Fujian.html'.format(
        #             page * 10)
        #         yield Request(url=url, headers=headers, callback=self.parse)
        #     page += 1


        formdata = {
            'returnTo': '#REVIEWS',
            'filterLang': 'en',
            'filterSeasons': '',
            'filterSegment': '',
            'filterRating': '',
            'reqNum': '1',
            'changeSet': 'REVIEW_LIST',
            'puid': 'WwEkXMCoCxsAAKEJLKoAAAAb'
        }
        # 英文 共79页
        page = 0
        while page < 80:
            if page == 0:
                url = 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-Gulangyu_Island-Xiamen_Fujian.html'
            else:
                url = 'https://www.tripadvisor.cn/Attraction_Review-g297407-d1131761-Reviews-or{}-Gulangyu_Island-Xiamen_Fujian.html'.format(
                    page * 10)
            page += 1
            post = scrapy.FormRequest(
                url=url,
                headers=headers,
                formdata=formdata,
                callback=self.parse
            )
            yield post
>>>>>>> bc07d23c48ab57901eafd684c4fd45b7ff6f27f6:scrapy_templates/travel/tripadvisor/tripadvisor/spiders/comment.py
