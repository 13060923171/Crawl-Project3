import requests
from lxml import etree
import time
from tqdm import tqdm
import random
import threadpool
import os
import json
import threading as th
import concurrent.futures
user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

headers = {
    "Cookie": "Hm_lvt_d39191a0b09bb1eb023933edaa468cd5=1633438037; PHPSESSID=a10slgalqur20gr9fkkjdoilnk; Hm_lpvt_d39191a0b09bb1eb023933edaa468cd5=1633438194",
    "user-agent": random.choice(user_agent),
}


def parse_url(url, proxies):

    # html = requests.get(url,headers=headers,proxies=json.loads(content2[proxies].replace('\n','').replace("'",'"')), timeout=3)
    html = requests.get(url, headers=headers, proxies=proxies,
                        timeout=3)
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)


def get_html(html):
    content = html.text
    soup = etree.HTML(content)
    try:
        href = soup.xpath("//ul[@id='list']/li/a/@href")
        for h in href:
            write_txt(h)
        time.sleep(0.2)
    except Exception as e:
        print('请过一会再试', e)


def write_txt(content):
    with open('输出文本.txt', 'a+', encoding='utf-8')as f:
        f.write(content+'\n')
        print('写入成功')


def get_data():
    list_ip = []
    for i in range(0, 256, 1):
        for j in range(0, 256, 1):
            #需要修改的地方
            ip = "39.102" + "." + str(i) + "." + str(j)
            list_ip.append(ip)
    return list_ip


def daili():
    url = 'https://api.juliangip.com/api/dynamic/getdynamic?num=50&pt=1&resultType=text&split=\\r\\n&tradeNo=1048021442024661&type=time&sign=d56f140b46408243f65020d7651fabc7'
    html = requests.get(url)
    content = html.text
    with open('代理.txt','w',encoding='utf-8')as f:
        f.write(content)

def get_ip(url):
    with open('代理.txt', 'r', encoding='utf-8')as f:
        content = f.readlines()
    for c in content:
        c = c.replace('\n','')
        proxies = {
            "http": "http://" + c,
            "https": "http://" + c
        }
        test_proxies(proxies,url)
    #     list_ip1.append(([proxies,],None))
    #
    # return list_ip1

def test_proxies(proxies,url):
    try:
        html = requests.get("https://www.baidu.com/", proxies=proxies, timeout=3)
        parse_url(url, proxies)
        # print("可以使用的代理:{}".format(proxies))
        # with open('可用代理.txt', 'a+', encoding='utf-8')as f:
        #     f.write("{}".format(proxies) + "\n")
        # list_ip1.append(proxies)
    except:
        # print("不可以使用的代理:{}".format(proxies))
        pass

# def pool_thread():
#     # daili()
#     list_ip1 = get_ip()
#     pool = threadpool.ThreadPool(50)
#     # 往线程里面添加URL，makeRequests创建任务，创建100个任务
#     reque = threadpool.makeRequests(test_proxies, list_ip1)
#     # 用一个for循环线程池
#     for r in reque:
#         # putRequest提交这100个任务，往线程池里面提交100个任务
#         pool.putRequest(r)
#     pool.wait()

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10)as e:
        #调用这个函数，用一个列表的形式把这个函数给保存下来
        futuers = [e.submit(get_ip,'https://site.ip138.com/{}/'.format(l)) for l in list_ip]
        #用叠带把这个函数的内容一个个打印出来
        for futuer in concurrent.futures.as_completed(futuers):
            print(futuer.result())
    # for l in tqdm(list_ip):
    #     url = 'https://site.ip138.com/{}/'.format(l)
    #     get_ip(url)

if __name__ == '__main__':
    list_ip = get_data()
    t1 = th.Thread(target=daili)
    t2 = th.Thread(target=main)
    #开始线程保护
    t1.setDaemon(True)
    #开启线程
    t1.start()
    t2.setDaemon(True)
    t2.start()
    #加一个线程阻塞
    t1.join()
    t2.join()
    # get_ip()
    # # pool_thread()
    # list_ip = get_data()
    # count = 0
    # number1 = 0
    # number3 = 0
    # with open('可用代理.txt', 'r', encoding='utf-8')as f:
    #     content2 = f.readlines()
    # number2 = len(content2)
    # # test = content2[0].replace('\n','').replace("'",'"')
    # # test_dict = json.loads(test)
    #
    # for l in tqdm(list_ip):
    #     url = 'https://site.ip138.com/{}/'.format(l)
    #     count += 1
    #     if count == 50:
    #         count = 0
    #         number1 += 1
    #         parse_url(url, proxies=json.loads(content2[number1].replace('\n','').replace("'",'"')))
    #         number3 += 1
    #
    #         if number3 == number2:
    #             os.remove(r'可用代理.txt')
    #             get_ip()
    #             with open('可用代理.txt', 'r', encoding='utf-8')as f:
    #                 content2 = f.readlines()
    #             number2 = len(content2)
    #             number1 = 0
    #             number3 = 0
    #             continue
    #     else:
    #         # print(number1)
    #         parse_url(url, proxies=json.loads(content2[number1].replace('\n','').replace("'",'"')))
