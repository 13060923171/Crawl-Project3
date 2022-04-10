import jieba
import pandas as pd
# coding=utf-8
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# 对原文本分词
def cut_words():
    # 获取当前文件路径
    df = pd.read_excel('招聘数据.xlsx').loc[:,['fullcontent']]
    text1 = df.astype('str').values
    content = ''
    for t in text1:
        text = jieba.cut(t[0], cut_all=False)
        for i in text:
            content += i
            content += " "
        content += "\n"
    return content

# 加载stopwords
def load_stopwords():
    filepath = r'stopwords_cn.txt'
    stopwords = [line.strip() for line in open(
        filepath, encoding='utf-8').readlines()]
    return stopwords

# 去除原文stopwords,并生成新的文本
def move_stopwwords(content, stopwords):
    content_after = ''
    for word in content:
        if word not in stopwords:
            # if word != '\t'and'\n':
            content_after += word

    # 写入去停止词后生成的新文本
    with open('数据.txt', 'w', encoding='UTF-8-SIG') as f:
        f.write(content_after)

content = cut_words()
stopwords = load_stopwords()
move_stopwwords(content, stopwords)

# 文档预料 空格连接
corpus = []

# 读取预料 一行预料为一个文档
for line in open('数据.txt', 'r',encoding='utf-8').readlines():
    corpus.append(line.strip())
# 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
vectorizer = CountVectorizer()

# 该类会统计每个词语的tf-idf权值
transformer = TfidfTransformer()

# 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
# 获取词袋模型中的所有词语
word = vectorizer.get_feature_names()

# 将tf-idf矩阵抽取出来 元素w[i][j]表示j词在i类文本中的tf-idf权重
weight = tfidf.toarray()

# 打印特征向量文本内容
print('Features length: ' + str(len(word)))




print('Start Kmeans:')
from sklearn.cluster import KMeans

clf = KMeans(n_clusters=4)
print(clf)
pre = clf.fit_predict(weight)
df = pd.read_excel('招聘数据.xlsx')
result = pd.concat((df, pd.DataFrame(pre)), axis=1)
result.rename({0: '聚类结果'}, axis=1, inplace=True)
result.to_excel('招聘数据-聚类.xlsx')
print(pre)
#
# 中心点
print(clf.cluster_centers_)
print(clf.inertia_)



from sklearn.decomposition import PCA

pca = PCA(n_components=4)  # 输出两维
newData = pca.fit_transform(weight)  # 载入N维
print(newData)

x = [n[0] for n in newData]
y = [n[1] for n in newData]
plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(20,9),dpi = 300)
plt.scatter(x, y, c=pre, s=100)
# plt.legend()
plt.title("./data/聚类图")
plt.savefig('./data/聚类图.jpg')
plt.show()