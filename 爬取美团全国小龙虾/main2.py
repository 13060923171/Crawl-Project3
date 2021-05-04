import requests
import re
import json
import random
import time
from tqdm import tqdm
from lxml import etree

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



def get_parse(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        "Host": "gz.meituan.com",
        "Referer": "https://gz.meituan.com/meishi/c54/pn5/",
        "Cookie": "_lxsdk_cuid=176cc938bb490-0040463f3d68d8-c791039-e1000-176cc938bb5c8; iuuid=25A31E7553EB400F96942D62BCA7FFBAE7732C1D202A34A2546AD68C9161CB68; _lxsdk=25A31E7553EB400F96942D62BCA7FFBAE7732C1D202A34A2546AD68C9161CB68; Hm_lvt_f66b37722f586a240d4621318a5a6ebe=1609852138; cityname=%E6%97%A0%E9%94%A1; mtcdn=K; lsu=; _hc.v=6fea36cf-6c02-d091-81e6-5ab379b908b1.1619617992; uuid=467ca50fcf8c4c2f9ca8.1619840960.1.0.0; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; userTicket=fRzWlldQDxidqrjWcmmqmiTemOVxaKWUGLLcQQQb; u=229598129; n=%E4%BD%A0%E5%A5%8B%E6%96%97%E7%9A%84%E6%A0%B7%E5%AD%90%E7%9C%9F%E7%BE%8E; lt=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; mt_c_token=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; token=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; token2=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; unc=%E4%BD%A0%E5%A5%8B%E6%96%97%E7%9A%84%E6%A0%B7%E5%AD%90%E7%9C%9F%E7%BE%8E; __mta=121412663.1619846786827.1619846786827.1619847406341.2; client-id=e9743547-abd4-435e-a5e2-f223f4f87893; ci=52; rvct=52%2C20%2C1; lat=22.978195; lng=113.317448; firstTime=1619851410205; _lxsdk_s=1792695e9c5-758-32c-93b%7C%7C9",
        "User-Agent": random.choice(user_agent),
    }
    html = requests.get(url=url,headers=headers)

    if html.status_code:
        get_html(html)
    else:
        print(html.status_code)


def get_html(html):
    content = html.text
    print(content)
    #店名
    href = re.compile('"url":"{.*?}"}')
    hrefs = href.findall(content)
    print(hrefs)
    # for h in hrefs:
    #     print(h)
    # for i in items:
    #     href = i.xpath("/a/@href")[0]
    #     print(href)
    #     get_phone(href)

def get_phone(href):
    headers = {
        "Cookie": "_lxsdk_cuid=176cc938bb490-0040463f3d68d8-c791039-e1000-176cc938bb5c8; __mta=249928633.1609749990443.1609749990443.1609749990443.1; iuuid=25A31E7553EB400F96942D62BCA7FFBAE7732C1D202A34A2546AD68C9161CB68; _lxsdk=25A31E7553EB400F96942D62BCA7FFBAE7732C1D202A34A2546AD68C9161CB68; Hm_lvt_f66b37722f586a240d4621318a5a6ebe=1609852138; cityname=%E6%97%A0%E9%94%A1; mtcdn=K; lsu=; _hc.v=6fea36cf-6c02-d091-81e6-5ab379b908b1.1619617992; uuid=467ca50fcf8c4c2f9ca8.1619840960.1.0.0; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; userTicket=fRzWlldQDxidqrjWcmmqmiTemOVxaKWUGLLcQQQb; u=229598129; n=%E4%BD%A0%E5%A5%8B%E6%96%97%E7%9A%84%E6%A0%B7%E5%AD%90%E7%9C%9F%E7%BE%8E; lt=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; mt_c_token=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; token=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; token2=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; unc=%E4%BD%A0%E5%A5%8B%E6%96%97%E7%9A%84%E6%A0%B7%E5%AD%90%E7%9C%9F%E7%BE%8E; client-id=50d9d632-29cd-45c5-98fb-14336570d747; ci=52; rvct=52%2C20%2C1; firstTime=1619850030999; lat=22.978195; lng=113.317448; _lxsdk_s=1792695e9c5-758-32c-93b%7C%7C3",
        "User-Agent": random.choice(user_agent),
    }
    html = requests.get(url=href,headers=headers)
    content = html.text
    soup = etree.HTML(content)
    items = soup.xpath("//div[@class='d-left']")
    for i in items:
        title = i.soup("./div[@class='name']/text()")[0]
        address = i.soup("./div[@class='address']/p/text()")
        print(address)


