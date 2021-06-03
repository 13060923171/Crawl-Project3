from lxml import etree
import re
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


def get_html(content):
    soup = etree.HTML(content)
    # soups = BeautifulSoup(content, 'lxml')
    # items = soups.select('div.tF2Cxc')
    # for i in items:
    #     title = i.select_one('h3.LC20lb.DKV0Md').text
    #     time = i.select_one('span.aCOpRe span').text
    #     # comment = i.select_one('div.tF2Cxc div.IsZvec span ')
    #     # print(comment)
    # comment = soups.select('div.tF2Cxc div.IsZvec span')
    # for c in comment:
    #     c = c.text
    #     print(c)
    list_title = []
    list_time = []
    list_comment = []
    items = soup.xpath("//div[@class='tF2Cxc']")
    for i in items:
        title = i.xpath("./div[@class='yuRUbf']/a/h3/text()")[0]
        time = i.xpath("./div[@class='IsZvec']/span/span/text()")[0]
        list_title.append(title)
        list_time.append(time)
    comment = re.compile('</span><span>(.*?)</span></span>',re.S|re.I)
    comments = comment.findall(content)

    for c in comments:
        c = c.replace('<em>','').replace('</em>','').strip(' ').replace('<wbr>','').replace('...','').replace('&nbsp','')
        list_comment.append(c)
    save_excel(list_title, list_comment, list_time)

def save_excel(list_title,list_comment,list_time):
    df = pd.DataFrame()
    print(len(list_title))
    print(len(list_time))
    print(len(list_comment))
    df['标题'] = list_title
    df['内容'] = list_comment
    df['时间'] = list_time
    df.to_csv('李宇春-男.csv',mode="a+", header=None, index=None, encoding="utf-8")

if __name__ == '__main__':
    for i in tqdm(range(8, 9)):
        with open('./李宇春 男/李宇春 男 - Google 搜索{}.html'.format(i), 'r', encoding='utf-8')as f:
            content = f.read()
        get_html(content)