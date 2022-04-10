import json
import random
import time
from multiprocessing.dummy import Pool

import numpy as np
import pandas
import requests
import re
pool = Pool(5)
from lxml import etree

proxy_api = 'http://http.tiqu.alibabaapi.com/getip?num=1&type=2&neek=563834&port=11&lb=1&pb=4&regions='
golols = {
    "dl":{
        'https':'16150'
    }
}

def setproxy():
    try:
        time.sleep(random.randint(1, 3))
        res = requests.get(proxy_api)
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
        "cookie": "acw_sc__v2="
    }
    while True:
        try:
            r = requests.get('https://jobs.51job.com/beijing/133817725.html', headers=headers
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
            if '<title>æ»å¨éªè¯é¡µé¢</title>' in r.text:
                print(f"切换ck后任然无法获取数据")
                setproxy()
            break
        except  Exception as e:
            print(f"网络异常：{e}")
            setproxy()
            time.sleep(2)
    etree_html = etree.HTML(r.content.decode('gbk',errors='ignore'))
    infodata = etree_html.xpath(".//div[@class='bmsg job_msg inbox']//text()")
    if len(infodata) ==0:
        print(r.text)
    return {
        "content":';'.join(infodata),
        "tell_c":''.join(etree_html.xpath(".//div[@class='tCompany_main']/div[2]//text()")),
        "com_info": ''.join(etree_html.xpath(".//div[@class='tCompany_main']/div[3]//text()"))
    }





def mapwork(ijob,pagenum):
    saveitem = {}
    saveitem['fabutime'] = ijob.get("issuedate")
    saveitem['leibie'] = ijob.get("job_title")
    saveitem['attlist'] = str(ijob.get("attribute_text"))
    saveitem['gangwei'] = ijob.get("job_title")
    saveitem['company'] = ijob.get("company_name")
    saveitem['compXinZhi'] = ijob.get("companytype_text")
    saveitem['comGuimo'] = ijob.get("companysize_text")
    saveitem['comlabel'] = ijob.get("companyind_text")
    saveitem['url'] = ijob.get("job_href")
    saveitem['place'] = ijob.get("workarea_text")
    saveitem['xueli'] = ijob.get("attribute_text")[1] if len(ijob.get("attribute_text")) > 1 else ''
    saveitem['jingyan'] = ijob.get("attribute_text")[2] if len(ijob.get("attribute_text")) > 2 else ''
    saveitem['num'] = ijob.get("attribute_text")[3] if len(ijob.get("attribute_text")) > 3 else ''
    print(f" 页码：{pagenum} 数据：{saveitem}")
    # print(f"岗位描述：{des}")
    print("*" * 50 + '\n' )
    with open("comp.txt",'a',encoding='utf-8') as ff:
        ff.write(json.dumps(saveitem))
        ff.write('\n')
def start_project_detail():
    result = []
    with open("comp.txt",'r',encoding='utf-8') as ff:
        lines = [i.strip() for i in ff.readlines()][1600:]
    for iline in lines:
        try:
            result.append(json.loads(iline))
        except:
            continue
    print(f"当前comp文件链接数：{len(result)}")
    pool.map(downloaddetail,result)

def downloaddetail(item):
    job_item = item.copy()
    job_item["spider_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    try:
        data = geturldata(item.get("url"))
        job_item['fullcontent'] = data.get("content")
        job_item['tell_c'] = data.get("tell_c")
        job_item['com_info'] = data.get("com_info")
    except Exception as e:
        print(f"请求异常：{e}")
        job_item['fullcontent'] = ''
        job_item['tell_c'] = ''
        job_item['com_info'] = ''
    loginf = job_item["fullcontent"].replace("\r","").replace("\n","").replace("\t","").replace(" ","")
    print(f'链接：{job_item.get("job_href")} 描述：{loginf}')

    ###此处处理整个json内容到数据库 ==》 job_item
    with open("funnc.txt",'a',encoding='utf-8') as fc:
        fc.write(json.dumps(job_item))
        fc.write('\n')

if  __name__ == "__main__":
    setproxy()
    start_project_detail()

