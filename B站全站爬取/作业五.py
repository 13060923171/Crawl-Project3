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


session = requests.session()
session.headers = headers


def get_parse(url):
    #请求网页
    html = session.get(url)
    # 请求网页查看是否为200，200说明网页正常，进行下去
    if html.status_code == 200:
        xx_coment(html)
    #否则返回状态码
    else:
        print(html.status_code)


def xx_coment(html):
    #获取源码
    content = html.text
    # 把数据源替换成xpath语法能读取到的数据
    try:
        oid = re.findall("\"aid\":([0-9]*),", content)[0]
    except:
        oid = ''

    try:
        reply = re.findall("\"reply\":([0-9]*),", content)[0]
    except:
        reply = ''

    acquire_reply(oid,reply)



#爬二级评论
def reply_clean(reply):
    level = reply['member']['level_info']['current_level']  # 等级
    content = reply['content']['message'].replace("\n", "")  # 评论内容
    t = reply['ctime']
    timeArray = time.localtime(t)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)  # 评论时间，时间戳转为标准时间格式
    return level,content,otherStyleTime,'回复'


#获取评论信息
def acquire_reply(oid,reply):
    page = int(int(reply) / 20) + 1
    for i in tqdm(range(1, int(page))):
        try:
            url = 'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={}&type=1&oid={}&mode=3&plat=1'.format(i,oid)
            html = session.get(url, headers=headers)
            content = html.json()
            replies = content['data']['replies']
            for r in replies:
                count = r['count']
                content = r['content']['message'].replace("\n", "")
                level = r['member']['level_info']['current_level']  # 等级
                t = r['ctime']
                timeArray = time.localtime(t)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)  # 评论时间，时间戳转为标准时间格式

                type1 = '评论'
                df1['评论内容'] = [content]
                df1['评论时间'] = [otherStyleTime]
                df1['评论人等级'] = [level]
                df1['评论类型'] = [type1]

                df1.to_csv('./作业五数据存储/评论信息表.csv',mode='a+',index=None,header=None,encoding='utf-8')
                if count >= 1:
                    replies1 = r['replies']
                    for r1 in replies1:
                        level,content,otherStyleTime,type2 = reply_clean(r1)
                        df1['评论内容'] = [content]
                        df1['评论时间'] = [otherStyleTime]
                        df1['评论人等级'] = [level]
                        df1['评论类型'] = [type2]
                        df1.to_csv('./作业五数据存储/评论信息表.csv', mode='a+', index=None, header=None, encoding='utf-8')
                else:
                    pass
                time.sleep(0.2)
        except:
            continue


if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/BV1yt4y1Q7SS?spm_id_from=333.999.0.0'
    BV = 'BV1yt4y1Q7SS'
    filename = '作业五数据存储'
    # 创建一个文件夹，如果这个文件夹不存在，那么我们就创建这个文件夹，这个是一条死语句，必须得背下来
    if not os.path.exists(filename):
        os.makedirs(filename)
    df1 = pd.DataFrame()
    # df1['评论内容'] = ['评论内容']
    # df1['评论时间'] = ['评论时间']
    # df1['评论人等级'] = ['评论人等级']
    # df1['评论类型'] = ['评论类型']
    # df1.to_csv('./作业五数据存储/评论信息表.csv', index=None, mode='w', header=None, encoding='utf-8')
    get_parse(url)

