# 导入需要的模块
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib
from tqdm import tqdm
# 处理乱码
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False


def get_html(code, start_date, end_date, page=1, per=20):
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&page={1}&sdate={2}&edate={3}&per={4}'.format(
        code, page, start_date, end_date, per)
    rsp = requests.get(url)
    html = rsp.text
    return html


def get_fund(code, start_date, end_date, page=1, per=20):
    # 获取html
    html = get_html(code, start_date, end_date, page, per)
    soup = BeautifulSoup(html, 'html.parser')
    # 获取总页数
    pattern = re.compile('pages:(.*),')
    result = re.search(pattern, html).group(1)
    total_page = int(result)
    # 获取表头信息
    heads = []
    for head in soup.findAll("th"):
        heads.append(head.contents[0])

    # 数据存取列表
    records = []
    # 获取每一页的数据
    current_page = 1
    while current_page <= total_page:
        html = get_html(code, start_date, end_date, current_page, per)
        soup = BeautifulSoup(html, 'html.parser')
        # 获取数据
        for row in soup.findAll("tbody")[0].findAll("tr"):
            row_records = []
            for record in row.findAll('td'):
                val = record.contents
                # 处理空值
                if val == []:
                    row_records.append(np.nan)
                else:
                    row_records.append(val[0])
            # 记录数据
            records.append(row_records)
        # 下一页
        current_page = current_page + 1

    # 将数据转换为Dataframe对象
    np_records = np.array(records)
    fund_df = pd.DataFrame()
    for col, col_name in enumerate(heads):
        fund_df[col_name] = np_records[:, col]

    # 按照日期排序
    fund_df['净值日期'] = pd.to_datetime(fund_df['净值日期'], format='%Y/%m/%d')
    fund_df = fund_df.sort_values(by='净值日期', axis=0, ascending=True).reset_index(drop=True)
    fund_df = fund_df.set_index('净值日期')

    # 数据类型处理
    fund_df['单位净值'] = fund_df['单位净值'].astype(float)
    fund_df['累计净值'] = fund_df['累计净值'].astype(float)
    fund_df['日增长率'] = fund_df['日增长率'].str.strip('%').astype(float)
    return fund_df

def data():
    with open('代码.txt','r',encoding='utf-8')as f:
        content = f.readlines()
    now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    over_the_past_year = str(int(now[0:4]) - 1) + now[4:]
    list_one_week = []
    list_two_week = []
    list_three_week = []
    list_four_week = []
    list_one_month = []
    list_three_month = []
    list_six_month = []
    list_one_year = []
    list_data_time = []
    list_rate_of_increase = []
    d = [i.strip('\n') for i in content]
    for i in tqdm(d):
        fund_df = get_fund('{}'.format(i), start_date='{}'.format(over_the_past_year), end_date='{}'.format(now))
        if int(int(now[8:]) - 2) < 10:
            data_time = str(now[5:8]) + '0' + str(int(now[8:]) - 2)
            list_data_time.append(data_time)
        else:
            data_time = str(now[5:8])+ str(int(now[8:]) - 2)
            list_data_time.append(data_time)
        rate_of_increase = "{}".format((fund_df['日增长率'][-1]))
        print(fund_df)
        list_rate_of_increase.append(rate_of_increase)
        one_week = "{:.3}%".format(sum([float(o) for o in fund_df['日增长率'][-7:]]))
        list_one_week.append(one_week)
        two_week = "{:.3}%".format(sum([float(o) for o in fund_df['日增长率'][-14:]]))
        list_two_week.append(two_week)
        three_week = "{:.3}%".format(sum([float(o) for o in fund_df['日增长率'][-21:]]))
        list_three_week.append(three_week)
        four_week = "{:.3}%".format(sum([float(o) for o in fund_df['日增长率'][-28:]]))
        list_four_week.append(four_week)
        one_month = "{:.3}%".format(sum([float(o) for o in fund_df['日增长率'][-30:]]))
        list_one_month.append(one_month)
        three_month = "{:.3}%".format(sum([float(o) for o in fund_df['日增长率'][-90:]]))
        list_three_month.append(three_month)
        six_month = "{:.3}%".format(sum([float(o) for o in fund_df['日增长率'][-180:]]))
        list_six_month.append(six_month)
        one_year = "{:.3}%".format(sum([float(o) for o in fund_df['日增长率'][:]]))
        list_one_year.append(one_year)
    return list_one_week,list_two_week,list_three_week,list_four_week,list_one_month,list_three_month,list_six_month,list_one_year,list_data_time,list_rate_of_increase,d



if __name__ == '__main__':
    list_one_week,list_two_week,list_three_week,list_four_week,list_one_month,list_three_month,list_six_month,list_one_year,list_data_time,list_rate_of_increase,d = data()
    df = pd.DataFrame()
    df['基金代码'] = d
    df['最新日期'] = list_data_time
    df['最新增长率'] = list_rate_of_increase
    df['最近一个星期'] = list_one_week
    df['最近两个星期'] = list_two_week
    df['最近三个星期'] = list_three_week
    df['最近四个星期'] = list_four_week
    df['最近一个月'] = list_one_month
    df['最近三个月'] = list_three_month
    df['最近六个月'] = list_six_month
    df['最近一年'] = list_one_year
    df.to_excel('基金分析.xlsx')
    print('success')
