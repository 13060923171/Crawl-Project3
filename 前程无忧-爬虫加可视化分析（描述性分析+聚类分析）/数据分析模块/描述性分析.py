import pandas as pd
import matplotlib.pyplot as plt
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
from pyecharts import options as opts
import stylecloud
from IPython.display import Image
plt.rcParams['font.sans-serif']=['SimHei']

df = pd.read_excel('招聘数据.xlsx')


def company_number():
    company_pie = df['city_type'].value_counts()
    x_data = [i for i in company_pie.index]
    y_data = [i for i in company_pie.values]

    plt.figure(figsize=(12, 9),dpi=300)  # 调节图形大小
    labels = x_data  # 定义标签
    sizes = y_data  # 每块值
    explode = (0, 0.05, 0, 0)  # 将某一块分割出来，值越大分割出的间隙越大
    colors = ['Cyan', 'CadetBlue', 'SteelBlue', 'DeepSkyBlue']
    patches, text1, text2 = plt.pie(sizes,
                                    explode=explode,
                                    labels=labels,
                                    colors=colors,
                                    labeldistance=1.1,  # 图例距圆心半径倍距离
                                    autopct='%3.2f%%',  # 数值保留固定小数位
                                    shadow=False,  # 无阴影设置
                                    startangle=90,  # 逆时针起始角度设置
                                    pctdistance=0.6)  # 数值距圆心半径倍数距离
    # patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部文本
    # x，y轴刻度设置一致，保证饼图为圆形
    plt.axis('equal')
    plt.legend()
    plt.title('城市类型与企业数量占比')
    plt.savefig('./data/城市类型与企业数量占比.jpg')
    plt.show()


def city_word():
    # 绘制词云图
    text1 = list(df['place'])


    stylecloud.gen_stylecloud(text=','.join(text1), max_words=100,
                              collocations=False,
                              font_path='simhei.ttf',
                              icon_name='fas fa-globe',
                              size=500,
                              # palette='matplotlib.Inferno_9',
                              output_name='./data/城市频数-云图.png')
    Image(filename='./data/城市频数-云图.png')


def city_china():
    text1 = list(df['place'])
    counts = {}
    for t in text1:
        counts[t] = counts.get(t,0)+1
    ls = list(counts.items())
    ls.sort(key=lambda x: x[0], reverse=True)
    c = (
        Geo()
        .add_schema(
            maptype="china",
            itemstyle_opts=opts.ItemStyleOpts(color="#323c48", border_color="#111"),
        )
        .add(
            "",
            ls,
            type_=ChartType.EFFECT_SCATTER,
            color="red",
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="岗位分布情况"))
        .render("./data/岗位分布情况.html")
    )

def company_people():
    def compan_class(x):
        df1 = x
        counts = {}
        comlabel = df1['comGuimo']
        list_sum = []
        for c in comlabel:
            c = str(c)
            list_sum.append(c)

        for l in list_sum:
            counts[l] = counts.get(l,0)+1

        ls = list(counts.items())
        ls.sort(key=lambda x:x[0],reverse=True)
        ls[3],ls[1] = ls[1],ls[3]
        ls[2], ls[4] = ls[4], ls[2]
        ls[4], ls[3] = ls[3], ls[4]
        ls[4], ls[5] = ls[5], ls[4]
        ls[5], ls[6] = ls[6], ls[5]
        return ls



    compan = df.groupby('city_type').apply(compan_class)
    x_data = [i[0] for i in list(compan.values)[0]]
    y_data1 = [i[1] for i in list(compan.values)[0]]
    y_data2 = [i[1] for i in list(compan.values)[1]]
    y_data3 = [i[1] for i in list(compan.values)[2]]
    y_data4 = [i[1] for i in list(compan.values)[3]]

    c = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis("{}".format(list(compan.index)[0]), y_data1)
        .add_yaxis("{}".format(list(compan.index)[1]), y_data2)
        .add_yaxis("{}".format(list(compan.index)[2]), y_data3)
        .add_yaxis("{}".format(list(compan.index)[3]), y_data4)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
            title_opts=opts.TitleOpts(title="企业规模在四类城市分别情况"),
        )
        .render("./data/企业规模在四类城市分别情况.html")
    )



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



    education = df.groupby('city_type').apply(education_class)
    x_data = [i[0] for i in list(education.values)[0]]
    y_data1 = [i[1] for i in list(education.values)[0]]
    y_data2 = [i[1] for i in list(education.values)[1]]
    y_data3 = [i[1] for i in list(education.values)[2]]
    y_data4 = [i[1] for i in list(education.values)[3]]

    c = (
        Bar()
            .add_xaxis(x_data)
            .add_yaxis("{}".format(list(education.index)[0]), y_data1)
            .add_yaxis("{}".format(list(education.index)[1]), y_data2)
            .add_yaxis("{}".format(list(education.index)[2]), y_data3)
            .add_yaxis("{}".format(list(education.index)[3]), y_data4)
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
            title_opts=opts.TitleOpts(title="学历要求在四类城市的分别情况"),
        )
            .render("./data/学历要求在四类城市的分别情况.html")
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



    work = df.groupby('city_type').apply(work_class)
    x_data = [i[0] for i in list(work.values)[0]]
    y_data1 = [i[1] for i in list(work.values)[0]]
    y_data2 = [i[1] for i in list(work.values)[1]]
    y_data3 = [i[1] for i in list(work.values)[2]]
    y_data4 = [i[1] for i in list(work.values)[3]]

    c = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis("{}".format(list(work.index)[0]), y_data1, is_smooth=True)
        .add_yaxis("{}".format(list(work.index)[1]), y_data2, is_smooth=True)
        .add_yaxis("{}".format(list(work.index)[2]), y_data3, is_smooth=True)
        .add_yaxis("{}".format(list(work.index)[3]), y_data4, is_smooth=True)
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
            .render("./data/工作经验在四类城市分别情况.html")
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



    pay = df.groupby('city_type').apply(pay_class)
    x_data = [i[0] for i in list(pay.values)[0]]
    y_data1 = [i[1] for i in list(pay.values)[0]]
    y_data2 = [i[1] for i in list(pay.values)[1]]
    y_data3 = [i[1] for i in list(pay.values)[2]]
    y_data4 = [i[1] for i in list(pay.values)[3]]

    c = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis("{}".format(list(pay.index)[0]), y_data1, is_smooth=True)
            .add_yaxis("{}".format(list(pay.index)[1]), y_data2, is_smooth=True)
            .add_yaxis("{}".format(list(pay.index)[2]), y_data3, is_smooth=True)
            .add_yaxis("{}".format(list(pay.index)[3]), y_data4, is_smooth=True)
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
            .render("./data/四类城市薪资分别情况.html")
    )






if __name__ == '__main__':
    company_number()
    company_people()
    education_type()
    work_type()
    pay_type()
    city_word()
    city_china()