# def dowload(t,a,p):
#     data = {
#         '店铺名称': t,
#         '所在省份': '广东省',
#         # '所在城市': name[l],
#         '店铺地址': a,
#         '电话': p
#     }
#     with open("广东省小龙虾商家信息.txt","a+",encoding="utf-8")as f:
#         f.write(json.dumps(data,ensure_ascii=False)+"\n")
#         print("写入成功")
#
#
# def city_number():
#     headers = {
#
#         'Host': 'hotel.meituan.com',
#         'Cookie': '_lxsdk_cuid=176cc938bb490-0040463f3d68d8-c791039-e1000-176cc938bb5c8; iuuid=25A31E7553EB400F96942D62BCA7FFBAE7732C1D202A34A2546AD68C9161CB68; _lxsdk=25A31E7553EB400F96942D62BCA7FFBAE7732C1D202A34A2546AD68C9161CB68; Hm_lvt_f66b37722f586a240d4621318a5a6ebe=1609852138; ci=52; cityname=%E6%97%A0%E9%94%A1; mtcdn=K; lsu=; _hc.v=6fea36cf-6c02-d091-81e6-5ab379b908b1.1619617992; uuid=467ca50fcf8c4c2f9ca8.1619840960.1.0.0; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; userTicket=fRzWlldQDxidqrjWcmmqmiTemOVxaKWUGLLcQQQb; u=229598129; n=%E4%BD%A0%E5%A5%8B%E6%96%97%E7%9A%84%E6%A0%B7%E5%AD%90%E7%9C%9F%E7%BE%8E; lt=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; mt_c_token=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; token=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; token2=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ; unc=%E4%BD%A0%E5%A5%8B%E6%96%97%E7%9A%84%E6%A0%B7%E5%AD%90%E7%9C%9F%E7%BE%8E; firstTime=1619843092025',
#         'User-Agent': random.choice(user_agent),
#     }
#     url = 'https://hotel.meituan.com/dist/static/data/city.json?utm_medium=pc&version_name=999.9'
#     html = requests.get(url, headers=headers)
#     content = html.json()
#
#     data = content['data']
#     with open('省份城市.txt', 'r', encoding='utf-8') as f:
#         content1 = f.readlines()
#     city = []
#     for c in content1:
#         c = str(c)
#         c = c.split('(')
#         city.append(c[0])
#     number_list = []
#     name_list = []
#     for d in range(len(data)):
#         name = data[d]['name']
#         id = data[d]['id']
#         for c in city:
#             if name in c:
#                 number_list.append(id)
#                 name_list.append(name)
#     return number_list,name_list
#

if __name__ == '__main__':
    # #在这个URL里面offse参数每次翻页增加32，limit参数是一次请求的数据量，q是搜索关键词poi/pcsearch/1？其中的1是北京城市的id编号。
    # for i in range(0,33,32):
    #     url = "https://apimobile.meituan.com/group/v4/poi/pcsearch/1?uuid=b1b2966b4c8d4eeeacf4.1619659713.1.0.0&userid=229598129&limit=32&offset={}&cateId=-1&q=%E5%B0%8F%E9%BE%99%E8%99%BE".format(i)
    #     get_parse(url)
    # number,name = city_number()
    # for l in number:
    #     for i in range(0, 961, 32):
    #         url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/{}?uuid=467ca50fcf8c4c2f9ca8.1619840960.1.0.0&userid=229598129&limit=32&offset={}&cateId=-1&q=%E5%B0%8F%E9%BE%99%E8%99%BE&token=sagsaE5u84XC6OGi7vY3J8lYHSQAAAAAZg0AAGjbpzUeDGr3S2WlcVsdTOv1G-jVoXffNaRXPupNnyruPhhg1KBOiElcEhuglWImfQ'.format(
    #             str(l),str(i))
    #         get_parse(url)
    #         sleepTime = random.randint(1, 10)
    #         print('睡眠' + str(sleepTime) + '秒')
    #         time.sleep(sleepTime)
    url = 'https://gz.meituan.com/meishi/c54/pn5/'
    get_parse(url)