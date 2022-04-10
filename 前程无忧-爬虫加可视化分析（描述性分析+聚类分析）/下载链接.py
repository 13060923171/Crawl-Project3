import json
import os
import random
import time
from multiprocessing.dummy import Pool

import numpy as np
import pandas
import requests
import re
pool = Pool(3)
from lxml import etree

proxy_api = 'http://http.tiqu.alibabaapi.com/getip?num=1&type=2&neek=563834&port=11&lb=1&pb=4&regions='
golols = {
    "dl":{
        'https':'16150'
    }
}

# classify = {
#         "01": "计算机软件",
#         37: "计算机硬件",
#         38: "计算机服务(系统、数据服务、维修)",
#         31: "通信/电信/网络设备",
#         39: "通信/电信运营、增值服务",
#         32: "互联网/电子商务",
#         40: "网络游戏",
#         "02": "电子技术/半导体/集成电路",
#         35: "仪器仪表/工业自动化",
#         41: "会计/审计",
#         "03": "金融/投资/证券",
#         42: "银行",
#         43: "保险",
#         62: "信托/担保/拍卖/典当",
#         "04": "贸易/进出口",
#         22: "批发/零售",
#         "05": "快速消费品(食品、饮料、化妆品)",
#         "06": "服装/纺织/皮革",
#         44: "家具/家电/玩具/礼品",
#         60: "奢侈品/收藏品/工艺品/珠宝",
#         45: "办公用品及设备",
#         14: "机械/设备/重工",
#         33: "汽车",
#         65: "汽车零配件",
#         "08": "制药/生物工程",
#         46: "医疗/护理/卫生",
#         47: "医疗设备/器械",
#         12: "广告",
#         48: "公关/市场推广/会展",
#         49: "影视/媒体/艺术/文化传播",
#         13: "文字媒体/出版",
#         15: "印刷/包装/造纸",
#         26: "房地产",
#         "09": "建筑/建材/工程",
#         50: "家居/室内设计/装潢",
#         51: "物业管理/商业中心",
#         34: "中介服务",
#         63: "租赁服务",
#         "07": "专业服务(咨询、人力资源、财会)",
#         59: "外包服务",
#         52: "检测，认证",
#         18: "法律",
#         23: "教育/培训/院校",
#         24: "学术/科研",
#         11: "餐饮业",
#         53: "酒店/旅游",
#         17: "娱乐/休闲/体育",
#         54: "美容/保健",
#         27: "生活服务",
#         21: "交通/运输/物流",
#         55: "航天/航空",
#         19: "石油/化工/矿产/地质",
#         16: "采掘业/冶炼",
#         36: "电气/电力/水利",
#         61: "新能源",
#         56: "原材料和加工",
#         28: "政府/公共事业",
#         57: "非营利组织",
#         20: "环保",
#         29: "农/林/牧/渔",
#         58: "多元化业务集团公司"
#     }

def setproxy():
    try:
        time.sleep(random.randint(1, 3))
        res = requests.get(proxy_api)
        print(res.text)
        ip = (res.json().get("data")[0].get("ip") + ":" +res.json().get("data")[0].get("port") )
        golols['dl']["https"] = "https://" + ip
        print("https://" + ip)
    except Exception as e:
        print(e,"设置代理错误！")
        time.sleep(random.randint(1,3))
        setproxy()

def get_hexxor(s1, _0x4e08d8):
    _0x5a5d3b = ''

    for i in range(len(s1)):
        if i % 2 != 0: continue
        _0x401af1 = int(s1[i: i + 2], 16)
        _0x105f59 = int(_0x4e08d8[i: i + 2], 16)
        _0x189e2c_10 = (_0x401af1 ^ _0x105f59)
        _0x189e2c = hex(_0x189e2c_10)[2:]
        if len(_0x189e2c) == 1:
            _0x189e2c = '0' + _0x189e2c
        _0x5a5d3b += _0x189e2c
    return _0x5a5d3b


def get_unsbox(arg1):
    _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19,
                 0xd,
                 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c,
                 0x22, 0x25, 0xc, 0x24]
    _0x4da0dc = []
    _0x12605e = ''
    for i in _0x4b082b:
        _0x4da0dc.append(arg1[i - 1])
    _0x12605e = "".join(_0x4da0dc)
    return _0x12605e

