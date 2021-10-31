import re
import pyecharts.options as opts
from pyecharts.charts import Funnel
from pyecharts.globals import ThemeType

with open('商品属性.text','r',encoding='utf-8')as f:
    content = f.read()

sum1 = re.compile('(人脸识别)')
sums = sum1.findall(content)
sum_1 = 0
sum_1 = len(sums)


sum2 = re.compile('(NFC)',re.S|re.I)
sums_2 = sum2.findall(content)
sum_2 = 0
sum_2 = len(sums_2)


sum3 = re.compile('(快速充电)')
sums_3 = sum3.findall(content)
sum_3 = 0
sum_3 = len(sums_3)


sum4 = re.compile('(无线充电)')
sums_4 = sum4.findall(content)
sum_4 = 0
sum_4 = len(sums_4)


sum5 = re.compile('(液冷散热)')
sums_5 = sum5.findall(content)
sum_5 = 0
sum_5 = len(sums_5)

sum6 = re.compile('(高倍率变焦)')
sums_6 = sum6.findall(content)
sum_6 = 0
sum_6 = len(sums_6)

sum7 = re.compile('(屏幕指纹)')
sums_7 = sum7.findall(content)
sum_7 = 0
sum_7 = len(sums_7)


sum8 = re.compile('(防水防尘)')
sums_8 = sum8.findall(content)
sum_8 = 0
sum_8 = len(sums_8)


sum9 = re.compile('(隔空操作)')
sums_9 = sum9.findall(content)
sum_9 = 0
sum_9 = len(sums_9)


sum10 = re.compile('(5G)',re.I|re.S)
sums_10 = sum10.findall(content)
sum_10 = 0
sum_10 = len(sums_10)


sum11 = re.compile('(超高屏占比)')
sums_11 = sum11.findall(content)
sum_11 = 0
sum_11 = len(sums_11)


sum12 = re.compile('(弹出式摄像头)')
sums_12 = sum12.findall(content)
sum_12 = 0
sum_12 = len(sums_12)

sum13 = re.compile('(屏幕高刷新率)')
sums_13 = sum13.findall(content)
sum_13 = 0
sum_13 = len(sums_13)

x_data = ['人脸识别','NFC','快速充电','无线充电','液冷散热','高倍率变焦','屏幕指纹','防水防尘','隔空操作','5G','超高屏占比','弹出式摄像头','屏幕高刷新率']
y_data = [sum_1,sum_2,sum_3,sum_4,sum_5,sum_6,sum_7,sum_8,sum_9,sum_10,sum_11,sum_12,sum_13]


def main_funnel():
    c = (
        Funnel(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
            .add(
            "手机热点占比",
            [list(z) for z in zip(x_data, y_data)],
            label_opts=opts.LabelOpts(position="inside"),
        )
    )
    return c

