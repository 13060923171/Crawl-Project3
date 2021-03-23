import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


df = pd.read_excel('是否注册企业微信名单（第三批）.xlsx').loc[:,['名称','Unnamed: 4','Unnamed: 5','Unnamed: 6','Unnamed: 7']]

list_1 = []
list_2 = []
list_3 = []
list_4 = []
list_5 = []

state_1 = []
state_2 = []
state_3 = []
state_4 = []
state_5 = []


#定位Chromedriver这个工具的位置
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs",{"profile.mamaged_default_content_settings.images":2})
options.add_experimental_option('excludeSwitches',['enable-automation'])
browser = webdriver.Chrome(executable_path="C:\\Users\\96075\\Desktop\\全部资料\\Python\\爬虫\\chromedriver.exe",options=options)
#设置等待时间
wait = WebDriverWait(browser,10)

def inquire(i):
    url = 'https://work.weixin.qq.com/wework_admin/register_wx?from=myhome_baidu'
    browser.get(url)
    input = wait.until(EC.presence_of_element_located((
        By.XPATH, '//input[@id="corp_name"]'
    )))
    input.send_keys(i)  # 输入关键词
    button = wait.until(EC.element_to_be_clickable((
        By.XPATH, '//div[@class="register_column_item_title"]'
    )))
    button.click()  # 模拟鼠标点击
    time.sleep(0.2)
    total = wait.until(EC.presence_of_element_located((
        By.XPATH, '//div[@class= "register_column_item_tip"]'
    ))).text
    input.clear()

    return total


def main():
    for j in df['名称']:
        list_1.append(j)
        inquire(j)
        if '该企业名称已被认证企业占用' == inquire(j):
            state_1.append('存在')
        if '填写企业、政府或组织名称' == inquire(j):
            state_1.append('不存在')

    for j in df['Unnamed: 4']:
        list_2.append(j)
        inquire(j)
        if '该企业名称已被认证企业占用' == inquire(j):
            state_2.append('存在')
        if '填写企业、政府或组织名称' == inquire(j):
            state_2.append('不存在')

    for j in df['Unnamed: 5']:
        list_3.append(j)
        inquire(j)
        if '该企业名称已被认证企业占用' == inquire(j):
            state_3.append('存在')
        if '填写企业、政府或组织名称' == inquire(j):
            state_3.append('不存在')

    for j in df['Unnamed: 6']:
        list_4.append(j)
        inquire(j)
        if '该企业名称已被认证企业占用' == inquire(j):
            state_4.append('存在')
        if '填写企业、政府或组织名称' == inquire(j):
            state_4.append('不存在')

    for j in df['Unnamed: 7']:
        list_5.append(j)
        inquire(j)
        if '该企业名称已被认证企业占用' == inquire(j):
            state_5.append('存在')
        if '填写企业、政府或组织名称' == inquire(j):
            state_5.append('不存在')
    df1 = pd.DataFrame()
    df1['1'] = list_1
    df1['2'] = state_1
    df1['3'] = list_2
    df1['4'] = state_2
    df1['5'] = list_3
    df1['6'] = state_3
    df1['7'] = list_4
    df1['8'] = state_4
    df1['9'] = list_5
    df1['10'] = state_5
    try:
        df1.to_csv("名单2.csv", mode="a+", header=None, index=None, encoding="gbk")
        print("写入成功")
    except:
        print("当页数据写入失败")

if __name__ == '__main__':
    main()