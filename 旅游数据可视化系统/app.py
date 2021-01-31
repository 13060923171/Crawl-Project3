
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bar')
def bar():
    return render_template('bar.html', title='游客餐饮信息获取渠道/旅游平台网站考虑,因素')


@app.route('/line')
def line():
    return render_template('line.html', title='春/夏/秋/冬/旅游成本指数省份')


@app.route('/pie')
def pie():
    return render_template('pie.html', title='国内旅游收入分布情况<城镇居民/农村居民>')



@app.route('/bar_3')
def bar_3():
    return render_template('bar_3.html', title='国内旅游人数情况/出境旅游')


@app.route('/bar_4')
def bar_4():
    return render_template('bar_4.html', title='旅行社团内旅游组团人数和接待人数')


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
