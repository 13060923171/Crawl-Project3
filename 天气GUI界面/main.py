import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
#GUI界面需要调用的库
import tkinter as tk
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#用于处理图片的
from PIL import Image,ImageTk
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
mpl.rcParams['axes.unicode_minus'] = False  # 负号显示
sum_hight = []
sum_low = []
sum_day = []
sum_zhishu = []


def weather_data():
    global sum_hight, sum_low, sum_day,sum_zhishu
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Cookie": "Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1626600382; f_city=%E5%8C%97%E4%BA%AC%7C101010100%7C; Hm_lpvt_080dabacb001ad3dc8b9b9049b36d43b=1626602207",
    }
    city = b1.get()
    number = ''
    if city == '广州':
        number = 101280101
    elif city == '北京':
        number = 101010100
    elif city == '上海':
        number = 101020100
    elif city == '成都':
        number = 101270101
    elif city == '杭州':
        number = 101210101
    elif city == '南京':
        number = 101190101
    elif city == '天津':
        number = 101030100
    elif city == '深圳':
        number = 101280601
    elif city == '重庆':
        number = 101040100
    elif city == '西安':
        number = 101110101
    elif city == '青岛':
        number = 101120201
    elif city == '武汉':
        number = 101200101
    list_url = ['http://www.weather.com.cn/weather/{}.shtml'.format(number),
                'http://www.weather.com.cn/weather15d/{}.shtml'.format(number),
                ]

    for url in list_url:
        html = requests.get(url,headers=headers)
        html.encoding = html.apparent_encoding
        if html.status_code == 200:
            content = html.text
            soup = BeautifulSoup(content,'lxml')
            zhishu = soup.select('div.livezs ul.clearfix li')
            for z in zhishu:
                em = z.select_one('em').text
                span = z.select_one('span').text
                p = z.select_one('p').text
                sum_zhishu.append([em,span,p])
            tem = soup.select("li p.tem")
            for t in tem:
                wendu = t.text.strip('\n').split('/')
                sum_hight.append(wendu[0])
                sum_low.append(wendu[-1])
            tem_15 = soup.select("li span.tem")
            for t in tem_15:
                hight = t.select_one("em").text
                sum_hight.append(hight)
                low = t.text.split('/')[-1]
                sum_low.append(low)
            time = soup.select("ul.t.clearfix li")
            for t in time:
                try:
                    day = t.select_one("h1").text
                    sum_day.append(day[:3].replace("（", "").replace(" )", ""))
                    # weather = t.select_one('p.wea').text
                    # sum_weather.append(weather)
                    # fen = t.select_one('p.win i').text
                    # sum_fen.append(fen)
                except Exception as e:
                    day = t.select_one("span.time").text.replace("（", "").replace("）", "")
                    sum_day.append(day[2:])
                    # weather = t.select_one('span.wea').text
                    # sum_weather.append(weather)
                    # fen15 = t.select_one('span.wind1').text
                    # sum_fen.append(fen15)

    fig = plt.figure(figsize=(6,4), dpi=90)  # 图像比例
    f_plot = fig.add_subplot(111)  # 划分区域
    canvas_spice = FigureCanvasTkAgg(fig, win)
    canvas_spice.get_tk_widget().place(x=0, y=200)  # 放置位置
    if len(sum_hight) != len(sum_low) or len(sum_hight) != len(sum_day):
        sum_hight.insert(0, '')
    def data(x):
        x = x.replace('℃', '')
        return x

    df = pd.DataFrame()
    df['日期'] = sum_day
    df['最高温'] = sum_hight
    df['最低温'] = sum_low
    x1 = df['最高温'].apply(data)
    x2 = df['最低温'].apply(data)
    df['最高温'] = x1
    df['最低温'] = x2
    df['最高温'].fillna(df['最高温'].mean(), inplace=True)
    f_plot.clear()  # 刷新
    plt.plot(df['日期'], x2, color='blue', alpha=0.5, linestyle='--', linewidth=3, marker='*',label='最低温')
    plt.plot(df['日期'], x1, color='red', alpha=0.5, linestyle='--', linewidth=3, marker='v',label='最高温')
    plt.legend()
    plt.ylabel('温度:(单位/℃)')
    plt.xticks(rotation=-45)
    plt.title('未来15天内的天气的最高和最低温')
    canvas_spice.draw()

    spider()
    get_data()