def geturldata(url):
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Host': 'jobs.51job.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
        'X-Requested-With': 'XMLHttpRequest',
        "cookie": "acw_sc__v2=620b1bbfad96f4f5b65f77ef6062958afa930983"
    }
    while True:
        try:
            r = requests.get(url, headers=headers
                             , proxies=golols["dl"],timeout=10)
            arg1s = re.findall("arg1=\'(.*?)\'", r.text)
            if len(arg1s) == 0:
                print(f"无法获取setcookie {arg1s} 尝试切换代理！")
                setproxy()
                time.sleep(4)
                continue
            break
        except  Exception as e:
            print(f"网络异常：{e}")
            setproxy()
    s1 = get_unsbox(arg1s[0])
    _0x4e08d8 = "3000176000856006061501533003690027800375"
    _0x12605e = get_hexxor(s1, _0x4e08d8)
    print(f"更新_0x12605e： {_0x12605e}")
    headers = {
        # 'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Host': 'jobs.51job.com',
        'Pragma': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
        'X-Requested-With': 'XMLHttpRequest',
        "cookie": "acw_sc__v2=%s" % _0x12605e
    }
    while True:
        try:
            r = requests.get(url, headers=headers, proxies=golols["dl"], timeout=10)
            break
        except  Exception as e:
            print(f"网络异常：{e}")
            setproxy()
            time.sleep(2)
    etree_html = etree.HTML(r.content.decode('gbk',errors='ignore'))
    infodata = etree_html.xpath(".//div[@class='bmsg job_msg inbox']//text()")
    if len(infodata) ==0:
        print(r.text)
    return ';'.join(infodata)

def get_page_searchdata(url):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Host': 'search.51job.com',
        'Pragma': 'no-cache',
        'Referer': 'https://search.51job.com/list/010000,000000,0000,00,9,99,java,2,15.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
        'X-Requested-With': 'XMLHttpRequest',
        "cookie": "acw_sc__v2=%s" % ''
    }
    while True:
        try:
            r = requests.get(url, headers=headers,
                             proxies=golols["dl"],
                             timeout=10)
            print(r.text)
            arg1s = re.findall("arg1=\'(.*?)\'", r.text)
            if '"engine_jds":' in r.text:
                return r.json()
            if len(arg1s) == 0:
                print(f"无法获取setcookie {arg1s} 尝试切换代理！")
                setproxy()
                continue
            break
        except  Exception as e:
            print(f"网络异常：{e}")
            setproxy()
    s1 = get_unsbox(arg1s[0])
    _0x4e08d8 = "3000176000856006061501533003690027800375"
    _0x12605e = get_hexxor(s1, _0x4e08d8)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Host': 'search.51job.com',
        'Pragma': 'no-cache',
        'Referer': 'https://search.51job.com/list/010000,000000,0000,00,9,99,java,2,15.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
        'X-Requested-With': 'XMLHttpRequest',
        "cookie": "acw_sc__v2=%s" % _0x12605e
    }
    while True:
        try:
            ssr = requests.get(url, headers=headers,
                               proxies=golols["dl"],
                               timeout=10).json()
            break
        except  Exception as e:
            print(f"网络异常：{e}")
            setproxy()
            get_page_searchdata(url)
    return ssr


def start_project_links(gw_code='00',gw_name='-',citycode='000000',city_name='+',keyword='大数据开发工程师',price='-'):
    gololstimer = {"index": 0}
    while True:
        gololstimer["index"] += 1
        url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{keyword},2,{gololstimer["index"]}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
        page_source_data = get_page_searchdata(url)
        print(page_source_data)
        jobs_data = page_source_data.get("engine_jds")
        for ijob in jobs_data:
            mapwork(ijob,gololstimer["index"],city_name)
        if gololstimer["index"] >= int(page_source_data.get("total_page"))  or   gololstimer["index"] >=2000:
            print(f"超出页码限制 ==》 exit {gololstimer['index']} {page_source_data.get('total_page')}")
            break
        # pool.map(mapwork,jobs_data)
def mapwork(ijob,pagenum,city_name):
    saveitem = {}
    saveitem['fabutime'] = ijob.get("issuedate")
    saveitem['leibie'] = ijob.get("job_title")
    # saveitem['attlist'] = str(ijob.get("attribute_text"))
    saveitem['gangwei'] = ijob.get("job_title")
    saveitem['company'] = ijob.get("company_name")
    saveitem['providesalary_text'] = ijob.get("providesalary_text")
    saveitem['compXinZhi'] = ijob.get("companytype_text")
    saveitem['comGuimo'] = ijob.get("companysize_text")
    saveitem['comlabel'] = ijob.get("companyind_text")
    saveitem['url'] = ijob.get("job_href")
    saveitem['place'] = ijob.get("workarea_text").split("-")
    saveitem['xueli'] = ijob.get("attribute_text")[1] if len(ijob.get("attribute_text")) > 1 else ''
    saveitem['jingyan'] = ijob.get("attribute_text")[2] if len(ijob.get("attribute_text")) > 2 else ''
    saveitem['num'] = ijob.get("attribute_text")[3] if len(ijob.get("attribute_text")) > 3 else ''
    print(f" 页码：{pagenum} 数据：{saveitem}")
    print("*" * 50 + '\n' )
    with open("comp.txt",'a',encoding='utf-8') as ff:
        ff.write(json.dumps(saveitem))
        ff.write('\n')

def init():
    res = requests.get('http://httpbin.org/get').json()
    ip = res.get("origin")
    base_api = f'https://ty-http-d.hamir.net/index/white/add?neek=tyhttp447242&appkey=7a708324dfca56cbaee3dcb908ca5198&white=' + ip
    res = requests.get(base_api).json()
    print(f'添加白名单状态：{res}')

if  __name__ == "__main__":
    init()
    setproxy()
    start_project_links()
