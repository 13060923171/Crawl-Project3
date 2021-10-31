import re
import pyecharts.options as opts
from pyecharts.charts import Radar
from pyecharts.globals import ThemeType

with open('商品属性.text','r',encoding='utf-8')as f:
    content = f.read()

#水滴屏
sum1 = re.compile('(水滴屏)')
sums = sum1.findall(content)
sum_1 = 0
sum_1 = len(sums)

#盲孔屏
sum2 = re.compile('(盲孔屏)')
sums_2 = sum2.findall(content)
sum_2 = 0
sum_2 = len(sums_2)


#极点屏
sum3 = re.compile('(极点屏)')
sums_3 = sum3.findall(content)
sum_3 = 0
sum_3 = len(sums_3)

#正常屏幕
sum4 = re.compile('(正常屏幕)')
sums_4 = sum4.findall(content)
sum_4 = 0
sum_4 = len(sums_4)

#瞳孔屏
sum5 = re.compile('(瞳孔屏)')
sums_5 = sum5.findall(content)
sum_5 = 0
sum_5 = len(sums_5)

#全面屏
sum6 = re.compile('(全面屏)')
sums_6 = sum6.findall(content)
sum_6 = 0
sum_6 = len(sums_6)

#刘海屏
sum7 = re.compile('(刘海屏)')
sums_7 = sum7.findall(content)
sum_7 = 0
sum_7 = len(sums_7)

#曲面屏
sum8 = re.compile('(曲面屏)')
sums_8 = sum8.findall(content)
sum_8 = 0
sum_8 = len(sums_8)

#开孔屏
sum9 = re.compile('(开孔屏)')
sums_9 = sum9.findall(content)
sum_9 = 0
sum_9 = len(sums_9)

#魅眼屏
sum10 = re.compile('(魅眼屏)')
sums_10 = sum10.findall(content)
sum_10 = 0
sum_10 = len(sums_10)

#老式屏幕
sum11 = re.compile('(老式屏幕)')
sums_11 = sum11.findall(content)
sum_11 = 0
sum_11 = len(sums_11)


#折叠幕
sum12 = re.compile('(折叠屏)')
sums_12 = sum12.findall(content)
sum_12 = 0
sum_12 = len(sums_12)

#珍珠屏
sum13 = re.compile('(珍珠屏)')
sums_13 = sum13.findall(content)
sum_13 = 0
sum_13 = len(sums_13)





data = [[sum_1,sum_2,sum_3,sum_4,sum_5,sum_6,sum_7,sum_8,sum_9,sum_10,sum_11,sum_12,sum_13]]

def main_radar():
    c = (
        # 创建雷达图，对雷达图进行设置大小和主题
        Radar(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
        .add_schema(
            schema=[
                # 雷达每个角对应的内容，和范围
                opts.RadarIndicatorItem(name="水滴屏", max_=500),
                opts.RadarIndicatorItem(name="盲孔屏", max_=500),
                opts.RadarIndicatorItem(name="极点屏", max_=500),
                opts.RadarIndicatorItem(name="正常屏幕", max_=500),
                opts.RadarIndicatorItem(name="瞳孔屏", max_=500),
                opts.RadarIndicatorItem(name="全面屏", max_=500),
                opts.RadarIndicatorItem(name="刘海屏", max_=500),
                opts.RadarIndicatorItem(name="曲面屏", max_=500),
                opts.RadarIndicatorItem(name="开孔屏", max_=500),
                opts.RadarIndicatorItem(name="魅眼屏", max_=500),
                opts.RadarIndicatorItem(name="老式屏幕", max_=500),
                opts.RadarIndicatorItem(name="折叠屏", max_=500),
                opts.RadarIndicatorItem(name="珍珠屏", max_=500),

            ],
            # 雷达图的文字和颜色选择
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            textstyle_opts=opts.TextStyleOpts(color="#fff"),
        )
        # 一个add对应一条雷达线
        .add(
            series_name="",
            data=data,
            linestyle_opts=opts.LineStyleOpts(color="#DA4B1E"),
        )
        # 设置雷达图的标题的大小和颜色以及位置
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return c
