import jieba
import pandas as pd
import stylecloud
from IPython.display import Image

df = pd.read_excel('招聘数据-聚类.xlsx')
df['fullcontent'] = df['fullcontent'].astype(str)
def get_cut_words(content_series):
    # 读入停用词表
    stop_words = []

    with open("stopwords_cn.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            stop_words.append(line.strip())

    # 分词
    word_num = jieba.lcut(content_series['fullcontent'].str.cat(sep='。'), cut_all=False)

    # 条件筛选
    word_num_selected = [i for i in word_num if i not in stop_words and len(i) >= 2]
    return word_num_selected

compan = df.groupby('聚类结果').apply(get_cut_words)
y_data1 = list(compan.values)[0]
y_data2 = list(compan.values)[1]
y_data3 = list(compan.values)[2]
y_data4 = list(compan.values)[3]

counts1 = {}
counts2 = {}
counts3 = {}
counts4 = {}

def main1():
    for y in y_data1:
        counts1[y] = counts1.get(y,0)+1

    ls = list(counts1.items())
    ls.sort(key=lambda x:x[1],reverse=True)
    x_data = []
    y_data = []
    for key,values in ls:
        x_data.append(key)
        y_data.append(values)

    df1 = pd.DataFrame()
    df1['word'] = x_data[:200]
    df1['counts'] = y_data[:200]
    df1.to_excel('./聚类-data/0类高词频.xlsx')


def main2():
    for y in y_data2:
        counts2[y] = counts2.get(y, 0) + 1

    ls = list(counts2.items())
    ls.sort(key=lambda x: x[1], reverse=True)
    x_data = []
    y_data = []
    for key, values in ls:
        x_data.append(key)
        y_data.append(values)

    df1 = pd.DataFrame()
    df1['word'] = x_data[:200]
    df1['counts'] = y_data[:200]
    df1.to_excel('./聚类-data/1类高词频.xlsx')


def main3():
    for y in y_data3:
        counts3[y] = counts3.get(y, 0) + 1

    ls = list(counts3.items())
    ls.sort(key=lambda x: x[1], reverse=True)
    x_data = []
    y_data = []
    for key, values in ls:
        x_data.append(key)
        y_data.append(values)

    df1 = pd.DataFrame()
    df1['word'] = x_data[:200]
    df1['counts'] = y_data[:200]
    df1.to_excel('./聚类-data/2类高词频.xlsx')


def main4():
    for y in y_data4:
        counts4[y] = counts4.get(y, 0) + 1

    ls = list(counts4.items())
    ls.sort(key=lambda x: x[1], reverse=True)
    x_data = []
    y_data = []
    for key, values in ls:
        x_data.append(key)
        y_data.append(values)

    df1 = pd.DataFrame()
    df1['word'] = x_data[:200]
    df1['counts'] = y_data[:200]
    df1.to_excel('./聚类-data/3类高词频.xlsx')

if __name__ == '__main__':
    main1()
    main2()
    main3()
    main4()
