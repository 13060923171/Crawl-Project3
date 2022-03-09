import requests
from lxml import etree
import random
import re
from urllib import parse
import pandas as pd
import time
from tqdm import tqdm
import os
import json
import datetime


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
   "cookie": "_uuid=715101066C-FAA5-D175-EA51-51071BCDDFFB928793infoc; buvid3=0D1B00B3-6F3D-4B89-AFC7-DFE562DDF14F167614infoc; b_nut=1638068729; DedeUserID=35906556; DedeUserID__ckMd5=6bc77a6b9c4d788a; video_page_version=v_old_home; blackside_state=1; CURRENT_QUALITY=0; rpdid=|(umR~~|Ykmu0J'uYJ)JYY~R); i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO1816398016892574; buvid4=C66AE545-82A9-EB40-B87C-DA9B90EDB50A31270-022013014-Vp25bGcbK8ZpT1kPMJFT9g%3D%3D; fingerprint=807b5f756ae9d19228302dac996d1efd; buvid_fp_plain=undefined; buvid_fp=f8287eb05aecbd49171ed08907b0b66d; SESSDATA=c7c7f7e4%2C1659262304%2C7c0f4%2A21; bili_jct=81d5eaa78413784a8cec20f7b076ab3c; sid=5g0611ll; bp_t_offset_35906556=629159455574008408; bp_video_offset_35906556=631834442866884617; CURRENT_BLACKGAP=0; innersign=0; b_lsid=EDFE95D7_17F55230D71; nostalgia_conf=-1; CURRENT_FNVAL=80; PVID=1",
}

#判断页面是否正常
def get_parse(url):
    html = requests.get(url,headers=headers)
    if html.status_code == 200:
        return 200,html
    else:
        return html.status_code,html


def up_content(mid):
    url = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(mid)
    status,html = get_parse(url)
    if status == 200:
        content = html.json()
        name = content['data']['name']
        sex = content['data']['sex']
        mid = content['data']['mid']
        sign = content['data']['sign']
        sign = sign.strip('\n')
        level = content['data']['level']
        title = content['data']['official']['title']
        birthday = content['data']['birthday']
        tags = content['data']['tags']
        return name,sex,mid,sign,level,title,birthday,tags
    else:
        pass

def up_video():
    url = 'https://api.bilibili.com/x/space/arc/search?mid=423895&pn=1&ps=25&index=1&jsonp=jsonp'
    status,html = get_parse(url)
    if status == 200:
        content = html.json()
        count = content['data']['page']['count']
        return count
    else:
        pass


def up_fensi():
    url = 'https://api.bilibili.com/x/relation/stat?vmid=423895&jsonp=jsonp'
    status,html = get_parse(url)
    if status == 200:
        content = html.json()
        following = content['data']['following']
        follower = content['data']['follower']
        return following,follower
    else:
        pass


def video_message():
    df1 = pd.DataFrame()
    df1['视频标题'] = ['视频标题']
    df1['创建时间'] = ['创建时间']
    df1['视频编号'] = ['视频编号']
    df1['视频时长'] = ['视频时长']
    df1['播放量'] = ['播放量']
    df1['视频弹幕'] = ['视频弹幕']
    df1['视频评论'] = ['视频评论']
    df1.to_csv('./作业三数据存储/视频信息.csv', mode='w', header=None, index=None, encoding='utf-8')
    page = int(int(count) / 30) + 1
    for i in tqdm(range(1, int(page)+1)):
        url = 'https://api.bilibili.com/x/space/arc/search?mid=423895&ps=30&tid=0&pn={}&keyword=&order=pubdate&jsonp=jsonp'.format(i)
        status, html = get_parse(url)
        if status == 200:
            content = html.json()
            data = content['data']['list']['vlist']
            for d in data:
                try:
                    title = d['title']
                    created = d['created']
                    bvid = d['bvid']
                    length = d['length']
                    play = d['play']
                    video_review = d['video_review']
                    comment = d['comment']
                    df1['视频标题'] = [title]
                    df1['创建时间'] = [created]
                    df1['视频编号'] = [bvid]
                    df1['视频时长'] = [length]
                    df1['播放量'] = [play]
                    df1['视频弹幕'] = [video_review]
                    df1['视频评论'] = [comment]
                    df1.to_csv('./作业三数据存储/视频信息.csv', mode='a+', header=None, index=None, encoding='utf-8')
                    time.sleep(0.1)
                except Exception as e:
                    pass
        else:
            pass


# def fensi_number():
#     page = int(int(follower) / 20) + 1
#     for i in tqdm(range(1, int(page) + 1)):
#         url = 'https://api.bilibili.com/x/relation/followers?vmid={}&pn={}&ps=20&order=desc&jsonp=jsonp&callback=__jp9'.format(mid,i)
#         status, html = get_parse(url)
#         if status == 200:
#             content = html.json()
#             data = content['data']['list']
#             for d in data:
#                 mid = d['mid']
#                 name, sex, mid, sign, level, title, birthday, tags = up_content(mid)
#                 #剩下就是数据写入部分
#         else:
#             pass


def shujutiqu():
    df2 = pd.read_csv('./作业三数据存储/视频信息.csv')
    df2['时间'] = pd.to_datetime(df2['创建时间'],unit='s')
    df2['数量'] = 1
    df2.index = df2['时间']
    df3 = df2.resample('Y').sum()
    print(df3)
    df3 = df3.drop(['创建时间'],axis=1)
    df3.columns = ['总播放量','总弹幕量','总评论量','总数量']
    df3.to_excel('./作业三数据存储/所有视频的基本信息.xlsx')


if __name__ == '__main__':
    mid = 423895
    name,sex,mid,sign,level,title,birthday,tags = up_content(mid)
    count = up_video()
    following,follower = up_fensi()
    df = pd.DataFrame()
    df['up主名称'] = [name]
    df['up主mid'] = [mid]
    df['up主性别'] = [sex]
    df['up主等级'] = [level]
    df['up主生日'] = [birthday]
    df['up主签名'] = [sign]
    df['up主头衔'] = [title]
    df['up主标签'] = [tags]
    df['up主视频数量'] = count
    df['up主关注人数'] = following
    df['up主粉丝数量'] = follower
    filename = '作业三数据存储'
    # 创建一个文件夹，如果这个文件夹不存在，那么我们就创建这个文件夹，这个是一条死语句，必须得背下来
    if not os.path.exists(filename):
        os.makedirs(filename)
    df.to_csv('./作业三数据存储/up主基本信息.csv')
    video_message()
    shujutiqu()