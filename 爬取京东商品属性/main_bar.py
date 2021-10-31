import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

df = pd.read_excel('商品属性.xls').loc[:,['价钱','评论']]

list_price = []
for i in df['价钱']:
    i = i.replace('"','').replace("{",'').replace('price','').replace(':','').replace(' ','')\
        .replace('.00','').replace('.01','').replace('.99','').replace('.80','').replace('.90','')\
        .replace('.88','').replace('.20','').replace('.93','').replace('.70','')\
        .replace('.10','').replace('.91','').replace('.87','')
    list_price.append(i)

list_comment = []
for i in df['评论']:
    i = i.strip(' ').replace('"comment":','').replace('"','').strip(' ').replace('万','0000').replace('+','')
    i = int(i)
    list_comment.append(i)

sum_1000 = 0
sum_2000 = 0
sum_3000 = 0
sum_4000 = 0
sum_5000 = 0
sum_10000 = 0
for i in range(len(list_price)):
    if int(list_price[i]) < 1000:
        sum_1000 += list_comment[i]
    elif 1000 <= int(list_price[i]) < 2000:
        sum_2000 += list_comment[i]
    elif 2000 <= int(list_price[i]) < 3000:
        sum_3000 += list_comment[i]
    elif 3000 <= int(list_price[i]) < 4000:
        sum_4000 += list_comment[i]
    elif 4000 <= int(list_price[i]) < 5000:
        sum_5000 += list_comment[i]
    else:
        sum_10000 += list_comment[i]


x_data = ['0-1000','1000-2000','2000-3000','3000-4000','4000-5000','5000及以上']
y_data = [sum_1000,sum_2000,sum_3000,sum_4000,sum_5000,sum_10000]


def main_bar():
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
        .add_xaxis(x_data)
        .add_yaxis("销量总数", y_data, label_opts=opts.LabelOpts(is_show=False))

        .set_global_opts(
            title_opts={"text": "各个价格区域之间的销量总数"},
        )
    )
    return c

