import hashlib
import json
import random
import threading
import time
import os
import copyheaders
import redis
import requests
from lxml import etree

redis_con = redis.Redis(db=1)
headers = copyheaders.headers_raw_to_dict(b"""
accept: application/json, text/javascript, */*; q=0.01
content-type: application/x-www-form-urlencoded; charset=UTF-8
cookie: __jsluid_s=30499397eea47bf4c48ac3bde3d9abf9; mfw_uuid=63218ea7-b577-968e-5751-73fbf462ff5e; uva=s%3A92%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1663143592%3Bs%3A10%3A%22last_refer%22%3Bs%3A24%3A%22https%3A%2F%2Fwww.mafengwo.cn%2F%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1663143592%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=63218ea7-b577-968e-5751-73fbf462ff5e; _r=bing; __jsluid_h=2273f7d3549f13c79309c65b76b2dc74; PHPSESSID=vpk16hj1s7nsathaq8mnvfr5g1; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A13%3A%22www.bing.com%2F%22%3Bs%3A1%3A%22t%22%3Bi%3A1666667662%3B%7D; oad_n=a%3A5%3A%7Bs%3A5%3A%22refer%22%3Bs%3A21%3A%22https%3A%2F%2Fwww.bing.com%2F%22%3Bs%3A2%3A%22hp%22%3Bs%3A12%3A%22www.bing.com%22%3Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A13%3A%22m.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222022-10-25+11%3A14%3A22%22%3B%7D; __mfwothchid=referrer%7Cwww.bing.com; __omc_chl=; __mfwc=referrer%7Cwww.bing.com; __mfwa=1663143587415.40576.4.1663147626010.1666667663060; __mfwlv=1666667663; __mfwvn=2; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1666667664; bottom_ad_status=0; __omc_r=; cc=UGD632110431000871666667753104; tt=https%3A%2F%2Fm.mafengwo.cn%2Fyj%2F10035; current_url=https%3A%2F%2Fm.mafengwo.cn%2Fmdd%2F10035; source=ug-seo-bing; source_data=%7B%22event_id%22%3A%22UGD632110431000871666667753104%22%2C%22uuid%22%3A%2263218ea7-b577-968e-5751-73fbf462ff5e%22%2C%22share_uuid%22%3A%22%22%2C%22wake_way%22%3A%22deeplink%22%2C%22UA%22%3A%22safari%22%2C%22platform%22%3A%22h5%22%7D; __mfwlt=1666668124; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1666668126; ariaDefaultTheme=undefined
origin: https://www.mafengwo.cn
referer: https://www.mafengwo.cn/travel-scenic-spot/mafengwo/10208.html
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47
x-requested-with: XMLHttpRequest
""")



proxy_host = 'http-dynamic-S02.xiaoxiangdaili.com'
proxy_port = 10030
proxy_username = '916959556566142976'
proxy_pwd = 'qHDFwFYk'

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
        "user": proxy_username,
        "pass": proxy_pwd,
}

proxies = {
        'http': proxyMeta,
        'https': proxyMeta,
}




def reqPost(body):


    while 1:
        try:
            res = requests.post(
                'https://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist',
                headers=headers,
                timeout=(4,5),
                data=body,
                # proxies=proxies
            )
            return res.json()
        except Exception as e:
            print(f">>> error: {e}")
            time.sleep(1)

def search(mddid,mddname):

    for icust in [str(i) for i in range(1,5)]:
        for page in range(1,2000):
            timesamp = str(int(time.time())*1000)
            params = {"_ts":timesamp,"cost":icust,"days":"0","mddid":mddid,"month":"0","page":str(page),"pageid":"mdd_index","sort":"2","tagid":"0"}
            encparams = '{"_ts":"'+timesamp+'","cost":"'+icust+'","days":"0","mddid":"'+mddid+'","month":"0","page":"'+str(page)+'","pageid":"mdd_index","sort":"2","tagid":"0"}c9d6618dbc657b41a66eb0af952906f1'
            params["_sn"] = hashlib.md5(encparams.encode()).hexdigest()[2:12]

            respons = reqPost(params)
            document = etree.HTML(respons.get("list"))

            h_list = document.xpath(".//div[@class='tn-item clearfix']")
            print(f'【{mddname}】 【{icust}】 【{page}】 ',len(h_list))
            for hli in h_list:
                saveiten = {}
                saveiten["areaid"] = mddid
                saveiten["areaname"] = mddname
                saveiten["href"] = 'https://www.mafengwo.cn'+ ''.join(hli.xpath(".//a[@class='title-link']/@href"))
                saveiten["title"] = ''.join(hli.xpath(".//a[@class='title-link']/text()")).strip()
                saveiten["abs"]=  ''.join(hli.xpath(".//dl/dd//text()")).strip()
                saveiten["auth"] = ''.join(hli.xpath(".//span[@class='tn-user']//text()")).strip()
                saveiten["views"] = ''.join(hli.xpath(".//span[@class='tn-nums']//text()")).strip()
                print(f'【{mddname}】 【{icust}】 【{page}】 ',saveiten)

                if not str(saveiten["href"].split("/")[-1].split(".")[0]).isdigit():
                    print(f">>> 无效url： {saveiten['href']}")
                    continue

                redis_con.hset('mfw:result', str(saveiten['href']), json.dumps(saveiten))
            if len(h_list) <=4:
                break







if __name__ == "__main__":
    # search(mddid='26496', mddname='番禺')
    search(mddid='18341',mddname='从化')
