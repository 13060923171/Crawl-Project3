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
from shujuku import COMMODITY,sess

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
    soup = etree.HTML(content)
    #视频时长
    try:
        time_length = re.findall("\"timelength\":([0-9]*),", content)[0]
        time_length = (int(time_length) / 1000) / 60
        time_length = str(time_length).split('.')
        time_length = time_length[0] + ":" + time_length[1][:2]
    except:
        time_length = ''
    #点赞，投币，收藏，转发
    video_message = soup.xpath('//div[@class="ops"]/span/text()')
    #视频标签
    try:
        fenlei = re.findall('name="keywords" content="(.*?)"><meta data-vue-meta',content)
        fenlei1 = str(fenlei[0]).split(',')
        fenlei2 = ' '.join(fenlei1[1:-4])
    except:
        fenlei2 = ''
    #视频标题
    title = soup.xpath('//div[@id="viewbox_report"]/h1/span/text()')
    #视频描述
    descrip = soup.xpath('//div[@class="desc-info desc-v2 open"]/span/text()')[0].replace('\n','')
    #视频的品质信息
    try:
        quality_message = re.findall('"accept_description":(.*?),"accept_quality"', content)[0]
    except:
        quality_message = ''

    try:
        oid = re.findall("\"aid\":([0-9]*),", content)[0]
    except:
        oid = ''

    try:
        reply = re.findall("\"reply\":([0-9]*),", content)[0]
    except:
        reply = ''

    df = pd.DataFrame()
    df['视频标题'] =title
    df['视频介绍'] =[descrip]
    df['视频时长'] = [time_length]
    df['点赞，投币，收藏，转发'] = [video_message]
    df['视频标签'] = [fenlei2]
    df['视频评论'] = [reply]
    df['视频品质'] = [quality_message]
    filename = '作业二数据存储'
    # 创建一个文件夹，如果这个文件夹不存在，那么我们就创建这个文件夹，这个是一条死语句，必须得背下来
    if not os.path.exists(filename):
        os.makedirs(filename)
    df.to_csv('./作业二数据存储/单个视频具体信息.csv')

    # #获取时间开始时间  这个对应的是爬取历史数据的弹幕，获取时间的创建时间，以及现在的时间，求出所有时间的列表
    # start_time = soup.xpath('//div[@class="video-data"]/span[3]/text()')[0].split(' ')[0]
    # end_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # date_list = [x for x in pd.date_range(start_time, end_time).strftime('%Y-%m-%d')]
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
                df1.to_csv('./作业二数据存储/评论信息表.csv',mode='a+',index=None,header=None,encoding='utf-8')
                if count >= 1:
                    replies1 = r['replies']
                    for r1 in replies1:
                        level,content,otherStyleTime,type2 = reply_clean(r1)
                        df1['评论内容'] = [content]
                        df1['评论时间'] = [otherStyleTime]
                        df1['评论人等级'] = [level]
                        df1['评论类型'] = [type2]
                        df1.to_csv('./作业二数据存储/评论信息表.csv', mode='a+', index=None, header=None, encoding='utf-8')
                else:
                    pass
                time.sleep(0.1)
        except:
            continue

#数据库存储
#获取评论信息
def shujuku_reply(oid,reply):
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
                # df1['评论内容'] = [content]
                # df1['评论时间'] = [otherStyleTime]
                # df1['评论人等级'] = [level]
                # df1['评论类型'] = [type1]
                # df1.to_csv('./作业二数据存储/评论信息表.csv',mode='a+',index=None,header=None,encoding='utf-8')
                if count >= 1:
                    replies1 = r['replies']
                    for r1 in replies1:
                        level,content,otherStyleTime,type2 = reply_clean(r1)
                        try:
                            video_data = COMMODITY(
                                comment=content,
                                play_time=otherStyleTime,
                                level=level,
                                type1=type2,
                            )
                            sess.add(video_data)
                            sess.commit()
                        except Exception as e:
                            print(e)
                            sess.rollback()
                else:
                    pass
                time.sleep(0.1)
        except:
            continue

# #获取弹幕的oid值
# def acquire_oid():
#     url1 = 'https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(BV)
#     html = requests.get(url1)
#     content = html.json()
#     oid = content['data'][0]['cid']
#     return oid


#获取弹幕信息
# def acquire_dm(date):
#     oid = acquire_oid()
#     url1 = "https://api.bilibili.com/x/v2/dm/web/history/seg.so?"
#     headers = {
#         "sec-fetch-dest": "empty",
#         "sec-fetch-mode": "cors",
#         "sec-fetch-site": "same-site",
#         "origin": "https://www.bilibili.com",
#         "cookie": "_uuid=715101066C-FAA5-D175-EA51-51071BCDDFFB928793infoc; buvid3=0D1B00B3-6F3D-4B89-AFC7-DFE562DDF14F167614infoc; b_nut=1638068729; DedeUserID=35906556; DedeUserID__ckMd5=6bc77a6b9c4d788a; video_page_version=v_old_home; blackside_state=1; CURRENT_QUALITY=0; rpdid=|(umR~~|Ykmu0J'uYJ)JYY~R); i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO1816398016892574; buvid4=C66AE545-82A9-EB40-B87C-DA9B90EDB50A31270-022013014-Vp25bGcbK8ZpT1kPMJFT9g%3D%3D; fingerprint=807b5f756ae9d19228302dac996d1efd; buvid_fp_plain=undefined; buvid_fp=f8287eb05aecbd49171ed08907b0b66d; SESSDATA=c7c7f7e4%2C1659262304%2C7c0f4%2A21; bili_jct=81d5eaa78413784a8cec20f7b076ab3c; sid=5g0611ll; bp_t_offset_35906556=629159455574008408; bp_video_offset_35906556=631834442866884617; CURRENT_BLACKGAP=0; innersign=0; b_lsid=EDFE95D7_17F55230D71; nostalgia_conf=-1; CURRENT_FNVAL=80; PVID=1",
#         'user-agent': random.choice(user_agent),
#     }
#     params = {
#         'type': 1,
#         'oid': oid,
#         'date': date
#     }
#
#     response = requests.get(url1, params=params, headers=headers)
#     print(response.text)
#     # # print(response.encoding)
#     # response.encoding = response.apparent_encoding
#     # print(response.text)
#     # # comment = re.findall('<d p=".*?">(.*?)</d>', response.text)
#     # # # print(comment)
#     # # with open('barrages.txt', 'a+') as f:
#     # #     for con in comment:
#     # #         f.write(con + '\n')
#     # # time.sleep(random.randint(1, 3))


def huifu_level():
    df2 = pd.read_csv('./作业二数据存储/评论信息表.csv')
    count = 0
    level = df2['评论人等级']
    type1 = df2['评论类型']
    for l,t in zip(level,type1):
        if str(t) == '回复' and int(l) >= 4:
            count += 1
    print('有 {} LV4+以上的账号回复'.format(count))



if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/BV1us411h7BQ?from=search&seid=9220732790560164695&spm_id_from=333.337.0.0'
    BV = 'BV1us411h7BQ'
    df1 = pd.DataFrame()
    df1['评论内容'] = ['评论内容']
    df1['评论时间'] = ['评论时间']
    df1['评论人等级'] = ['评论人等级']
    df1['评论类型'] = ['评论类型']
    df1.to_csv('./作业二数据存储/评论信息表.csv', index=None, mode='w', header=None, encoding='utf-8')
    get_parse(url)
    #获取回复等级人数
    huifu_level()
