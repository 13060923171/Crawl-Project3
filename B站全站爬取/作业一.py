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
    # "origin": "https://search.bilibili.com",
   "cookie": "buvid3=9AD7946F-F104-C53A-D57D-B9A1ED199C3F38237infoc; i-wanna-go-back=-1; _uuid=4447FCCE-10D48-A6E5-2F4C-AA3EF101DC33D38615infoc; buvid4=6B686B1D-6309-A6D5-737A-DCD4BBB5CB1E39359-022032919-3B5Gb3RqLY4lnqUyS/geHw%3D%3D; nostalgia_conf=-1; CURRENT_BLACKGAP=0; rpdid=|(um|kmkJ|~Y0J'uYR)llk~~u; buvid_fp_plain=undefined; hit-dyn-v2=1; LIVE_BUVID=AUTO7416505258571664; fingerprint=02a51db82bc114addf42e55b5ecb25f7; SESSDATA=ef45abfa%2C1666519854%2Ce3696%2A41; bili_jct=8e1e9744710c8e39c611f3c282c5e945; DedeUserID=35906556; DedeUserID__ckMd5=6bc77a6b9c4d788a; sid=l5g3nk8n; buvid_fp=02a51db82bc114addf42e55b5ecb25f7; CURRENT_QUALITY=80; b_ut=5; PVID=1; blackside_state=0; b_lsid=8C2FDC76_181F1129711; bsource=share_source_copy_link; bp_video_offset_35906556=681897226011672601; innersign=1; b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_9AD7946F%22%3A%22181F1129E51%22%2C%22333.337.fp.risk_9AD7946F%22%3A%22181F112EEB4%22%2C%22333.788.fp.risk_9AD7946F%22%3A%22181F11F8FAA%22%2C%22333.999.fp.risk_9AD7946F%22%3A%22181F11A6563%22%2C%22333.880.fp.risk_9AD7946F%22%3A%22181F043BCC0%22%7D%7D; CURRENT_FNVAL=80",
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
        "keyword": name,
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
    for n in tqdm(range(1,int(numPages)+5)):
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
            "keyword": name,
            "category_id": None,
            "search_type": "video",
            "dynamic_offset": int((n-1) * 36),
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
                    danmaku = r['danmaku']
                    # 视频评论数量
                    review = r['review']
                    # 视频链接
                    url = r['arcurl']
                    # 收藏数量
                    favorites = r['favorites']
                    # 点赞
                    like = r['like']
                    # 标签
                    tag = r['tag']
                    # 时间戳
                    pubdate = r['pubdate']

                    is_pay = r['is_pay']
                    is_union_video = r['is_union_video']
                    timeArray = time.localtime(pubdate)
                    timedate = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


                    df['发布时间'] = [timedate]
                    df['视频链接'] = [url]
                    df['标题'] = [title1]
                    df['时长'] = [duration]
                    df['作者名称'] = [author]
                    df['播放量'] = [play]
                    df['评论数'] = [review]
                    df['弹幕数'] = [danmaku]
                    df['点赞'] = [like]
                    df['收藏'] = [favorites]
                    df['标签'] = [tag]
                    df['1'] = [is_pay]
                    df['2'] = [is_union_video]
                    df.to_csv('./作业一数据存储/{}_相关信息.csv'.format(name), mode='a+', header=None, index=None, encoding='utf-8-sig')
                    time.sleep(0.1)
                except Exception as e:
                    pass
        else:
            return '视频参数错误，请检查'


if __name__ == '__main__':
    name = '王者荣耀'
    keyword = parse.quote('王者荣耀')
    df = pd.DataFrame()
    df['发布时间'] = ['发布时间']
    df['视频链接'] = ['视频链接']
    df['标题'] = ['标题']
    df['时长'] = ['时长']
    df['作者名称'] = ['作者名称']
    df['播放量'] = ['播放量']
    df['评论数'] = ['评论数']
    df['弹幕数'] = ['弹幕数']
    df['点赞'] = ['点赞']
    df['收藏'] = ['收藏']
    df['标签'] = ['标签']
    df['1'] = ['1']
    df['2'] = ['2']
    df.to_csv('./作业一数据存储/{}_相关信息.csv'.format(name),mode='w',header=None,index=None,encoding='utf-8-sig')
    video_number()


