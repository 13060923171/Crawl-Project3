import requests
from lxml import etree
from urllib.parse import quote_plus
import pandas as pd
import time
from tqdm import tqdm



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    "Cookie": "acw_tc=2760828a16319323346108685e7ae7ec2f7192b77414ac265bc753caf64e83; __uuid=1631932339089.97; __tlog=1631932339103.63%7C00000000%7C00000000%7C00000000%7C00000000; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1631932339; fe_se=-1631932339660; __s_bid=d3ecefef645854030cc86b62a3b1aa3e4b62; JSESSIONID=765D9305F2D0363C4C7CA4C822F271D8; __session_seq=11; __uv_seq=11; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1631932652",
}

session = requests.session()
session.headers = headers

def get_parse(url):
    html = session.get(url,headers=headers)
    if html.status_code ==200:
        get_html(html)
    else:
        print(html.status_code)


def get_html(html):
    content = html.text
    soup = etree.HTML(content)
    list_href = []
    href = soup.xpath("//div[@class='job-info']/h3/a/@href")
    for h in href:
        if '/a/' in h:
            url = "https://www.liepin.com" + h
            list_href.append(url)
        else:
            list_href.append(h)
    for h in list_href:
        get_data(h)

def get_data(url):
    html = session.get(url,headers=headers)
    content = html.text
    soup = etree.HTML(content)
    intro = soup.xpath('//dd[@data-selector="job-intro-content"]/text()')
    name = soup.xpath('//div[@class="name-box"]/span[@class="name ellipsis-1"]/text()')
    salary = soup.xpath('//div[@class="name-box"]/span[@class="salary"]/text()')
    diction = soup.xpath('//div[@class="job-properties"]/span[1]/text()')
    split = soup.xpath('//div[@class="job-properties"]/span[3]/text()')
    education = soup.xpath('//div[@class="job-properties"]/span[5]/text()')

    list_education = []
    list_split = []
    list_diction = []
    list_salary = []
    list_name = []
    list_intro = []

    if len(education) == 0:
        education1 = '无'
        list_education.append(education1)
    else:
        list_education.append(education[0])

    if len(split) == 0:
        split1 = '无'
        list_split.append(split1)
    else:
        list_split.append(split[0])

    if len(diction) == 0:
        diction1 = '无'
        list_diction.append(diction1)
    else:
        list_diction.append(diction[0])

    if len(salary) == 0:
        salary1 = '无'
        list_salary.append(salary1)
    else:
        list_salary.append(salary[0])

    if len(name) == 0:
        name1 = '无'
        list_name.append(name1)
    else:
        list_name.append(name[0])

    if len(intro) == 0:
        intro1 = '无'
        list_education.append(intro1)
    else:
        list_intro.append(intro[0].replace('\r','').replace('\n','').replace('\xa0',''))

    df = pd.DataFrame()
    df['name'] = list_name
    df['salary'] = list_salary
    df['diction'] = list_diction
    df['split'] = list_split
    df['education'] = list_education
    df['intro'] = list_intro


    try:
        df.to_csv("猎聘碳材料.csv", mode="a+", header=None, index=None, encoding="utf-8")
        print("写入成功")
    except:
        print("当页数据写入失败")
    time.sleep(0.2)

if __name__ == '__main__':
    keyword = '碳材料'
    for i in tqdm(range(0,3)):
        url = 'https://www.liepin.com/zhaopin/?compkind=&dqs=060&sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&&key={}&curPage={}'.format(quote_plus(keyword),i)
        get_parse(url)