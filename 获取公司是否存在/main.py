import requests
import pandas as pd
from tqdm import tqdm

def get_data(keywords):
    url = "http://restapi.amap.com/v3/place/text?key=cdb418bdf7be6ca2fc93bbbfec7108cc&keywords={}&types=&city=&children=&offset=&page=&extensions=all".format(keywords)
    html = requests.get(url)
    if html.status_code == 200:
        content = html.json()
        count = content['count']
        if int(count) >= 1:
            return '能'
        else:
            return '不能'
    else:
        print('今日使用的次数已超过，请明天再使用')


def get_name():
    df = pd.read_excel('河源整理.xlsx').loc[:,['企业名称']]
    list_name = [str(n) for n in df['企业名称']]
    list_status = []
    for l in tqdm(list_name):
        status = get_data(l)
        list_status.append(status)
    df1 = pd.DataFrame()
    df1['企业名称'] = list_name
    df1['能否导航'] = list_status
    df1.to_excel('河源整理-新.xlsx',index=None,encoding='gbk')


if __name__ == '__main__':
    get_name()