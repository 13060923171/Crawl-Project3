import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

df = pd.read_excel('商品属性.xls').loc[:,['品牌','评论']]


list_comment = []
for i in df['评论']:
    i = i.strip(' ').replace('"comment":','').replace('"','').strip(' ').replace('万','0000').replace('+','')
    i = int(i)
    list_comment.append(i)

list_title = []
for i in df['品牌']:
    i = str(i)
    i = i.replace('attribute','').replace('"','').replace(':','').replace('[','').strip(' ')
    list_title.append(i)

count_mini = 0
count_huawei = 0
count_oppo = 0
count_vivo = 0
count_svmsung = 0
count_apple = 0
count_iphone = 0
for i in range(len(list_title)):
    if '小米' in list_title[i] or '红米' in list_title[i] :
        count_mini += list_comment[i]
    elif 'OPPO' in list_title[i] or 'oppo' in list_title[i] :
        count_oppo += list_comment[i]
    elif 'iQOO' in list_title[i] or 'vivo' in list_title[i] or '一加' in list_title[i]:
        count_vivo += list_comment[i]
    elif '华为' in list_title[i] or '荣耀' in list_title[i]:
        count_huawei += list_comment[i]
    elif '苹果' in list_title[i] or 'Apple' in list_title[i] or 'iPhone' in list_title[i]:
        count_apple += list_comment[i]
    elif '三星' in list_title[i]:
        count_svmsung += list_comment[i]
    else:
        count_iphone += list_comment[i]

x_data = ['华为','小米','苹果','其他品牌的手机','vivo','OPPO','三星']
y_data = [count_huawei,count_mini,count_apple,count_iphone,count_vivo,count_oppo,count_svmsung]


def main_reversal():
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
        .add_xaxis(x_data)
        .add_yaxis("销量", y_data, label_opts=opts.LabelOpts(is_show=False))
        .reversal_axis()
        .set_global_opts(
            title_opts={"text": "不同品牌手机销量对比"}
        )
    )

    return c

