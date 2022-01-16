import requests
from lxml import etree
import time
import random
import re

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
    'user-agent': random.choice(user_agent),
    "Cookie": "login_sid_t=938e3b4deddae4f9c75e5358df3ff279; cross_origin_proto=SSL; _s_tentry=www.google.com; UOR=www.google.com,weibo.com,www.google.com; Apache=1903674588878.3147.1642225343191; SINAGLOBAL=1903674588878.3147.1642225343191; ULV=1642225343195:1:1:1:1903674588878.3147.1642225343191:; ALF=1673761372; SSOLoginState=1642225377; SUB=_2A25M5i6ODeRhGeNN6lsS-CrJyz-IHXVvkgdGrDV8PUNbmtAKLWXSkW9NSdnQVCKI5IvfARMe1l0m8HlmLsJ1Sym3; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5GwlB4mf13pUNVQ0MzU9ZV5JpX5KzhUgL.Fo-0eK.01hBfehe2dJLoIEBLxKqL1-eL1h.LxKML12eLB-zLxKnL1h-LB.zLxK-LBKqL1Kqt; wvr=6; webim_unReadCount=%7B%22time%22%3A1642225557545%2C%22dm_pub_total%22%3A4%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A38%2C%22msgbox%22%3A0%7D; WBStorage=09a9c7be|undefined",
    "Host": "s.weibo.com",
}

session = requests.session()
session.headers = headers

def status_url(url):
    html = session.get(url)
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)


def get_html(html):
    content = html.text
    comment_urls = re.compile('<a href="(.*?)" target="_blank"')
    comment_url = comment_urls.findall(content)
    for c in comment_url:
        if 'refer_flag' in c and 'class' not in c and "L" in c and 'href' not in c:
            url1 = "https:" + c + "&type=comment"
            print(url1)
            comment_text(url1)
            a = random.random()
            time.sleep(a)


def comment_text(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        "Cookie": "login_sid_t=938e3b4deddae4f9c75e5358df3ff279; cross_origin_proto=SSL; _s_tentry=www.google.com; UOR=www.google.com,weibo.com,www.google.com; Apache=1903674588878.3147.1642225343191; SINAGLOBAL=1903674588878.3147.1642225343191; ULV=1642225343195:1:1:1:1903674588878.3147.1642225343191:; ALF=1673761372; SSOLoginState=1642225377; SUB=_2A25M5i6ODeRhGeNN6lsS-CrJyz-IHXVvkgdGrDV8PUNbmtAKLWXSkW9NSdnQVCKI5IvfARMe1l0m8HlmLsJ1Sym3; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5GwlB4mf13pUNVQ0MzU9ZV5JpX5KzhUgL.Fo-0eK.01hBfehe2dJLoIEBLxKqL1-eL1h.LxKML12eLB-zLxKnL1h-LB.zLxK-LBKqL1Kqt; wvr=6; webim_unReadCount=%7B%22time%22%3A1642225557545%2C%22dm_pub_total%22%3A4%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A38%2C%22msgbox%22%3A0%7D; WBStorage=09a9c7be|undefined",
    }
    html = requests.get(url,headers=headers)
    content = html.json()
    print(content)


if __name__ == '__main__':
    # url = 'https://s.weibo.com/weibo?q=EDG%E5%A4%BA%E5%86%A0&xsort=hot&suball=1&Refer=g&page=1'
    # status_url(url)
    url1 = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4725148656339791&root_comment_max_id=140918602237235&root_comment_max_id_type=0&root_comment_ext_param=&page=2&filter=hot&sum_comment_number=26&filter_tips_before=0&from=singleWeiBo&__rnd=1642229015358'
    comment_text(url1)