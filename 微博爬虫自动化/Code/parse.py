import pandas as pd
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.style.use('ggplot')
#设置字体为楷体

class Parse:

    def plot1(self):
        """
            微博关键词疫情实时舆情词云、词频统计
        :return:
        """
        df = pd.read_csv("../static/疫情关键词实时舆论.csv", encoding="utf-8")
        text_list = df['content'].values.tolist()

        # 创建停用词列表
        def get_stopwords_list():
            stopwords = [line.strip() for line in open('stopwords.txt', encoding='UTF-8').readlines()]
            return stopwords

        stopwords = get_stopwords_list()

        def seg_depart(sentence):
            # 对文档中的每一行进行中文分词
            sentence_depart = jieba.lcut(sentence)
            return sentence_depart
        text_list = [str(i).replace('#', '').strip().replace("【", "").replace("】", "") for i in text_list]
        text_list2 = []
        for text in text_list:
            text = seg_depart(text)
            for index, one in enumerate(text):
                if one not in stopwords:
                    item = {
                        '序号': index,
                        '词语': one
                    }
                    text_list2.append(item)
        df = pd.DataFrame(text_list2)
        row_df = df.groupby('词语').count().sort_values('序号', ascending=False)
        row_df.reset_index(inplace=True)
        row_df.columns = ['词语', '次数']
        row_df_TOP_20 = row_df.head(20)
        plt.figure(figsize=(15, 10))
        plt.title('词频TOP20柱状图')
        plt.bar(list(row_df_TOP_20['词语'].values), list(row_df_TOP_20['次数'].values),color="skyblue")
        plt.ylabel('词频')
        plt.xlabel('词语')
        plt.savefig("../static/疫情关键词高频词统计")
        print("词频TOP20柱状图保存成功！")
        c_text = ' '.join(row_df['词语'].values)
        wordc = WordCloud(background_color="white",
                          width=1000,
                          height=1000,
                          font_path='simhei.ttf',
                          ).generate(c_text[:1000])
        wordc.to_file("../static/微博疫情关键词舆情词云图.jpg")    #保存为图片
        print("微博疫情关键词舆情词云图保存成功！")



    def pie1(self):
        """
            舆情来源占比分析
        :return:
        """
        df = pd.read_csv("../static/疫情关键词实时舆论.csv", encoding="utf-8")
        f = [str(i) if "iPhone" not in str(i) else "iPhone客户端" for i in df['f'].values.tolist()]
        df['f'] = f
        new_df = df.groupby("f").count().sort_values("name", ascending=False)
        new_df.reset_index(inplace=True)
        new_df = new_df[['f', "name"]]
        new_df.columns = ['来源', '次数']
        r_df = new_df[:20]
        import numpy as np
        # np.hstack():在水平方向上拼接数组
        explode = np.hstack((np.zeros(6), np.linspace(0, 2.5, len(r_df) - 6)))  # (每一块)离开中心距离
        plt.figure(figsize=(15, 10))
        plt.title("微博舆情群体饼状图", fontsize=20)
        plt.pie(r_df['次数'], labels=r_df['来源'], autopct='%1.1f%%', textprops={'fontsize': 16}, explode=explode);
        plt.savefig("../static/舆情来源占比图.jpg")
        print("舆情来源占比图保存成功!")


if __name__ == '__main__':
    obj = Parse()
    obj.plot1()
    obj.pie1()



