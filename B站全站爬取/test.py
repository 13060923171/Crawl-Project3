import requests
import re
from lxml import etree
import pandas as pd
import time
import random
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
    'user-agent': random.choice(user_agent),
    # "origin": "https://search.bilibili.com",
   "cookie": "buvid3=9AD7946F-F104-C53A-D57D-B9A1ED199C3F38237infoc; i-wanna-go-back=-1; _uuid=4447FCCE-10D48-A6E5-2F4C-AA3EF101DC33D38615infoc; buvid4=6B686B1D-6309-A6D5-737A-DCD4BBB5CB1E39359-022032919-3B5Gb3RqLY4lnqUyS/geHw%3D%3D; nostalgia_conf=-1; CURRENT_BLACKGAP=0; rpdid=|(um|kmkJ|~Y0J'uYR)llk~~u; buvid_fp_plain=undefined; hit-dyn-v2=1; LIVE_BUVID=AUTO7416505258571664; fingerprint=02a51db82bc114addf42e55b5ecb25f7; SESSDATA=ef45abfa%2C1666519854%2Ce3696%2A41; bili_jct=8e1e9744710c8e39c611f3c282c5e945; DedeUserID=35906556; DedeUserID__ckMd5=6bc77a6b9c4d788a; sid=l5g3nk8n; buvid_fp=02a51db82bc114addf42e55b5ecb25f7; CURRENT_QUALITY=80; b_ut=5; PVID=1; blackside_state=0; b_lsid=8C2FDC76_181F1129711; bsource=share_source_copy_link; bp_video_offset_35906556=681897226011672601; innersign=1; b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_9AD7946F%22%3A%22181F1129E51%22%2C%22333.337.fp.risk_9AD7946F%22%3A%22181F112EEB4%22%2C%22333.788.fp.risk_9AD7946F%22%3A%22181F11F8FAA%22%2C%22333.999.fp.risk_9AD7946F%22%3A%22181F11A6563%22%2C%22333.880.fp.risk_9AD7946F%22%3A%22181F043BCC0%22%7D%7D; CURRENT_FNVAL=80",
}

#长连接，就是把几个请求连接起来变成一个，防止对那个网站损害太大
session = requests.session()
session.headers = headers


def get_data(url):
    dic1 = {}
    html = session.get(url,headers=headers)
    if html.status_code == 200:
        content = html.text
        soup = etree.HTML(content)
        number = soup.xpath('//div[@class="bilibili-player-video-sendbar bilibili-player-normal-mode"]/div/div[1]/text()')
        print(number)
        like = soup.xpath('//div[@class="toolbar-left"]/span[1]/span/text()')
        toubi = soup.xpath('//div[@class="toolbar-left"]/span[2]/span/text()')
        shoucan = soup.xpath('//div[@class="toolbar-left"]/span[3]/span/text()')
        zhuangfa = soup.xpath('//div[@class="toolbar-left"]/span[4]/span/text()')
        print(like)
        print(toubi)
        print(shoucan)
        print(zhuangfa)
        # #播放量
        # view_count = re.compile('class="view">(.*?)播放')
        # view_counts = view_count.findall(content)[0]
        # print(view_counts)
        # view_counts = soup.xpath("//div[@class='video-data']/span[1]/text()")[0]
    #     #点赞量
    #     give_a_like = soup.xpath("//div[@class='ops']/span[1]/text()")[0].strip('\n').replace(' ','').replace('\n','')
    #     print(give_a_like)
    #     #评论量
    #     comment_count = re.compile('"reply":(.*?),"favorite',re.S | re.I)
    #     comment_counts = comment_count.findall(content)[0]
    #     #转发量
    #     share_counts = soup.xpath("//div[@class='ops']/span[4]/text()")[0].strip('\n').replace(' ','').replace('\n','')
    #     #投币量
    #     insert_coins = soup.xpath("//div[@class='ops']/span[2]/text()")[0].strip('\n').replace(' ','').replace('\n','')
    #     #弹幕量
    #     bullet_screen = soup.xpath("//div[@class='video-data']/span[2]/text()")[0].strip('\n').replace(' ','').replace('\n','')
    #     #视频标签
    #     tag_name = re.compile('"tag_name":"(.*?)","cover"',re.S | re.I)
    #     tag_names = tag_name.findall(content)
    #     #视频名称
    #     names = re.compile('<h1 title="(.*?)" class',re.S | re.I)
    #     name = names.findall(content)[0]
    #
    #     try:
    #         dic1['name'] = name
    #     except:
    #         dic1['name'] = 0
    #
    #     try:
    #         dic1['view_counts'] = view_counts
    #     except:
    #         dic1['view_counts'] = 0
    #
    #     try:
    #         dic1['give_a_like'] = give_a_like
    #     except:
    #         dic1['give_a_like'] = 0
    #
    #     try:
    #         dic1['comment_counts'] = comment_counts
    #     except:
    #         dic1['comment_counts'] = 0
    #
    #     try:
    #         dic1['share_counts'] = share_counts
    #     except:
    #         dic1['share_counts'] = 0
    #
    #     try:
    #         dic1['insert_coins'] = insert_coins
    #     except:
    #         dic1['insert_coins'] = 0
    #
    #     try:
    #         dic1['bullet_screen'] = bullet_screen
    #     except:
    #         dic1['bullet_screen'] = 0
    #
    #     try:
    #         dic1['tag_names'] = tag_names
    #     except:
    #         dic1['tag_names'] = 0
    #
    #     time.sleep(0.2)
    #
    # else:
    #     print(html.status_code)
    # savefving_csv(dic1)


def savefving_csv(dic1):
    df = pd.DataFrame()
    df['名字'] = [dic1['name']]
    df['播放量'] = [dic1['view_counts']]
    df['点赞量'] = [dic1['give_a_like']]
    df['评论量'] = [dic1['comment_counts']]
    df['转发量'] = [dic1['share_counts']]
    df['投币量'] = [dic1['insert_coins']]
    df['弹幕量'] = [dic1['bullet_screen']]
    df['视频标签'] = [dic1['tag_names']]

    df.to_csv('知识.csv',mode='a+',index=None,header=None,encoding='utf-8')


if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/BV1VJ411Q766?p=6&spm_id_from=pageDriver&vd_source=e9269baccd81f93d19c615cd57b2b36c'
    get_data(url)


