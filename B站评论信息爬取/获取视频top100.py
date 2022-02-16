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
    "referer": "https://www.bilibili.com/",
    # #到时候替换成你自己的
    "cookie": "_uuid=DE95E435-8C4C-4C3F-93A1-57DB808F829530580infoc; buvid3=E2B1C11B-A111-4692-B768-316E8429C7E018547infoc; blackside_state=1; rpdid=|(um||k))uYu0J'uYuR)JJkkm; DedeUserID=35906556; DedeUserID__ckMd5=6bc77a6b9c4d788a; CURRENT_QUALITY=80; video_page_version=v_old_home_18; b_ut=5; i-wanna-go-back=2; CURRENT_BLACKGAP=1; buvid4=D11C438E-7E71-9149-BB6D-0538D117546D12889-022012415-zVIpBdzth4rj3vTAGCv+5g%3D%3D; fingerprint=d96f31db386a48ede8037178b7423708; buvid_fp_plain=undefined; buvid_fp=6749d91e28e011ed31c760585f0c4654; SESSDATA=b84ce533%2C1658912417%2C8b4dd%2A11; bili_jct=76828d7371c276234de273cf1115b07b; sid=iamn2302; CURRENT_FNVAL=4048; bp_t_offset_35906556=626917796178323786; PVID=2; bp_video_offset_35906556=626940769954340072; b_lsid=A479DAD7_17EF6F24AC4; bsource=search_google; innersign=0",
}


session = requests.session()
session.headers = headers

def get_parse(url):
    #请求网页
    html = session.get(url)
    # 请求网页查看是否为200，200说明网页正常，进行下去
    if html.status_code == 200:
        get_html(html)
    #否则返回状态码
    else:
        print(html.status_code)


def get_html(html):
    #获取数据源
    content = html.text
    #把数据源替换成xpath语法能读取到的数据
    soup = etree.HTML(content)
    #进行定位，定位到请求连接，后面要用到
    href = soup.xpath('//div[@class="info"]/a/@href')
    #进行定位，获取视频标题
    title = soup.xpath('//div[@class="info"]/a/text()')
    #进行定位，获取up主的名称
    name = soup.xpath('//div[@class="detail"]/a/span/text()')
    #循环获取到内容，zip是用于多个列表一起循环时使用的
    for h,n,t in tqdm(zip(href,name,title)):
        #构造视频主页面
        url1 = 'https:' + h
        #对名字进行清洗，删除多余字符
        n = str(n).strip('\n').strip(' ').replace('\n','')
        #传入到下一个函数里面
        xx_coment(url1,n,t)
        #停顿0.2秒
        time.sleep(0.2)


def xx_coment(url,name,title):
    #对上面获取到的URL进行请求
    html = session.get(url)
    #获取源码
    content = html.text
    # 把数据源替换成xpath语法能读取到的数据
    soup = etree.HTML(content)
    #加入防错机制，防止程序出错，导致停运
    try:
        #获取粉丝数
        number = soup.xpath('//div[@class="default-btn follow-btn btn-transition b-gz not-follow"]/span/span/text()')[0]
        number = str(number).strip('\n').strip(' ')
    except:
        #如果粉丝数获取不到，则返回空值
        number = ''
    try:
        #获取uid，这里采用的是正则表达式，因为xpath语法获取不了，只能用正则进行定位
        uid = re.findall("\"mid\":([0-9]*),", content)[0]
        uid = str(uid).strip('\n').strip(' ')
    except:
        uid = ''
    try:
        fenlei = re.findall('name="keywords" content="(.*?)"><meta data-vue-meta',content)
        fenlei1 = str(fenlei[0]).split(',')
        fenlei2 = ' '.join(fenlei1[1:-4])
    except:
        fenlei2 = ''
    try:
        oid = re.findall("\"aid\":([0-9]*),", content)[0]
    except:
        oid = ''
    count = pl_number(oid)
    print(title,name,uid,number)
    #最后根据上面获取到的内容，保存到CSV文件里面
    df['标题'] = [title]
    df['up名称'] = [name]
    df['up-uid'] = [uid]
    df['up粉丝数'] = [number]
    df['分类'] = [fenlei2]
    df['评论数'] = [count]
    df['url'] = [url]
    df['评论oid'] = [oid]
    df.to_csv('top100.csv', mode='a+', encoding='utf-8', header=None,index=None)


def pl_number(oid):
    url1 = 'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=2&type=1&oid={}&mode=3&plat=1'.format(oid)
    html = session.get(url1)
    content = html.text
    try:
        count = re.findall("\"all_count\":([0-9]*),", content)[0]
    except:
        count = ''
    return count

if __name__ == '__main__':
    #top100的URL
    url = 'https://www.bilibili.com/v/popular/rank/all'
    #创建dataframe格式文件，用于保存数据
    df = pd.DataFrame()
    #构建请求头
    df['标题'] = ['标题']
    df['up名称'] = ['up名称']
    df['up-uid'] = ['up-uid']
    df['up粉丝数'] = ['up粉丝数']
    df['分类'] = ['分类']
    df['评论数'] = ['评论数']
    df['url'] = ['url']
    df['评论oid'] = ['评论oid']
    df.to_csv('top100.csv', mode='w', encoding='utf-8', header=None,index=None)
    get_parse(url)
    #最后把获取好的数据，进行格式转换，把utf-8转换为gbk格式
    df1 = pd.read_csv('top100.csv', encoding='utf-8')
    df1.to_excel('top100.xlsx',index=None)
    #删除多余数据
    os.remove('top100.csv')