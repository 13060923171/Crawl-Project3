import requests
import re
from lxml import etree
import pandas as pd
import time
from tqdm import tqdm

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "cookie": "buvid3=E2CF89BF-6527-B3A6-B394-F15D33F2308531736infoc; _uuid=E20A1724-1355-C5E9-0996-725650CABF1930288infoc; blackside_state=1; fingerprint=f0dd7150ddbbac02574da34eda3d20a9; buvid_fp=E2CF89BF-6527-B3A6-B394-F15D33F2308531736infoc; buvid_fp_plain=9344C64E-0352-41B2-BE45-24ADF19B2D50184988infoc; DedeUserID=35906556; DedeUserID__ckMd5=6bc77a6b9c4d788a; SESSDATA=b740f51b%2C1648294671%2C1aba2*91; bili_jct=d46d0f25cb390020de5387c681ee7432; rpdid=|(umR~~|Y||~0J'uYJk~Rk~uu; PVID=1; CURRENT_FNVAL=976; CURRENT_QUALITY=80; bp_video_offset_35906556=585514358681638938; video_page_version=v_old_home_18; sid=c7s0j5gv; innersign=0",
}

#长连接，就是把几个请求连接起来变成一个，防止对那个网站损害太大
session = requests.session()
session.headers = headers


def parse_url(url):
    html = session.get(url,headers=headers)
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)


def get_html(html):
    content = html.text
    href = re.compile('"arcurl":(.*?),"bvid"',re.S|re.I)
    hrefs = href.findall(content)
    for h in tqdm(hrefs):
        h = str(h)
        h = h.replace('\\','').replace('"','')
        print(h)
        get_data(h)
        time.sleep(2)


def get_data(url):
    dic1 = {}
    html = session.get(url,headers=headers)
    if html.status_code == 200:
        content = html.text
        soup = etree.HTML(content)
        #播放量
        view_count = re.compile('class="view">(.*?)播放')
        view_counts = view_count.findall(content)[0]
        # view_counts = soup.xpath("//div[@class='video-data']/span[1]/text()")[0]
        #点赞量
        give_a_like = soup.xpath("//div[@class='ops']/span[1]/text()")[0].strip('\n').replace(' ','').replace('\n','')
        #评论量
        comment_count = re.compile('"reply":(.*?),"favorite',re.S | re.I)
        comment_counts = comment_count.findall(content)[0]
        #转发量
        share_counts = soup.xpath("//div[@class='ops']/span[4]/text()")[0].strip('\n').replace(' ','').replace('\n','')
        #投币量
        insert_coins = soup.xpath("//div[@class='ops']/span[2]/text()")[0].strip('\n').replace(' ','').replace('\n','')
        #弹幕量
        bullet_screen = soup.xpath("//div[@class='video-data']/span[2]/text()")[0].strip('\n').replace(' ','').replace('\n','')
        #视频标签
        tag_name = re.compile('"tag_name":"(.*?)","cover"',re.S | re.I)
        tag_names = tag_name.findall(content)
        #视频名称
        names = re.compile('<h1 title="(.*?)" class',re.S | re.I)
        name = names.findall(content)[0]

        try:
            dic1['name'] = name
        except:
            dic1['name'] = 0

        try:
            dic1['view_counts'] = view_counts
        except:
            dic1['view_counts'] = 0

        try:
            dic1['give_a_like'] = give_a_like
        except:
            dic1['give_a_like'] = 0

        try:
            dic1['comment_counts'] = comment_counts
        except:
            dic1['comment_counts'] = 0

        try:
            dic1['share_counts'] = share_counts
        except:
            dic1['share_counts'] = 0

        try:
            dic1['insert_coins'] = insert_coins
        except:
            dic1['insert_coins'] = 0

        try:
            dic1['bullet_screen'] = bullet_screen
        except:
            dic1['bullet_screen'] = 0

        try:
            dic1['tag_names'] = tag_names
        except:
            dic1['tag_names'] = 0

        time.sleep(0.2)

    else:
        print(html.status_code)
    savefving_csv(dic1)


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

def get_url(start,end):
    sum_url = []
    for i in range(1,4):
        url = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id=201&page={}&pagesize=10&jsonp=jsonp&time_from={}&time_to={}'.format(i,start,end)
        sum_url.append(url)
    for i in range(1,4):
        url = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id=124&page={}&pagesize=10&jsonp=jsonp&time_from={}&time_to={}'.format(i,start,end)
        sum_url.append(url)
    for i in range(1,4):
        url = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id=228&page={}&pagesize=10&jsonp=jsonp&time_from={}&time_to={}'.format(i,start,end)
        sum_url.append(url)

    return sum_url


if __name__ == '__main__':
    sum_url = get_url('20210901','20210930')
    for s in sum_url:
        parse_url(s)
        time.sleep(1)


