import pandas as pd
from pyecharts.globals import ThemeType
import pyecharts.options as opts
from pyecharts.charts import Line

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

d = {}
for i in range(len(list_comment)):
    d[list_title[i]] = list_comment[i]

ls = list(d.items())
ls.sort(key=lambda x: x[1], reverse=True)
ls = ls[0:15]
x_data = []
y_data = []

for l in range(len(ls)):
    x = ls[l][0]
    x = x.replace('4G','').replace('i','').replace('5z','')
    x_data.append(x)
    y = ls[l][1]
    y_data.append(y)

def main_line():
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="",
            symbol="emptyCircle",
            is_symbol_show=False,
            color="#d14a61",
            y_axis=y_data,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=5)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="销量最高的前15部手机"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False, axisline_opts=opts.AxisLineOpts(
                is_on_zero=False, linestyle_opts=opts.LineStyleOpts(color="#d14a61")
            ),axislabel_opts=opts.LabelOpts(rotate=-25)),
        )
    )
    return c

