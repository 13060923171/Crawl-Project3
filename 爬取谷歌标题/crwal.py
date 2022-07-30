import time
import urllib3
from lxml import etree
import requests
import pandas as pd
from tqdm import tqdm
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}


def get_status(url):
    # 增加重试连接次数
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.Session()
    # 关闭多余连接
    s.keep_alive = False
    # 取消验证证书
    s.verify = False
    # 关闭在设置了verify=False后的错误提示
    urllib3.disable_warnings()
    proxies = {
        'http': 'http://127.0.0.1:7890/',
        'https': 'http://127.0.0.1:7890/'
    }
    res = s.get(url=url, headers=headers, proxies=proxies)
    time.sleep(1)
    if res.status_code == 200:
        get_html(res)
    else:
        print(res.status_code)


def get_html(html):
    content = html.text
    soup = etree.HTML(content)
    title = soup.xpath('//div[@class="mCBkyc y355M ynAwRc MBeuO nDgy9d"]/text()')
    for t in title:
        df = pd.DataFrame()
        df['标题'] = [t]
        df.to_csv('数据.csv', encoding='utf-8-sig', index=None,mode='a+',header=None)


if __name__ == '__main__':
    df = pd.DataFrame()
    df['标题'] = ['标题']
    df.to_csv('数据.csv',encoding='utf-8-sig',index=None,mode='w',header=None)
    for i in tqdm(range(0,281,10)):
        url = 'https://www.google.com.hk/search?q=Virginia+crime+rate&newwindow=1&rlz=1C1CHWL_zh-CNCN908CN908&tbs=cdr:1,cd_min:3/24/2022,cd_max:7/24/2022&tbm=nws&sxsrf=ALiCzsbpGx-bwyvoAUqqsWHEgqnP8to6UA:1658647845762&ei=JfXcYvL_LZ-y2roP58Kp6As&start={}&sa=N&ved=2ahUKEwiypp3dgJH5AhUfmVYBHWdhCr04FBDy0wN6BAgBEDo&biw=1920&bih=975&dpr=1'.format(i)
        get_status(url)