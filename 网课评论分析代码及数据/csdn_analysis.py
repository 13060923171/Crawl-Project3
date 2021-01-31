'''
作者 : 丁毅
开发时间 : 2020/12/26 11:57
'''

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud
from PIL import Image
import matplotlib

plt.rcParams['font.family'] = 'SimHei'

# 课程评分分析
def course_rating():
    df = pd.read_csv(r'./数据/merge_course.csv', usecols=['platform', 'rating'])
    df = df.loc[df['platform'] == 'imooc'].head(500)

    section1 = len(df[df['rating'] >= 4.75])
    section2 = len(df[(df['rating'] < 4.75) & (df['rating'] >= 4.5)])
    section3 = len(df[(df['rating'] < 4.5)])
    print(section1,section2,section3)


# 绘制饼图
def draw_Pie_chart():
    # 绘制饼图

    colors = ['cornflowerblue', 'limegreen', 'orange']
    # 一些数据
    labels = ['4.75以上', '4.5~4.75', '4.5以下']
    fracs_imooc = [362, 112, 26]
    fracs_mooc163 = [390, 104, 6]
    # 制作图形和坐标轴
    fig, axs = plt.subplots(1, 2)
    # 一个标准的饼图
    axs[0].pie(fracs_imooc, labels=labels, autopct='%.2f%%', colors=colors, explode=(0, 0, 0.1))
    # 使用explode移动第二个切片
    axs[1].pie(fracs_mooc163, labels=labels, autopct='%.2f%%', colors=colors, explode=(0, 0, 0.1))
    axs[0].set_title('imooc')
    axs[1].set_title('study163')
    plt.savefig(r'./数据/Pie_chart.jpg', dpi=1000)
    plt.show()


# 评论人名称分析
def user_name():
    df = pd.read_csv(r'./数据/new_merge_comment.csv', low_memory=False, usecols=['platform', 'user_name'])
    df = df.loc[df['platform'] == 'mooc163', :]
    df.dropna(inplace=True)
    df.drop_duplicates(keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df.head(30000)
    chinese_name = []

    for name in df['user_name'].values:
        if re.findall(r'[\u4e00-\u9fff]', name):
            chinese_name.append(name)

    pure_chinese_name = []
    for name in chinese_name:
        if name == ''.join(re.findall(r'[\u4e00-\u9fff]', name)):
            pure_chinese_name.append(name)
    print(30000 - len(chinese_name))
    print(len(pure_chinese_name))

    #         imooc      icourse   mooc163
    # 纯字符名称 9991      12892     13737
    # 纯中文     9649      7079      7482
    # 混合      10360     10029      8781


# 绘制命名柱状图
def draw_name_Histogram():
    labels = ['imooc', 'icourse', 'study163']

    character = [9991, 12892, 13737]
    chinese = [9649, 7079, 7482]
    mix = [10360, 10029, 8781]

    x = np.arange(len(labels))  # 标签的位置
    width = 0.2  # 柱的宽度

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, character, width, label='字符')
    rects2 = ax.bar(x, chinese, width, label='中文')
    rects3 = ax.bar(x + width, mix, width, label='混合')

    # 为标签、标题和自定义x轴标记标签等添加一些文本。
    ax.set_ylabel('人数')
    ax.set_title('用户昵称格式')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        # 在每个矩形栏的上方附上一个文本标签，显示它的高度。
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3点的垂直偏移量
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    fig.tight_layout()
    plt.savefig(r'./数据/name_style.jpg', dpi=1000)
    plt.show()


# 各平台评论高频消极积极词汇词云图
def high_frequency_words():
    df = pd.read_csv(r'./数据/new_Chinese_comment3.csv', low_memory=False,
                     usecols=['platform', 'high_frequency_words_up', 'high_frequency_words_down'])
    df['high_frequency_words_up'] = df['high_frequency_words_up'] + ','
    df['high_frequency_words_down'] = df['high_frequency_words_down'] + ','

    df_by_platform = df.groupby(['platform']).sum().reset_index(drop=None)
    imooc_up_list = df_by_platform.loc[df_by_platform['platform'] == 'imooc', ['high_frequency_words_down']][
        'high_frequency_words_down'].tolist()
    imooc_up_list = imooc_up_list[0].split(',')
    imooc_up_list.pop()
    while True:
        try:
            imooc_up_list.remove('厉害')
        except:
            break
    while True:
        try:
            imooc_up_list.remove('东西')
        except:
            break
    imooc_up_str = ' '.join(imooc_up_list)
    # color_mask = np.array(Image.open(r'C:\\Users\pc\Desktop\爱心.png'))
    word = WordCloud(max_words=100,
                     max_font_size=200,
                     width=1000, \
                     height=800,
                     font_path='C:\Windows\Fonts\simhei.ttf',
                     ).generate(imooc_up_str)
    word.to_file(r"./数据/imooc_down.png")


# 评论平均长度分析
def comment_average_length():
    # 评论平均长度
    df = pd.read_csv(r'./数据/new_Chinese_comment3.csv', low_memory=False,
                     usecols=['platform', 'average_length'])
    df = df.groupby('platform').describe().reset_index(drop=None)
    print(df)
    # icourse 23
    # imooc 19
    # keqq 32
    # mooc163 24


# 绘制评论平均长度柱状图
def draw_Histogram():
    labels = ['imooc', 'icourse', 'keqq', 'study163']
    length = [19, 23, 32, 24]

    x = np.arange(len(labels))  # 标签的位置
    width = 0.35  # 柱的宽度

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, length, width)

    # 为标签、标题和自定义x轴标记标签等添加一些文本。
    ax.set_ylabel('评论长度')
    ax.set_title('各平台评论平均长度')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    # ax.legend()

    def autolabel(rects):
        # 在每个矩形栏的上方附上一个文本标签，显示它的高度。
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3点的垂直偏移量
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)

    fig.tight_layout()
    plt.grid(alpha=0.5)
    plt.savefig(r'./数据/comment_length.jpg', dpi=1000)
    plt.show()


# 评论数与课程评分之间的关系
def comment_rating_relation():
    df = pd.read_csv(r'./数据/merge_course.csv', low_memory=False,
                     usecols=['platform', 'course_name', 'course_id', 'rating'])
    df = df.loc[df['platform'] == 'mooc163'].reset_index(drop=None).head(200)
    df_comment = pd.read_csv(r'./数据/new_merge_comment.csv', low_memory=False,
                             usecols=['platform', 'course_id', 'comment'])
    df_comment = df_comment.loc[df_comment['platform'] == 'mooc163']
    series = df_comment.groupby('course_id')['comment'].count()

    df_comment = pd.DataFrame()
    df_comment['course_id'] = series.index
    df_comment['count'] = series.values
    df_comment['course_id'] = df_comment['course_id'].str.extract('^(\d+)', expand=True)
    new_df = pd.merge(df, df_comment, on='course_id')

    rating_list = new_df['rating'].values.tolist()  # 课程评分
    count_list = new_df['count'].values.tolist()  # 课程评论

    x = rating_list
    y = count_list

    fig, ax = plt.subplots()
    plt.title('课程评分与评论数量之间的关系')
    plt.xlabel('课程评分')
    plt.ylabel('评论数量')
    plt.plot(x, y, 'o')
    plt.show()


def main():
    course_rating()
    comment_rating_relation()
    draw_Pie_chart()
    user_name()
    draw_name_Histogram()
    high_frequency_words()
    comment_average_length()


if __name__=='__main__':
    main()