from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import WordCloud
import jieba

# 读入停用词表
stop_words = []
with open("stopwords_cn.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        stop_words.append(line.strip())
my_stop_words = ['price', 'comment', '，', '、', '“', '”','万+','attribute','poorrate','goodrate']
stop_words.extend(my_stop_words)
word1 = []
for i in range(0,10000):
    i = str(i)
    word1.append(i)
stop_words.extend(word1)
with open('商品属性.text','r',encoding='utf-8')as f:
    content = f.readlines()

ditc = {}
for d in content:
    d = str(d)
    d = d.strip('\n')
    fenchi = jieba.lcut(d)
    for fen in fenchi:
        if fen not in stop_words and len(fen) >= 2:
            ditc[fen] = ditc.get(fen, 0) + 1
ls = list(ditc.items())
ls.sort(key=lambda x: x[1], reverse=True)


def main_word():
    c = (
        WordCloud(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
            .add(series_name="", data_pair=ls, word_size_range=[8, 88])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="", title_textstyle_opts=opts.TextStyleOpts(font_size=32)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )

    return c
