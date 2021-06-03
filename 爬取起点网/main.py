import requests
from fake_useragent import UserAgent
import json
from lxml import etree

#一个随机的user-agent库
ua = UserAgent(verify_ssl=False)

headers = {
    "user-agent":ua.random,
    "referer": "https://book.qidian.com/info/1209977",
    "cookie": "_csrfToken=r9dxDTt7GJKvujvpAwyAvdXC67AvTZVBqbDeqefY; newstatisticUUID=1622377322_1651296694; _yep_uuid=00dbd6ce-e523-71b1-5137-4e4aa07640cf; e1=%7B%22pid%22%3A%22qd_P_Searchresult%22%2C%22eid%22%3A%22qd_S05%22%2C%22l1%22%3A3%7D; e2=%7B%22pid%22%3A%22qd_P_all%22%2C%22eid%22%3A%22%22%2C%22l1%22%3A2%7D",

}


def get_parse(url):
    html = requests.get(url,headers=headers)
    if html.status_code == 200:
        html.encoding = html.apparent_encoding
        get_html(html)
    else:
        print(html.status_code)

def get_html(html):
    conent = html.json()
    number = conent['data']['vs'][1]['cCnt']
    data = conent['data']['vs'][1]['cs']
    for d in range(int(number)):
        link = "https://read.qidian.com/chapter/" + data[d]['cU']
        res = requests.get(link,headers=headers)
        c=res.content.decode('utf-8')
        soup = etree.HTML(c)
        names = soup.xpath('//span[@class="content-wrap"]/text()')
        results = soup.xpath('//div[@class="read-content j_readContent"]/p/text()')
        for name in names:
            with open('./data/' + name + '.txt', 'a') as f:
                for result in results:
                    f.write(result + '\n')



if __name__ == '__main__':
    url = 'https://book.qidian.com/ajax/book/category?_csrfToken=r9dxDTt7GJKvujvpAwyAvdXC67AvTZVBqbDeqefY&bookId=1209977'
    get_parse(url)