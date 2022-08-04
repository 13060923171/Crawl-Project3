from selenium import webdriver
import time
from retrying import retry
from lxml import etree
# 计算机中chromedriver.exe的绝对位置
# "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome("chromedriver.exe")
# 请求网站
driver.get("https://www.bilibili.com/video/av555840581?vd_source=e9269baccd81f93d19c615cd57b2b36c")
# title = driver.find_element_by_xpath("//div/h1/span[@class='tit']").text
# 最大化窗口
driver.maximize_window()
time.sleep(3)
# 获取当前访问的url
url = driver.current_url
print('现在的网址是:', url)
# numbers = driver.find_element_by_xpath('//div[@class="bilibili-player-video-sendbar bilibili-player-normal-mode"]/div/div[1]').text
# print(numbers)
# print("标题为：", title)
# 显示网页源码
html = driver.page_source
# tree = etree.HTML(html)
# div_list = tree.xpath('//div[@class="bilibili-player-video-sendbar bilibili-player-normal-mode"]/div/div[1]/text()')
# print(div_list)
# numbers = driver.find_element_by_xpath('//div[@class="bilibili-player-video-sendbar bilibili-player-normal-mode"]/div/div[1]').text
# print(numbers)
# # 将源码保存以便观察
with open('html.html', 'w', encoding='utf-8') as f:
    f.write(html)
# # 获取cookie
# cookie = driver.get_cookies()
# cookie = {i['name']:i['value'] for i in cookie}
# print('获取到的cookie：\n', cookie)
time.sleep(5)


@retry()
def get_number():
    numbers = driver.find_element_by_xpath('//div[@class="bilibili-player-video-sendbar bilibili-player-normal-mode"]/div/div[1]').text
    return numbers



# 用selenium自带的定位功能获取信息
number = get_number()
data = time.strftime("%Y-%m-%d %H:%M:%S")
if number != "1":
    print("现在的时间是：{}，当前的观看人数是：{}".format(data, number))
driver.refresh()
time.sleep(3)