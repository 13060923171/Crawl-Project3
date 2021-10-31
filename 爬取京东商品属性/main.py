import requests
from lxml import etree
from urllib import parse
import json
import re
from tqdm import tqdm
import time
import random
headers = {

    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'referer': 'https://www.jd.com/',
    'cookie': '__jdv=76161171|baidu|-|organic|%25E4%25BA%25AC%25E4%25B8%259C|1618277962883; __jdu=161827796288293166331; areaId=19; ipLoc-djd=19-1601-36953-0; PCSYCityID=CN_440000_440100_440113; __jda=122270672.161827796288293166331.1618277963.1618277963.1618277963.1; __jdc=122270672; shshshfp=20533b16e5376ccce55364a2a79af360; shshshfpa=afbfb5a6-2b2f-2cd1-32c9-08f6cb7b5e62-1618277978; shshshfpb=bUxR1wpyM7eG3WPxMIY3taQ%3D%3D; rkv=1.0; qrsc=3; __jdb=122270672.7.161827796288293166331|1.1618277963; shshshsID=62ef4e44f8ae4ecf3c3bf515a929b216_6_1618279510237; 3AB9D23F7A4B3C9B=VXCREJHRBERJFNRSY7JQ5GDZ3XXG3TDRDLBEPH5N3QML3Y3RHTZRTEUTUJ3EE3LZOZRXXFF2ZTMB7NKN2N7PBKKTUA'

}


KEYWORD = parse.quote('手机')

def get_parse(url):
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)

def get_html(html):
    content = html.text
    soup = etree.HTML(content)
    items = soup.xpath("//div[@class='gl-i-wrap']")
    for i in range(len(items)):
        href = soup.xpath("//div[@class='p-img']/a[@target='_blank']/@href")[i]
        href = 'https:' + href
        commit = re.compile('https://item.jd.com/(.*?).html',re.S|re.I)
        commits = commit.findall(href)
        comment,goodrate,poorrate = get_number(commits[0])

        price = soup.xpath("//div[@class='p-price']/strong/i/text()")[i]
        a = random.random()
        time.sleep(a)
        get_comment(href,price,comment,goodrate,poorrate)


def get_number(commits):
    url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}&callback=jQuery3238709&_=1618278194940'.format(commits)
    headers = {
        'Cookie': '__jdv=76161171|baidu|-|organic|%25E4%25BA%25AC%25E4%25B8%259C|1618277962883; __jdu=161827796288293166331; areaId=19; ipLoc-djd=19-1601-36953-0; PCSYCityID=CN_440000_440100_440113; __jda=122270672.161827796288293166331.1618277963.1618277963.1618277963.1; __jdc=122270672; shshshfp=20533b16e5376ccce55364a2a79af360; shshshfpa=afbfb5a6-2b2f-2cd1-32c9-08f6cb7b5e62-1618277978; shshshfpb=bUxR1wpyM7eG3WPxMIY3taQ%3D%3D; 3AB9D23F7A4B3C9B=VXCREJHRBERJFNRSY7JQ5GDZ3XXG3TDRDLBEPH5N3QML3Y3RHTZRTEUTUJ3EE3LZOZRXXFF2ZTMB7NKN2N7PBKKTUA; __jdb=122270672.5.161827796288293166331|1.1618277963; shshshsID=62ef4e44f8ae4ecf3c3bf515a929b216_4_1618278194833',
        'Host': 'club.jd.com',
        'Referer': 'https://search.jd.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    }
    html = requests.get(url,headers=headers)
    content = html.text
    comment = re.compile('"CommentCountStr":"(.*?)",', re.I | re.S)
    comments = comment.findall(content)
    goodrate = re.compile('"GoodRate":(.*?),', re.I | re.S)
    goodrates = goodrate.findall(content)
    poorrate = re.compile('"GeneralRate":(.*?),', re.I | re.S)
    poorrates = poorrate.findall(content)
    return comments[0],goodrates[0],poorrates[0]


def get_comment(url,price,comment,goodrate,poorrate):
    html = requests.get(url,headers=headers)
    content = html.text
    soup = etree.HTML(content)
    attribute = soup.xpath("//ul[@class='parameter2 p-parameter-list']/li/@title")
    d = {
        'price': price,
        'comment':comment,
        'goodrate':goodrate,
        'poorrate':poorrate,
        'attribute': attribute,
    }
    print(d)
    save_to_file(d)

#写一个保存文件的函数
def save_to_file(result):
    #a是追加信息的意思
    with open("商品属性1.text","a",encoding='utf-8') as f:
        #把python转化为json，然后用json的形式保存下来，ensure_ascii=False是识别有没有中文的意思
        f.write(json.dumps(result,ensure_ascii=False)+"\n")
        print("存储到text成功")


if __name__ == '__main__':
    list1 = []
    for i in range(1,154,1):
        list1.append(i)
    list2 = [1,27]
    for j in range(56,4557,30):
        list2.append(j)
    for l in tqdm(range(len(list2))):
        url = 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&wq=%E6%89%8B%E6%9C%BA&page={}&s={}&click=0'.format(list1[l],list2[l])
        get_parse(url)




