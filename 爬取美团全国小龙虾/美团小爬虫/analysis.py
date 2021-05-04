'''
Function:
	简单的数据分析

python交流群:
	976191019
'''
import os
import jieba
import pickle
from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Line
from pyecharts import Radar
from pyecharts import Funnel
from wordcloud import WordCloud


'''饼图'''
def drawPie(title, data, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	pie = Pie(title, title_pos='center')
	pie.use_theme('westeros')
	attrs = [i for i, j in data.items()]
	values = [j for i, j in data.items()]
	pie.add('', attrs, values, is_label_show=True, legend_orient="vertical", legend_pos="left", radius=[30, 75], rosetype="area")
	pie.render(os.path.join(savepath, '%s.html' % title))


'''柱状图(2维)'''
def drawBar(title, data, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	bar = Bar(title, title_pos='center')
	bar.use_theme('vintage')
	attrs = [i for i, j in data.items()]
	values = [j for i, j in data.items()]
	bar.add('', attrs, values, xaxis_rotate=15, yaxis_rotate=10)
	bar.render(os.path.join(savepath, '%s.html' % title))


'''漏斗图'''
def drawFunnel(title, data, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	funnel = Funnel(title, title_pos='center')
	funnel.use_theme('chalk')
	attrs = [i for i, j in data.items()]
	values = [j for i, j in data.items()]
	funnel.add("", attrs, values, is_label_show=True, label_pos="inside", label_text_color="#fff", legend_pos="left", legend_orient="vertical")
	funnel.render(os.path.join(savepath, '%s.html' % title))


'''雷达图'''
def drawRadar(title, data, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	radar = Radar(title, title_pos='center')
	radar.use_theme('essos')
	values = [j for i, j in data.items()]
	sum_ = sum(values) / (len(values) // 2)
	schema = [(i, sum_) for i, j in data.items()]
	values = [values]
	radar.config(schema)
	radar.add("", values, is_splitline=True, is_axisline_show=True, radar_text_size=20)
	radar.render(os.path.join(savepath, '%s.html' % title))


'''统计词频'''
def statistics(texts, stopwords):
	words_dict = {}
	for text in texts:
		temp = jieba.cut(text)
		for t in temp:
			if t in stopwords or t == 'unknow':
				continue
			if t in words_dict.keys():
				words_dict[t] += 1
			else:
				words_dict[t] = 1
	return words_dict


'''折线图'''
def drawLine(title, data, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	line = Line(title, title_pos='center')
	line.use_theme('purple-passion')
	attrs = [i for i, j in data.items()]
	values = [j for i, j in data.items()]
	line.add('', attrs, values, xaxis_rotate=30, yaxis_rotate=30, mark_point=['max', 'min'])
	line.render(os.path.join(savepath, '%s.html' % title))


'''词云'''
def drawWordCloud(words, title, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	wc = WordCloud(font_path='data/simkai.ttf', background_color='white', max_words=2000, width=1920, height=1080, margin=5)
	wc.generate_from_frequencies(words)
	wc.to_file(os.path.join(savepath, title+'.png'))


'''run'''
if __name__ == '__main__':
	with open('杭州_data.json', 'rb') as f:
		all_data = pickle.load(f)
	# 词云
	stopwords = open('./data/stopwords.txt', 'r', encoding='utf-8').read().split('\n')[:-1]
	texts = [i.replace('(', '').replace(')', '').replace('（', '').replace('）', '') for i, j in all_data.items()]
	words_dict = statistics(texts, stopwords)
	drawWordCloud(words_dict, '杭州美食商家名词云', savepath='./results')
	texts = [j[0].replace('(', '').replace(')', '').replace('（', '').replace('）', '') for i, j in all_data.items()]
	words_dict = statistics(texts, stopwords)
	drawWordCloud(words_dict, '杭州美食商家地址词云', savepath='./results')
	# 性价比Top10
	data = {}
	for key, value in all_data.items():
		if value[1] != 0 and value[2] != 0 and value[3] != 0:
			data[key] = value
	top_10 = sorted(data.items(), key=lambda item: item[1][1]*item[1][2]/item[1][3])[-10:]
	data = {}
	for i, j in top_10:
		data[i] = j[1] * j[2] / j[3]
	drawBar('杭州性价比最高的十家店(可能不靠谱)', data, savepath='./results')