#设置图片的大小，并且调用
def get_image(file_name,width,height):
    #打开图片，并且定义宽与高
    img = Image.open(file_name).resize((width,height))
    #返回处理好的图片
    return ImageTk.PhotoImage(img)

def spider():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
    }
    #city的数值从b1输入框调用
    city = b1.get()
    #处理用户输入的时间
    #规定三种格式都可以2018/10/1 2018年10月1日 2018-10-1
    #获取时间文本框的输入
    # date = b2.get()
    # if '/' in date:
    #     tm_list = date.split('/')
    # elif '-' in date:
    #     tm_list = date.split('-')
    # else:
    #     tm_list = re.findall(r'\d+',date)
    # #1-9月 前面加0
    # if int(tm_list[1]) <10:
    #     tm_list[1] = f'0{tm_list[1]}'
    #分析网页发现的规律 构造URL
    #直接访问有该有所有天气信息的页面 提高查询效率，注意一下，因为这里不是会员所以调用次数有限，一天只能调用100次，请各位手下留情
    url = f"http://apis.juhe.cn/simpleWeather/query?city={city}&key=2bd46fa7867fe9598989a6681d4b44a5"
    #返回一个json类型
    html = requests.get(url,headers=headers).json()
    #定位到当前最新日期
    result = html['result']['realtime']
    #输出信息格式化一下
    list = []
    info1 = ['温度：', '湿度：', '天气：', '风度：', '风向：','风力强度:','aqi:']
    for key, values in result.items():
        list.append(result[key])
    #将两个列表联合在一起输出
    datas = [i + j for i,j in zip(info1,list)]
    #最后将datas这个列表打印出来
    info = '\n'.join(datas)

    #先在文本框里面插入最新天气现象
    t.insert('insert','{}最新天气现象     \n'.format(city))
    #再插入获取到的数据
    t.insert('insert',info)
    #最后将这些全部打印出来

def get_data():
    global sum_zhishu
    city = b1.get()
    zhishu = sum_zhishu[0:6]
    str1 = ''
    for z in zhishu:
        info = '\n'.join(z)
        str1 += info + '\n'
    print(str1)
    # 先在文本框里面插入最新天气现象
    t1.insert('insert', '{}生活指数     \n'.format(city))
    # 再插入获取到的数据
    t1.insert('insert', str1)

if __name__ == '__main__':
    # 定义窗口的名称
    win = tk.Tk()
    # 设置窗口title
    win.title('天气查询系统')
    # 设置窗口的大小
    win.geometry('800x800')
    # 设置画布的大小，作用于win这个窗口
    canvas = tk.Canvas(win, height=800, width=800)
    # 导入图片
    im_root = get_image('test.jpg', width=800, height=800)
    # 创建画布的图片
    canvas.create_image(400,400, image=im_root)
    canvas.pack()
    # 单行文本
    L1 = tk.Label(win, bg='#6A0996', text='城市', font=('SimHei', 12))
    # 位置
    L1.place(x=50, y=100)
    # 单行文本框，可采集键盘输入
    b1 = tk.Entry(win, font=('SimHei', 12), show=None, width=35)
    b1.place(x=100, y=100)
    # 设置查询按钮，点击调用爬虫函数来实现查询
    a = tk.Button(win, bg='#A22B10', text="查询", width=25, height=2, command=weather_data)
    a.place(x=160, y=140)
    t = tk.Text(win, width=20, height=9, font=("SimHei", 18), selectforeground='red')  # 显示多行文本
    t.place(x=550, y=200)
    t1 = tk.Text(win, width=20, height=9, font=("SimHei", 18), selectforeground='red')  # 显示多行文本
    t1.place(x=550, y=450)
    # 进入消息循环
    win.mainloop()
