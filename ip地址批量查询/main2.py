import requests
from lxml import etree
import time
from tqdm import tqdm
import random

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


def parse_url(url):
    html = requests.get(url,headers=headers)
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


if __name__ == '__main__':
    list_ip = get_data()
    count = 0
    for l in tqdm(list_ip):
        url = 'https://site.ip138.com/{}/'.format(l)
        count += 1
        if count == 100:
            time.sleep(300)
            count = 0
        else:
            parse_url(url)
            time.sleep(1)
