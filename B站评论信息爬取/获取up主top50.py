import requests
from lxml import etree
import random
import re
from urllib import parse
import pandas as pd
import time
from tqdm import tqdm
import os
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
    "origin": "https://search.bilibili.com",
#     "cookie": "_uuid=DE95E435-8C4C-4C3F-93A1-57DB808F829530580infoc; buvid3=E2B1C11B-A111-4692-B768-316E8429C7E018547infoc; blackside_state=1; rpdid=|(um||k))uYu0J'uYuR)JJkkm; DedeUserID=35906556; DedeUserID__ckMd5=6bc77a6b9c4d788a; CURRENT_QUALITY=80; video_page_version=v_old_home_18; b_ut=5; i-wanna-go-back=2; CURRENT_BLACKGAP=1; buvid4=D11C438E-7E71-9149-BB6D-0538D117546D12889-022012415-zVIpBdzth4rj3vTAGCv+5g%3D%3D; fingerprint=d96f31db386a48ede8037178b7423708; buvid_fp_plain=undefined; buvid_fp=6749d91e28e011ed31c760585f0c4654; SESSDATA=b84ce533%2C1658912417%2C8b4dd%2A11; bili_jct=76828d7371c276234de273cf1115b07b; sid=iamn2302; CURRENT_FNVAL=4048; bp_t_offset_35906556=626917796178323786; PVID=2; bp_video_offset_35906556=626940769954340072; b_lsid=A479DAD7_17EF6F24AC4; bsource=search_google; innersign=0",
 }


def get_parse(url):
    html = requests.get(url,headers=headers)
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)
#上面的都和第一个文件的含义一样

def get_html(html):
    #这个是把数据源转换为json的格式，方便后续进行定位
    content = html.json()
    #获取结果值
    result = content['data']['result']
    #获取名字
    name = result[0]['uname']
    #获取uid
    uid = result[0]['mid']
    #获取粉丝数
    fans = result[0]['fans']
    df['up名称'] = [name]
    df['up-uid'] = [uid]
    df['up粉丝数'] = [fans]
    #把数据保存为csv格式文件
    df.to_csv('up-top100.csv', mode='a+', encoding='utf-8', header=None, index=None)

def readcsv():
    #读取获取好的数据
    df1 = pd.read_csv('up-top100.csv',encoding='utf-8')
    #按照粉丝数进行排序，从大到小
    df1 = df1.sort_values(by=['up粉丝数'], ascending=False)
    #清理多余的数据，保存前50名up主的数据
    df1 = df1.iloc[0:50,:]
    #保存文件，进行编码转换
    df1.to_excel('up-top50.xlsx',index=None)
   #清除多余的数据
    os.remove('up-top100.csv')

if __name__ == '__main__':
    df = pd.DataFrame()
    df['up名称'] = ['up名称']
    df['up-uid'] = ['up-uid']
    df['up粉丝数'] = ['up粉丝数']
    df.to_csv('up-top100.csv', mode='w', encoding='utf-8', header=None, index=None)
    #读取去年2021年排名前100的up主名字
    with open('up.txt','r')as f:
        name_list = f.readlines()
    #对这些up主进行重新获取它们的粉丝数
    for n in tqdm(name_list):
        n1 = n.strip('\n')
        #把中文名转换为计算机看得到的编码
        keyword = parse.quote(n1)
        url = 'https://api.bilibili.com/x/web-interface/search/type?context=&search_type=bili_user&page=1&order=&keyword={}&category_id=&user_type=&order_sort=&changing=mid&__refresh__=true&_extra=&highlight=1&single_column=0'.format(keyword)
        get_parse(url)
        time.sleep(0.2)
    readcsv()