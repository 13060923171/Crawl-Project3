import requests
from lxml import etree
import random
import time
from tqdm import tqdm


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
    "user-agent":random.choice(user_agent),
    "Cookie": "_csrf=4dc7274086edec1a7450d85208bc743a77d9dd1a8741f92d423487af7b938b0aa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22RjAce990e08bhH_QO2HpcUzo1KcTgdvk%22%3B%7D; userId=1393031; userName=WX615acefac2cef%40aizhan.com; userGroup=1; userSecure=%2Fby3Ax9l7yxkSskfViZ3sOyQ98lkgWI%2B52aP3rD17BDvZxEK%2BUofmHKspdkbsXTXfJ9qb6SaKkHVQWhGcj50b4zGwM4%3D; userWxNickname=%E6%9C%89%E7%8C%AB%E8%85%BB",
}


def read_txt():
    list_ip = []
    with open('输入ip.txt','r',encoding='utf-8')as f:
        content = f.readlines()
    for c in content:
        ip = c.strip('\n')
        list_ip.append(ip)
    return list_ip


def parse_url(url):
    html = requests.get(url,headers=headers)
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)


def get_number():
    list_ip = read_txt()
    list_number_ip = []

    for i in list_ip:
        url = 'https://dns.aizhan.com/{}/'.format(i)
        try:
            html = requests.get(url, headers=headers)
            time.sleep(0.5)
            content = html.text
            soup = etree.HTML(content)
            number = soup.xpath("//li[@class='last']/span/text()")[0]
            number = int(number)
            numbers = int(number / 20)
            numbers = numbers + 1
            for l in range(1,numbers+1):
                url1 = 'https://dns.aizhan.com/{}/{}/'.format(i,l)
                list_number_ip.append(url1)
        except Exception as e:
            print('无效ip:{}'.format(i), e)
    return list_number_ip


def get_html(html):
    try:
        content = html.text
        soup = etree.HTML(content)
        href = soup.xpath("//td[@class='domain']/a/@href")
        for h in href:
            write_txt(h)
        time.sleep(0.2)
    except Exception as e:
        print('请过一会再试',e)



def write_txt(content):
    with open('输出文本.txt','a+',encoding='utf-8')as f:
        f.write(content+'\n')
        print('写入成功')


if __name__ == '__main__':
    list_number_ip = get_number()
    # parse_url(list_number_ip)
    for l in tqdm(list_number_ip):
        print(l)
        parse_url(l)

