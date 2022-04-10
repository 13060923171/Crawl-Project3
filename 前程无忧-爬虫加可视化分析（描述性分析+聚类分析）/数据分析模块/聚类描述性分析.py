import pandas as pd
import matplotlib.pyplot as plt
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts import options as opts
plt.rcParams['font.sans-serif']=['SimHei']

df = pd.read_excel('招聘数据-聚类.xlsx')

x_data1 = ['数据开发类','数据管理类','数据技能类','数据分析类']

def education_type():
    def education_class(x):
        df1 = x
        counts = {}
        comlabel = df1['jingyan']
        list_sum = []
        for c in comlabel:
            c = str(c)
            list_sum.append(c)

        for l in list_sum:
            counts[l] = counts.get(l,0)+1

        ls = list(counts.items())
        ls.sort(key=lambda x:x[1],reverse=True)

        return ls


    education = df.groupby('聚类结果').apply(education_class)
    x_data = [i[0] for i in list(education.values)[0]]
    y_data1 = [i[1] for i in list(education.values)[0]]
    y_data2 = [i[1] for i in list(education.values)[1]]
    y_data3 = [i[1] for i in list(education.values)[2]]
    y_data4 = [i[1] for i in list(education.values)[3]]

    c = (
        Bar()
            .add_xaxis(x_data)
            .add_yaxis("{}".format(x_data1[0]), y_data1)
            .add_yaxis("{}".format(x_data1[1]), y_data2)
            .add_yaxis("{}".format(x_data1[2]), y_data3)
            .add_yaxis("{}".format(x_data1[3]), y_data4)
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
            title_opts=opts.TitleOpts(title="学历要求在四类城市的分别情况"),
        )
            .render("./聚类-data/学历要求在四类城市的分别情况.html")
    )


def work_type():
    def work_class(x):
        df1 = x
        counts = {}
        comlabel = df1['xueli']
        list_sum = []
        for c in comlabel:
            c = str(c)
            list_sum.append(c)

        for l in list_sum:
            counts[l] = counts.get(l,0)+1

        ls = list(counts.items())
        ls.sort(key=lambda x:x[0],reverse=True)
        ls[6],ls[2] = ls[2],ls[6]
        ls[5], ls[3] = ls[3], ls[5]
        return ls



    work = df.groupby('聚类结果').apply(work_class)
    x_data = [i[0] for i in list(work.values)[0]]
    y_data1 = [i[1] for i in list(work.values)[0]]
    y_data2 = [i[1] for i in list(work.values)[1]]
    y_data3 = [i[1] for i in list(work.values)[2]]
    y_data4 = [i[1] for i in list(work.values)[3]]

    c = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis("{}".format(x_data1[0]), y_data1, is_smooth=True)
        .add_yaxis("{}".format(x_data1[1]), y_data2, is_smooth=True)
        .add_yaxis("{}".format(x_data1[2]), y_data3, is_smooth=True)
        .add_yaxis("{}".format(x_data1[3]), y_data4, is_smooth=True)
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="工作经验在四类城市分别情况"),
            xaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                is_scale=False,
                boundary_gap=False,
            ),
        )
            .render("./聚类-data/工作经验在四类城市分别情况.html")
    )



def pay_type():
    def handle_min(text):
        if type(text) == float:
            return '-'
        if text.strip().endswith("千/月"):
            salary = text.replace("千/月", '').split("-")[0]
            return float(salary) * 1000
        elif text.strip().endswith("万/月"):
            salary = text.replace("万/月", '').split("-")[0]
            return float(salary) * 10000
        elif text.strip().endswith("万/年"):
            salary = text.replace("万/年", '').split("-")[0]
            return float(salary) * 10000 / 12
        elif text.strip().endswith("元/天"):
            salary = text.replace("元/天", '').split("-")[0]
            return float(salary) * 30
        elif text.strip().endswith("万以上/年"):
            salary = text.replace("万以上/年", '').split("-")[0]
            return float(salary) * 10000 / 12

    def handle_max(text):
        if type(text) == float:
            return '-'
        if text.strip().endswith("千/月"):
            salary = text.replace("千/月", '').split("-")[-1]
            return float(salary) * 1000
        elif text.strip().endswith("万/月"):
            salary = text.replace("万/月", '').split("-")[-1]
            return float(salary) * 10000
        elif text.strip().endswith("万/年"):
            salary = text.replace("万/年", '').split("-")[-1]
            return float(salary) * 10000 / 12
        elif text.strip().endswith("元/天"):
            salary = text.replace("元/天", '').split("-")[-1]
            return float(salary) * 30
        elif text.strip().endswith("万以上/年"):
            salary = text.replace("万以上/年", '').split("-")[-1]
            return float(salary) * 10000 / 12

    def salary_type(x):
        if float(x) < 10000:
            return '一万以下'
        elif 10000 <= float(x) < 20000:
            return '一万到二万之间'
        elif 20000 <= float(x) < 30000:
            return '二万到三万之间'
        elif 30000 <= float(x) < 40000:
            return '三万到四万之间'
        elif 40000 <= float(x) < 50000:
            return '四万到五万之间'
        else:
            return '五万以上'

    df["min_salary"] = df["providesalary_text"].apply(handle_min)
    df["max_salary"] = df["providesalary_text"].apply(handle_max)
    df['salary'] = df["max_salary"].apply(salary_type)
    def pay_class(x):
        df1 = x
        counts = {}
        comlabel = df1['salary']

        list_sum = []
        for c in comlabel:
            c = str(c)
            list_sum.append(c)

        for l in list_sum:
            counts[l] = counts.get(l,0)+1

        ls = list(counts.items())
        ls.sort(key=lambda x:x[0],reverse=False)
        ls[2], ls[3] = ls[3], ls[2]
        return ls



    pay = df.groupby('聚类结果').apply(pay_class)
    x_data = [i[0] for i in list(pay.values)[0]]
    y_data1 = [i[1] for i in list(pay.values)[0]]
    y_data2 = [i[1] for i in list(pay.values)[1]]
    y_data3 = [i[1] for i in list(pay.values)[2]]
    y_data4 = [i[1] for i in list(pay.values)[3]]

    c = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis("{}".format(x_data1[0]), y_data1, is_smooth=True)
            .add_yaxis("{}".format(x_data1[1]), y_data2, is_smooth=True)
            .add_yaxis("{}".format(x_data1[2]), y_data3, is_smooth=True)
            .add_yaxis("{}".format(x_data1[3]), y_data4, is_smooth=True)
            .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="四类城市薪资分别情况"),
            xaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                is_scale=False,
                boundary_gap=False,
            ),
        )
        .render("./聚类-data/四类城市薪资分别情况.html")
    )


if __name__ == '__main__':
    education_type()
    work_type()
    pay_type()
