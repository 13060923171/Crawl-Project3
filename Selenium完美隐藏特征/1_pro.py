#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: 1_pro.py 
@time: 2020-11-30 22:39 
@description：解决方案，隐藏Selenium的特征
"""

import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')

chrome_options.add_argument("--disable-blink-features=AutomationControlled")


driver = Chrome(options=chrome_options)
# driver = Chrome('./chromedriver', options=chrome_options)


# 提前运行js代码
with open('./stealth.min.js') as f:
    js = f.read()

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
})
driver.get('https://bot.sannysoft.com/')
time.sleep(5)
driver.save_screenshot('walkaround.png')

# 你可以保存源代码为 html 再双击打开，查看完整结果
source = driver.page_source
with open('result.html', 'w') as f:
    f.write(source)
