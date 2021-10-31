import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.globals import ThemeType

df = pd.read_excel('商品属性.xls').loc[:,['品牌']]

list_name = []
count_mini = 0
count_huawei = 0
count_oppo = 0
count_vivo = 0
count_svmsung = 0
count_apple = 0
count_iphone = 0
for i in df['品牌']:
    i = str(i)
    if '小米' in i or '红米' in i:
        count_mini += 1
    elif 'OPPO' in i or 'oppo' in i:
        count_oppo += 1
    elif 'iQOO' in i or 'vivo' in i or '一加' in i:
        count_vivo += 1
    elif '华为' in i or '荣耀' in i:
        count_huawei += 1
    elif '苹果' in i or 'Apple' in i or 'iPhone' in i:
        count_apple += 1
    elif '三星' in i:
        count_svmsung += 1
    else:
        count_iphone += 1

x_data = ['小米','oppo','vivo','华为','苹果','三星','其他品牌手机']
y_data = [count_mini,count_oppo,count_vivo,count_huawei,count_apple,count_svmsung,count_iphone]

data_pair = [(i, int(j)) for i, j in zip(x_data, y_data)]


def main_pie():
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
        .add(
            "占比",
            data_pair,
            center=['50%','50%'],
            label_opts=opts.LabelOpts(is_show=True)
        )
        .set_colors(['SteelBlue','DarkCyan','DarkOrange','Salmon'])
        .set_global_opts(title_opts=opts.TitleOpts(title="不同品牌手机在平台占比",pos_left="center",
                pos_top="top",),legend_opts=opts.LegendOpts(is_show=False))
        .set_series_opts(tooltip_opts=opts.TooltipOpts(trigger='item',formatter="{a} <br/>{b}:{d}%"))
    )
    return c
