import concurrent
import requests
from lxml import etree
import json
from concurrent.futures import ThreadPoolExecutor

def daili():
    url = 'http://gec.ip3366.net/api/?key=20210523131817589&getnum=99999'
    html = requests.get(url)
    content = html.text
    with open('代理.txt','w',encoding='utf-8')as f:
        f.write(content.strip('\n').replace('\n',''))

def get_ip():
    list_ip = []
    with open('可用代理.txt', 'r', encoding='utf-8')as f:
        content = f.readlines()
    for c in content:
        c = c.replace('\n','')
        # proxies = {
        #     "http": "http://" + c,
        #     "https": "http://" + c
        # }
        try:
            html = requests.get("https://www.baidu.com/", proxies=c, timeout=3)
            print("可以使用的代理:{}".format(c))
            # list_ip.append(proxies)
        except:
            print("代理有问题:{}".format(c))




get_ip()