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
def get_parse(url,data):
    html = requests.get(url,headers=headers,params=data)
    if html.status_code == 200:
        return 200,html
    else:
        return html.status_code,html

#获取视频的总页数
def video_number():
    data = {
        "__refresh__": "true",
        "_extra":None,
        "context":None,
        "page": 1,
        "page_size": 42,
        "from_source": None,
        "from_spmid": 333.337,
        "platform": "pc",
        "highlight": 1,
        "single_column": 0,
        "keyword": keyword,
        "category_id":None,
        "search_type": "video",
        "dynamic_offset": 0,
        "preload": "true",
        "com2co": "true",
    }
    url = "https://api.bilibili.com/x/web-interface/search/type?"
    status,html = get_parse(url,data)
    if status == 200:
        content = html.json()
        #视频页数
        numPages = content['data']['numPages']
        video_content(numPages)
    else:
        return '视频参数错误，请检查'


#获取每个视频的基本信息
def video_content(numPages):
    for n in tqdm(range(1,int(numPages)+1)):
        data = {
            "__refresh__": "true",
            "_extra": None,
            "context": None,
            "page": n,
            "page_size": 42,
            "from_source": None,
            "from_spmid": 333.337,
            "platform": "pc",
            "highlight": 1,
            "single_column": 0,
            "keyword": keyword,
            "category_id": None,
            "search_type": "video",
            "dynamic_offset": 0,
            "preload": "true",
            "com2co": "true",
        }
        url = "https://api.bilibili.com/x/web-interface/search/type?"
        status, html = get_parse(url, data)
        if status == 200:
            content = html.json()
            # 搜索内容
            result = content['data']['result']
            for r in result:
                try:
                    #视频名称
                    title = r['title']
                    title1 = re.sub(r'<em.*?</em>','',title)
                    # 视频时长
                    duration = r['duration']
                    # 作者名称
                    author = r['author']
                    # 视频播放量
                    play = r['play']
                    # 视频弹幕数量
                    video_review = r['video_review']
                    # 视频评论数量
                    review = r['review']
                    df['标题'] = [title1]
                    df['时长'] = [duration]
                    df['作者名称'] = [author]
                    df['播放量'] = [play]
                    df['弹幕信息'] = [video_review]
                    df['评论数'] = [review]
                    df.to_csv('./作业一数据存储/{}_相关信息.csv'.format(keyword), mode='a+', header=None, index=None, encoding='utf-8')
                    time.sleep(0.1)
                except Exception as e:
                    pass
        else:
            return '视频参数错误，请检查'


def type_number(type):
    data = {
        "__refresh__": "true",
        "_extra": None,
        "context": None,
        "page": 1,
        # "page_size": 12,
        "from_source": None,
        "from_spmid": 333.337,
        "platform": "pc",
        "highlight": 1,
        "single_column": 0,
        "keyword": keyword,
        "category_id": None,
        "search_type": type,
        "preload": "true",
        "com2co": "true",
    }
    url = "https://api.bilibili.com/x/web-interface/search/type?"
    status, html = get_parse(url, data)
    if status == 200:
        content = html.json()
        # 视频总数量
        if type == 'live':
            numResults = content['data']['pageinfo']['live_room']['total']
            return numResults
        else:
            numResults = content['data']['numResults']
            return numResults
    else:
        return '视频参数错误，请检查'


def type_sum():
    number_sum = []
    list_type = ['video', 'media_bangumi', 'media_ft', 'live', 'article', 'topic', 'bili_user']
    name = ['视频','番剧','影视','直播','专栏','话题','用户']
    for l in list_type:
        number = type_number(l)
        number_sum.append(number)

    filename = '作业一数据存储'
    # 创建一个文件夹，如果这个文件夹不存在，那么我们就创建这个文件夹，这个是一条死语句，必须得背下来
    if not os.path.exists(filename):
        os.makedirs(filename)
    df1 = pd.DataFrame()
    df1['内容名称'] = name
    df1['对应数量'] = number_sum
    df1.to_csv('./作业一数据存储/{}_相关内容数量统计.csv'.format(keyword),encoding='utf-8')


def zlshuju():
    df2 = pd.read_csv('./作业一数据存储/fate_相关信息.csv')
    print(df2)
if __name__ == '__main__':
    # keyword = parse.quote('fate')
    # type_sum()
    #
    # df = pd.DataFrame()
    # df['标题'] = ['标题']
    # df['时长'] = ['时长']
    # df['作者名称'] = ['作者名称']
    # df['播放量'] = ['播放量']
    # df['弹幕信息'] = ['弹幕信息']
    # df['评论数'] = ['评论数']
    # df.to_csv('./作业一数据存储/{}_相关信息.csv'.format(keyword),mode='w',header=None,index=None,encoding='utf-8')
    # video_number()
    zlshuju()

