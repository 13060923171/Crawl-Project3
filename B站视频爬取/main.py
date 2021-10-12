import requests
import random
from lxml import etree
from urllib.parse import quote
import os
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
    "user-agent":random.choice(user_agent),
    "referer": "https://www.bilibili.com/",
    "cookie": "_uuid=DE95E435-8C4C-4C3F-93A1-57DB808F829530580infoc; buvid3=E2B1C11B-A111-4692-B768-316E8429C7E018547infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(um||k))uYu0J'uYuR)JJkkm; fingerprint=1211965a971db090bbca7833362e2fa0; buvid_fp=E2B1C11B-A111-4692-B768-316E8429C7E018547infoc; buvid_fp_plain=E2B1C11B-A111-4692-B768-316E8429C7E018547infoc; DedeUserID=35906556; DedeUserID__ckMd5=6bc77a6b9c4d788a; SESSDATA=d2c1dbd1%2C1630807734%2C99121*31; bili_jct=b0752bdcf4df366921028c4ff10d0374; PVID=1; CURRENT_QUALITY=0; innersign=0; arrange=matrix"
}
key = input('请输入关键词:')
key1 = quote(key)
filename = 'D:/Data/{}'.format(key)
if not os.path.exists(filename):
    os.makedirs(filename)

def parse_url(url):
    html = requests.get(url=url,headers=headers)
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)

def get_number(url):
    html = requests.get(url=url, headers=headers)
    if html.status_code == 200:
        content = html.text
        soup = etree.HTML(content)
        number = soup.xpath('//li[@class="page-item last"]/button/text()')[0].strip('\n').strip(' ')
        return number
    else:
        print(html.status_code)

def get_html(html):
    content = html.text
    soup = etree.HTML(content)
    times = soup.xpath("//span[@class='so-imgTag_rb']/text()")
    href = soup.xpath("//li[@class='video-item matrix']/a/@href")
    for i in range(len(href)):
        href1 = "https:" + href[i]
        dowloand(href1)



def dowloand(url):
    cmd = "you-get --format=flv480 -o {}".format(filename) + " " + url
    os.system(cmd)

def get_url():
    print('输入0为获取关键字所有视频，输入1为获取10分钟以下的视频')
    print('输入2为获取10-30分钟以内的视频，输入3为获取30-60分钟以内的视频，输入4位获取60分钟以上的视频')
    name = input('请输入具体数字操作:')
    return name

    
if __name__ == '__main__':
    shuzhi = get_url()
    url = 'https://search.bilibili.com/video?keyword={}&order=totalrank&duration={}&tids_1=0'.format(key1,shuzhi)
    number = get_number(url)
    for n in tqdm(range(2,int(number)+1)):
    # for n in tqdm(range(1,3)):
        url1 = 'https://search.bilibili.com/video?keyword={}&order=totalrank&duration={}&tids_1=0&page={}'.format(key1, shuzhi, n)
        parse_url(url1)

