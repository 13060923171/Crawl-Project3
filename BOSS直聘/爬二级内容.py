import datetime
import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from tqdm import tqdm


def main1(name,url):
    # 打开 boss 首页
    index_url = f'{url}'
    browser.get(index_url)
    # 等待元素出现
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "job-title"))
    )
    try:
        #显示岗位的活跃信息
        job_active = browser.find_element(by=By.XPATH,value='//div[@class="job-boss-info"]/h2/span').text
    except:
        job_active = np.NAN
    try:
        #岗位标题
        job_title = browser.find_element(by=By.XPATH,value='//div[@class="info-primary"]/div[2]/h1').text
    except:
        job_title = np.NAN
    try:
        #岗位工资
        job_salary = browser.find_element(by=By.XPATH,value='//div[@class="info-primary"]/div[2]/span').text
    except:
        job_salary = np.NAN
    try:
        #公司规模
        job_scale = browser.find_element(by=By.XPATH,value='//div[@class="sider-company"]/p[2]').text
    except:
        job_scale = np.NAN
    try:
        #公司类型
        job_type = browser.find_elements(by=By.XPATH,value='//div[@class="sider-company"]/p[3]/a')[0].text
    except:
        job_type = np.NAN
    time.sleep(10)  # 根据网络情况调整

    data = pd.DataFrame()
    data['城市'] = [name]
    data['链接'] = [url]
    data['岗位'] = [job_title]
    data['工资'] = [job_salary]
    data['公司规模'] = [job_scale]
    data['公司类型'] = [job_type]
    data['hr活跃表现'] = [job_active]
    data.to_csv('招聘详情.csv', encoding='utf-8-sig', mode='a+', index=False, header=False)


if __name__ == '__main__':
    df = pd.read_csv('一级链接.csv')
    df = df.drop_duplicates(subset=['链接'])
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
    browser = webdriver.Edge(options=options)
    data = pd.DataFrame()
    data['城市'] = ['城市']
    data['链接'] = ['链接']
    data['岗位'] = ['岗位']
    data['工资'] = ['工资']
    data['公司规模'] = ['公司规模']
    data['公司类型'] = ['公司类型']
    data['hr活跃表现'] = ['hr活跃表现']
    data.to_csv('招聘详情.csv', encoding='utf-8-sig', mode='w', index=False, header=False)
    for d1,d2 in tqdm(zip(df['城市'],df['链接'])):
        main1(d1,d2)
    # 确保退出浏览器
    browser.quit()