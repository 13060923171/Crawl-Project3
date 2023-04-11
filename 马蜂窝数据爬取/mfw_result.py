import os
import pprint
import random
import re
import json
import threading
import time
from multiprocessing.dummy import Pool
import execjs
import redis
import requests
import hashlib
from lxml import etree


def start(headers,session,url,ggproxy):
    '''发起第一次请求'''
    # 第一次访问,直接得到JS代码
    res = session.get(url=url, headers=headers,timeout=(4,5),proxies=ggproxy)

    # 正则匹配需要的部分
    __jsl_clearance_s = re.findall('cookie=(.*?);location', res.text)[0]
    # 反混淆，分割出cookie的部分
    __jsl_clearance_s = execjs.eval(__jsl_clearance_s).split(';')[0].split('=')[1]
    print(f"__jsl_clearance_s:{__jsl_clearance_s}")
    return then(__jsl_clearance_s,headers,session,url,ggproxy)


def then(__jsl_clearance_s,headers,session,url,ggproxy):
    '''发起第二次请求'''
    cookie = {
        '__jsl_clearance_s': __jsl_clearance_s
    }
    # 携带获得的cookie进行第二次访问
    session.cookies.update(cookie)
    res = session.get(url=url, headers=headers,timeout=(4,5),proxies=ggproxy)
    go = json.loads(re.findall('};go\((.*?)\)</script>', res.text)[0])
    return parse_cookie(go,headers,session,url,ggproxy)


def parse_cookie(go,headers,session,url,ggproxy):
    '''根据sha256算法规则反解cookie'''
    global ha
    for i in range(len(go['chars'])):
        for j in range(len(go['chars'])):
            values = go['bts'][0] + go['chars'][i] + go['chars'][j] + go['bts'][1]
            if go['ha'] == 'md5':
                ha = hashlib.md5(values.encode()).hexdigest()
            elif go['ha'] == 'sha1':
                ha = hashlib.sha1(values.encode()).hexdigest()
            elif go['ha'] == 'sha256':
                ha = hashlib.sha256(values.encode()).hexdigest()
                # print(ha)
            if ha == go['ct']:
                __jsl_clearance_s = values
                print(f"__jsl_clearance_s:{__jsl_clearance_s}")
                return end(__jsl_clearance_s,headers,session,url,ggproxy)


def end(cookie,headers,session,url,ggproxy):
    '''携带cookie第三次访问,提取文件地址'''
    cookie = {
        '__jsl_clearance_s': cookie
    }
    session.cookies.update(cookie)
    res = session.get(url=url, headers=headers,timeout=(4,5),proxies=ggproxy)
    return res.text

def get_fullhtml(url):
    ggproxy = getproxy()

    try:
        headers = {
            "referer":'https://www.mafengwo.cn/i/23447333.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        session = requests.Session()
        """
        两市；上海重庆
        九省：四川，江苏、浙江、安徽、江西、湖北、湖南，云南，贵州
        """
        pagenifo = start(headers, session, url,ggproxy)
        if pagenifo.strip() == '':
            raise Exception("数据为空")
        return pagenifo
    except Exception as e:
        print(e)
        time.sleep(1)
        setproxy()

def wrap(item):
    # setproxy()
    if redis_con.get(f'{__file__}-{getTheadName()}:proxy') is None:
        setproxy()
    url = item["href"]
    print(f">>> 正在解析href： {url}")
    if redis_con.hexists('mfw:detail', url):
        print(url, '已经存在')
        return
    if not str(url.split("/")[-1].split(".")[0]).isdigit():
        print(f">>> 无效url： {url}")
        return
    pageinfo = get_fullhtml(url)
    if pageinfo != None:

        document = etree.HTML(pageinfo)
        item["出发时间"] = ''.join(document.xpath(".//li[@class='time']//text()")).strip().replace("\r",'').\
            replace("\n",'').replace("\t",'').strip()
        item["出行天数"] = ''.join(document.xpath(".//li[@class='day']//text()")).strip().replace("\r", '').replace("\n",
                                                                                                                 '').replace(
            "\t", '').strip()
        item["人物"] = ''.join(document.xpath(".//li[@class='people']//text()")).strip().replace("\r", '').replace("\n",
                                                                                                                 '').replace(
            "\t", '').strip()
        item["人均费用"] = ''.join(document.xpath(".//li[@class='cost']//text()")).strip().replace("\r", '').replace("\n",
                                                                                                                 '').replace(
            "\t", '').strip()
        item["images"] =document.xpath(".//div[@class='_j_content_box']//img/@data-src")
        item["fulltext"] = ''.join(document.xpath(".//div[@id='pnl_contentinfo']//text()"))
        if item["fulltext"].strip() == "":
            item["fulltext"] = ''.join(document.xpath(".//div[@class='_j_content_box']//text()"))
        redis_con.hset('mfw:detail', url, json.dumps(item))
        pprint.pprint(item)


def setproxy():
    proxy_api = "http://http.tiqu.alibabaapi.com/getip?num=1&type=1&neek=555458&port=11&lb=1&pb=4&regions="
    try:
        time.sleep(random.randint(2, 3))
        res = requests.get(proxy_api,timeout=(3,5)).text.strip()
        if '请2秒后再试' in res:
            print(f">>> : 请2秒后再试")
            time.sleep(3)
            return setproxy()
        if '白名单不在您的用户' in res:
            print('白名单不在您的用户')
            time.sleep(4)
            return setproxy()
        if '置为白名单' in res:
            print(f">>>请添加白名单",res)
            time.sleep(4)
            return setproxy()

        print(f'{__file__}-{getTheadName()}:proxy','线程设置',"http://" + res)
        redis_con[f'{__file__}-{getTheadName()}:proxy'] = "https://" + res
    except Exception as e:
        print(e,"设置代理错误！")
        time.sleep(random.randint(4,10))
        return setproxy()

def getproxy():
    text = redis_con.get(f'{__file__}-{getTheadName()}:proxy').decode()
    print(f'{__file__}-{getTheadName()}:proxy', '线程获取',  text)
    if text == None:
        print(f">>> 代理为空： {None}")
        time.sleep(3)
        return getproxy()
    return {
        "https":text
    }

def getTheadName():
    return threading.currentThread().getName()

if __name__ == '__main__':

    redis_con = redis.Redis(db=1)
    pepoles = [json.loads(i.decode()) for i in redis_con.hvals('mfw:result')]
    pool = Pool(3)
    pool.map(wrap,pepoles)
    # for pep in pepoles:
    #     wrap(pep)


