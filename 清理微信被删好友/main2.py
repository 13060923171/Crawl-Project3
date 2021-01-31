import time

from appium import webdriver
from selenium.common.exceptions import NoSuchElementException

desired_capabilities = {
    'platformName': 'Android', # 操作系统
    'deviceName': '5ENDU19A11001953', # 设备 ID
    'platformVersion': '10.0.10', # 设备版本号，在手机设置中查看
    'appPackage': 'com.tencent.mm', # app 包名
    'appActivity': 'com.tencent.mm.ui.LauncherUI', # app 启动时主 Activity
    'noReset': True # 是否保留 session 信息 避免重新登录
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities)
print('微信启动')

def is_del():

    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/cn1').click()
    time.sleep(2)
    # 在搜索框输入搜索信息
    driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys('臭屁瑶')
    time.sleep(2)
    #点击好友
    driver.find_element_by_id('com.tencent.mm:id/tm').click()
    time.sleep(2)
    # 转账操作 + 号
    driver.find_element_by_id('com.tencent.mm:id/ala').click()
    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/iy1').send_keys('臭屁瑶')
    time.sleep(0.5)
    driver.find_element_by_id('com.tencent.mm:id/iy1').click()
    time.sleep(0.5)
    driver.find_element_by_id('com.tencent.mm:id/anv').click()
    # driver.find_element_by_id('com.tencent.mm:id/iy1').send_keys('臭屁瑶')
    # time.sleep(0.5)
    # driver.find_element_by_id('com.tencent.mm:id/anv').click()
    # time.sleep(0.5)
    # driver.find_element_by_id('com.tencent.mm:id/iy1').send_keys('臭屁瑶')
    # time.sleep(0.5)
    # driver.find_element_by_id('com.tencent.mm:id/anv').click()
    # time.sleep(0.5)
    # driver.find_element_by_id('com.tencent.mm:id/iy1').send_keys('臭屁瑶')
    # time.sleep(0.5)
    # driver.find_element_by_id('com.tencent.mm:id/anv').click()
    # time.sleep(0.5)
    # driver.find_element_by_id('com.tencent.mm:id/iy1').send_keys('臭屁瑶')
    # time.sleep(0.5)
    # driver.find_element_by_id('com.tencent.mm:id/anv').click()


if __name__ == '__main__':
    is_del()


