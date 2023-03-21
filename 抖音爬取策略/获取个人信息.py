import os
import time
import re
from lxml import etree
import requests
from selenium import webdriver
import pandas as pd
from tqdm import tqdm


def get_video_ids(author_url):
    chrome_option = webdriver.ChromeOptions()
    # chrome_option.add_argument('headless')  # 静默模式
    driver = webdriver.Chrome(options=chrome_option)
    driver.get(author_url)
    a = input('登录成功,请输入回车:')
    for i in range(0,9001,3000):
        driver.execute_script("window.scrollBy(0,{})".format(i))
        time.sleep(2)
        html_source = driver.page_source
        soup = etree.HTML(html_source)
        content = soup.xpath('//li[@class="Eie04v01"]')
        for c in tqdm(content):
            try:
                title = c.xpath('./a/p[@class="__0w4MvO"]/text()')[0]
            except:
                title = ''
            try:
                href = c.xpath('./a/@href')[0]
            except:
                href = ''

            df = pd.DataFrame()
            df['标题'] = [title]
            df['视频链接'] = [href]
            df.to_csv('data.csv', encoding='utf-8-sig', mode='a+', index=False, header=False)


def main1():
    df = pd.read_csv('data.csv')
    df = df.drop_duplicates(keep='first')
    df.to_csv('new_data.csv',encoding='utf-8-sig')


if __name__ == '__main__':
    df = pd.DataFrame()
    df['标题'] = ['标题']
    df['视频链接'] = ['视频链接']
    df.to_csv('data.csv',encoding='utf-8-sig',mode='w',index=False,header=False)
    data = pd.read_excel('账号.xlsx')
    for d in tqdm(data['主页']):
        url = d
        get_video_ids(url)
        main1()