import requests
from lxml import etree
import random
import re
import pandas as pd
import time
from tqdm import tqdm
import os


#构建请求头,反爬策略
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
    #随机请求反爬策略
    'user-agent': random.choice(user_agent),
    # #到时候替换成你自己的
    "cookie": "_uuid=DE95E435-8C4C-4C3F-93A1-57DB808F829530580infoc; buvid3=E2B1C11B-A111-4692-B768-316E8429C7E018547infoc; blackside_state=1; rpdid=|(um||k))uYu0J'uYuR)JJkkm; DedeUserID=35906556; DedeUserID__ckMd5=6bc77a6b9c4d788a; CURRENT_QUALITY=80; video_page_version=v_old_home_18; b_ut=5; i-wanna-go-back=2; CURRENT_BLACKGAP=1; buvid4=D11C438E-7E71-9149-BB6D-0538D117546D12889-022012415-zVIpBdzth4rj3vTAGCv+5g%3D%3D; fingerprint=d96f31db386a48ede8037178b7423708; buvid_fp_plain=undefined; buvid_fp=6749d91e28e011ed31c760585f0c4654; SESSDATA=b84ce533%2C1658912417%2C8b4dd%2A11; bili_jct=76828d7371c276234de273cf1115b07b; sid=iamn2302; CURRENT_FNVAL=4048; bp_t_offset_35906556=626917796178323786; PVID=2; bp_video_offset_35906556=626940769954340072; b_lsid=A479DAD7_17EF6F24AC4; bsource=search_google; innersign=0",
}

def get_parse(url):
    #请求网页
    html = requests.get(url,headers=headers)
    # 请求网页查看是否为200，200说明网页正常，进行下去
    if html.status_code == 200:
        get_html(html)
    #否则返回状态码
    else:
        print(html.status_code)


def get_html(html):
    content = html.json()
    try:
        replies = content['data']['replies']
        for reply in replies:
            mid = reply['member']['mid']
            sex = reply['member']['sex']
            vip = reply['member']['vip']['vipStatus']
            df1['mid'] = [mid]
            df1['sex'] = [sex]
            df1['vip'] = [vip]
            df1.to_csv('./data/{}.csv'.format(name),mode='a+',header=None,index=None)
    except:
        pass


if __name__ == '__main__':
    df = pd.read_excel('top100.xlsx').iloc[3:,:]
    number = df['评论数']
    oid = df['评论oid']

    for n,o in tqdm(zip(number,oid)):
        name = o
        page = int(n / 20) + 1
        df1 = pd.DataFrame()
        df1['mid'] = ['mid']
        df1['sex'] = ['sex']
        df1['vip'] = ['vip']
        df1.to_csv('./data/{}.csv'.format(name), mode='w', header=None, index=None)
        for i in range(1,int(page)):
            try:
                url = 'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={}&type=1&oid={}&mode=3&plat=1'.format(i,o)
                get_parse(url)
                time.sleep(0.2)
            except:
                continue
        time.sleep(300)