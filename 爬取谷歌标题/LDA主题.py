from gensim import corpora, models, similarities
import pyLDAvis
import pyLDAvis.gensim
import pandas as pd
import nltk
import re
from collections import Counter
from nltk.stem.snowball import SnowballStemmer  # 返回词语的原型，去掉ing等
import itertools
import matplotlib.pyplot as plt
import numpy as np
import re
import pandas as pd
import os

df = pd.read_csv('new_data.csv')


def lda():
    f = open('result-fenci.txt', 'w', encoding='utf-8-sig')
    for line in df['comment']:
        tokens = nltk.word_tokenize(line)
        # 计算关键词
        all_words = tokens
        c = Counter()
        for x in all_words:
            if len(x) > 1 and x != '\r\n' and x != '\n':
                c[x] += 1
        # Top50
        output = ""
        # print('\n词频统计结果：')
        for (k, v) in c.most_common(30):
            # print("%s:%d"%(k,v))
            output += k + " "

        f.write(output + "\n")

    else:
        f.close()

    fr = open('result-fenci.txt', 'r',encoding='utf-8-sig')
    train = []
    for line in fr.readlines():
        line = [word.strip() for word in line.split(' ')]
        line1 = [l for l in line if len(l) >= 1]
        train.append(line1)
    print(train)
    dictionary = corpora.Dictionary(train)
    corpus = [dictionary.doc2bow(text) for text in train]

    # 构造主题数寻优函数
    def cos(vector1, vector2):  # 余弦相似度函数
        dot_product = 0.0
        normA = 0.0
        normB = 0.0
        for a, b in zip(vector1, vector2):
            dot_product += a * b
            normA += a ** 2
            normB += b ** 2
        if normA == 0.0 or normB == 0.0:
            return (None)
        else:
            return (dot_product / ((normA * normB) ** 0.5))

        # 主题数寻优

    def lda_k(x_corpus, x_dict):
        # 初始化平均余弦相似度
        mean_similarity = []
        mean_similarity.append(1)

        # 循环生成主题并计算主题间相似度
        for i in np.arange(2, 11):
            lda = models.LdaModel(x_corpus, num_topics=i, id2word=x_dict)  # LDA模型训练
            for j in np.arange(i):
                term = lda.show_topics(num_words=50)

            # 提取各主题词
            top_word = []
            for k in np.arange(i):
                top_word.append([''.join(re.findall('"(.*)"', i)) \
                                 for i in term[k][1].split('+')])  # 列出所有词

            # 构造词频向量
            word = sum(top_word, [])  # 列出所有的词
            unique_word = set(word)  # 去除重复的词

            # 构造主题词列表，行表示主题号，列表示各主题词
            mat = []
            for j in np.arange(i):
                top_w = top_word[j]
                mat.append(tuple([top_w.count(k) for k in unique_word]))

            p = list(itertools.permutations(list(np.arange(i)), 2))
            l = len(p)
            top_similarity = [0]
            for w in np.arange(l):
                vector1 = mat[p[w][0]]
                vector2 = mat[p[w][1]]
                top_similarity.append(cos(vector1, vector2))

            # 计算平均余弦相似度
            mean_similarity.append(sum(top_similarity) / l)
        return (mean_similarity)

    # 计算主题平均余弦相似度
    word_k = lda_k(corpus, dictionary)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10, 8), dpi=300)
    plt.plot(word_k)
    plt.title('LDA评论主题数寻优')
    plt.xlabel('主题数')
    plt.ylabel('平均余弦相似度')
    plt.savefig('LDA评论主题数寻优.png')
    plt.show()

    topic_lda = word_k.index(min(word_k)) + 1

    lda = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=5)

    data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.save_html(data, './data/LDA.html')


lda()

