import datetime
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

def page_url(number1,number2,name):
    # 打开 boss 首页
    index_url = f'https://www.zhipin.com/web/geek/job?query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&city={number1}&salary=405&page={number2}'
    browser.get(index_url)
    # 等待页面加载
    time.sleep(3)  # 根据网络情况调整
    # 模拟滑动页面
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    job_detail = browser.find_elements(by=By.XPATH,
                                           value='//div[@class="search-job-result"]/ul/li')
    for job in job_detail:
        # 工作地址
        job_href = job.find_element(by=By.XPATH, value="./div[1]/a")
        # 获取 href 属性
        href_value = job_href.get_attribute("href")

        df = pd.DataFrame()
        df['城市'] = [name]
        df['链接'] = [href_value]
        df.to_csv('一级链接.csv', encoding='utf-8-sig', mode='a+', index=False, header=False)

    time.sleep(1.5)  # 根据网络情况调整


if __name__ == '__main__':
    df = pd.DataFrame()
    df['城市'] = ['城市']
    df['链接'] = ['链接']
    df.to_csv('一级链接.csv',encoding='utf-8-sig',mode='w',index=False,header=False)
    browser = webdriver.Edge()
    list_city = [101280100,101280800]
    list_city_name= ['广州','佛山']
    for c1,c2 in tqdm(zip(list_city,list_city_name)):
        for i in tqdm(range(1,20)):
            page_url(c1,i,c2)
    # 确保退出浏览器
    browser.quit()