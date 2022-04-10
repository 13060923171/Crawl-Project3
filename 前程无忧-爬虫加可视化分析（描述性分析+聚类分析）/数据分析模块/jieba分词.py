import jieba
import pandas as pd
import stylecloud
from IPython.display import Image

df = pd.read_excel('招聘数据-聚类.xlsx')
df['fullcontent'] = df['fullcontent'].astype(str)
print(df['fullcontent'])
def get_cut_words(content_series):
    # 读入停用词表
    stop_words = []

    with open("stopwords_cn.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            stop_words.append(line.strip())

    def is_all_chinese(strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True
    # 分词
    word_num = jieba.lcut(content_series['fullcontent'].str.cat(sep='。'), cut_all=False)

    # 条件筛选
    word_num_selected = [i for i in word_num if i not in stop_words and len(i) >= 2 and is_all_chinese(i) == True]
    return word_num_selected

compan = df.groupby('聚类结果').apply(get_cut_words)
print(compan)
y_data1 = list(compan.values)[0]
y_data2 = list(compan.values)[1]
y_data3 = list(compan.values)[2]
y_data4 = list(compan.values)[3]

def main1():
    # 绘制词云图
    stylecloud.gen_stylecloud(text=','.join(y_data1), max_words=100,
                              collocations=False,
                              font_path='simhei.ttf',
                              icon_name='fas fa-circle',
                              size=500,
                              # palette='matplotlib.Inferno_9',
                              output_name='./聚类-data/聚类1-云图.png')
    Image(filename='./聚类-data/聚类1-云图.png')

def main2():
    # 绘制词云图
    stylecloud.gen_stylecloud(text=','.join(y_data2), max_words=100,
                              collocations=False,
                              font_path='simhei.ttf',
                              icon_name='fas fa-archway',
                              size=500,
                              # palette='matplotlib.Inferno_9',
                              output_name='./聚类-data/聚类2-云图.png')
    Image(filename='./聚类-data/聚类2-云图.png')


def main3():
    # 绘制词云图
    stylecloud.gen_stylecloud(text=','.join(y_data3), max_words=100,
                              collocations=False,
                              font_path='simhei.ttf',
                              icon_name='fas fa-bell',
                              size=500,
                              # palette='matplotlib.Inferno_9',
                              output_name='./聚类-data/聚类3-云图.png')
    Image(filename='./聚类-data/聚类3-云图.png')

def main4():
    # 绘制词云图
    stylecloud.gen_stylecloud(text=','.join(y_data4), max_words=100,
                              collocations=False,
                              font_path='simhei.ttf',
                              icon_name='fas fa-heart',
                              size=500,
                              # palette='matplotlib.Inferno_9',
                              output_name='./聚类-data/聚类4-云图.png')
    Image(filename='./聚类-data/聚类4-云图.png')


if __name__ == '__main__':
    main1()
    main2()
    main3()
    main4()