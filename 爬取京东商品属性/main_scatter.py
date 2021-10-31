from pyecharts import options as opts
from pyecharts.charts import Scatter
from pyecharts.commons.utils import JsCode
import pandas as pd
from pyecharts.globals import ThemeType

df = pd.read_excel('商品属性.xls').loc[:,['好评','差评','品牌']]

list_good = []
for i in df['好评']:
    i = i.replace('goodrate','').replace(":","").replace('"','').strip(' ')
    list_good.append(float(i))


list_poor = []
for i in df['差评']:
    i = i.replace('poorrate','').replace(":","").replace('"','').strip(' ')
    list_poor.append(float(i))

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
sum_mini = 0
sum_huawei = 0
sum_oppo = 0
sum_vivo = 0
sum_svmsung = 0
sum_apple = 0
sum_iphone = 0
for i in range(len(list_title)):
    if '小米' in list_title[i] or '红米' in list_title[i] :
        count_mini += list_good[i]
        sum_mini += 1
    elif 'OPPO' in list_title[i] or 'oppo' in list_title[i] :
        count_oppo += list_good[i]
        sum_oppo += 1
    elif 'iQOO' in list_title[i] or 'vivo' in list_title[i] or '一加' in list_title[i]:
        count_vivo += list_good[i]
        sum_vivo += 1
    elif '华为' in list_title[i] or '荣耀' in list_title[i]:
        count_huawei += list_good[i]
        sum_huawei += 1
    elif '苹果' in list_title[i] or 'Apple' in list_title[i] or 'iPhone' in list_title[i]:
        count_apple += list_good[i]
        sum_apple += 1
    elif '三星' in list_title[i]:
        count_svmsung += list_good[i]
        sum_svmsung += 1
    else:
        count_iphone += list_good[i]
        sum_iphone += 1

count_mini_poor = 0
count_huawei_poor = 0
count_oppo_poor = 0
count_vivo_poor = 0
count_svmsung_poor = 0
count_apple_poor = 0
count_iphone_poor = 0
sum_mini_poor = 0
sum_huawei_poor = 0
sum_oppo_poor = 0
sum_vivo_poor = 0
sum_svmsung_poor = 0
sum_apple_poor = 0
sum_iphone_poor = 0
for i in range(len(list_title)):
    if '小米' in list_title[i] or '红米' in list_title[i] :
        count_mini_poor += list_poor[i]
        sum_mini_poor += 1
    elif 'OPPO' in list_title[i] or 'oppo' in list_title[i] :
        count_oppo_poor += list_poor[i]
        sum_oppo_poor += 1
    elif 'iQOO' in list_title[i] or 'vivo' in list_title[i] or '一加' in list_title[i]:
        count_vivo_poor += list_poor[i]
        sum_vivo_poor += 1
    elif '华为' in list_title[i] or '荣耀' in list_title[i]:
        count_huawei_poor += list_poor[i]
        sum_huawei_poor += 1
    elif '苹果' in list_title[i] or 'Apple' in list_title[i] or 'iPhone' in list_title[i]:
        count_apple_poor += list_poor[i]
        sum_apple_poor += 1
    elif '三星' in list_title[i]:
        count_svmsung_poor += list_poor[i]
        sum_svmsung_poor += 1
    else:
        count_iphone_poor += list_poor[i]
        sum_iphone_poor += 1





def new_round(_float, _len):
    if isinstance(_float, float):
        if str(_float)[::-1].find('.') <= _len:
            return (_float)
        if str(_float)[-1] == '5':
            return (round(float(str(_float)[:-1] + '6'), _len))
        else:
            return (round(_float, _len))
    else:
        return (round(_float, _len))

x_data = ['华为','小米','苹果','vivo','OPPO','三星','其他手机']
y_data = []
a = new_round(float(count_huawei/sum_huawei),3)
y_data.append(a)
b = new_round(float(count_mini/sum_mini),3)
y_data.append(b)
c = new_round(float(count_apple/sum_apple),3)
y_data.append(c)
e = new_round(float(count_vivo/sum_vivo),3)
y_data.append(e)
f = new_round(float(count_oppo/sum_oppo),3)
y_data.append(f)
g = new_round(float(count_svmsung/sum_svmsung),3)
y_data.append(g)
k = new_round(float(count_iphone/sum_iphone),3)
y_data.append(k)

y_data1 = []
l = new_round(float(count_huawei_poor/sum_huawei_poor),5)
y_data1.append(l)
q = new_round(float(count_mini_poor/sum_mini_poor),5)
y_data1.append(q)
w = new_round(float(count_apple_poor/sum_apple_poor),5)
y_data1.append(w)
r = new_round(float(count_vivo_poor/sum_vivo_poor),5)
y_data1.append(r)
t = new_round(float(count_oppo_poor/sum_oppo_poor),5)
y_data1.append(t)
y = new_round(float(count_svmsung_poor/sum_svmsung_poor),5)
y_data1.append(y)
u = new_round(float(count_iphone_poor/sum_iphone_poor),5)
y_data1.append(u)

y_data2 =[]
for y in y_data:
    y = y * 100
    y = new_round(float(y),2)
    y_data2.append(y)

y_data3 =[]
for y in y_data1:
    y = y * 100
    y = new_round(float(y),2)
    y_data3.append(y)


def main_scatter():
    c = (
        Scatter(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
            .add_xaxis(x_data)
            .add_yaxis("好评率", y_data2)
            .add_yaxis("差评率", y_data3)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各大手机厂商好评与差评占比"),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}%")),
            visualmap_opts=opts.VisualMapOpts(type_="size", max_=100, min_=0),
        )
    )
    return c
