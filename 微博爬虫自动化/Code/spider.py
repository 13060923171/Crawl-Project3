import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from lxml import etree
import pandas as pd
import sys

class Spider:
    def __init__(self,name,keyword):
        ###
        self.driver = webdriver.Edge('C:\\Users\\96075\\Desktop\\edgedriver_win32\\msedgedriver.exe')
        ### 储存信息
        self.item_list = []
        self.name = name
        self.keyword = keyword
        self.url = f"https://s.weibo.com/weibo?q={keyword}"

    def login(self):
        """

        :return:
        """
        self.driver.get("https://s.weibo.com/weibo?q=%E7%96%AB%E6%83%85&Refer=realtime_weibo&page=1")
        input("请手动登录，登录后请回车")
        time.sleep(2)
        print("登录成功!")


    def getData(self):
        """

        :return:
        """
        self.driver.get(self.url)
        time.sleep(1)
        if self.url == f"https://s.weibo.com/weibo?q={self.keyword}":
            input("关键词搜索中，搜索完毕请回车")
            time.sleep(1.5)
            # input("获取网页信息，请点击实时后回车")
        page = self.driver.page_source
        next_url = str(self.driver.find_element(By.XPATH, ("//a[text()='下一页']")).get_attribute('href'))
        print(next_url)
        try:
            self.parse(page,next_url)
        except Exception as e:
            print(e)
            self.download()


    def parse(self,page,next_url):
        tree = etree.HTML(page)
        div_list = tree.xpath('//div[@class="card-wrap"]')
        for div in div_list:
            item = {}
            name = div.xpath('.//div[@class="content"]/div[@class="info"]//a[@class="name"]/text()')
            name = name[0] if len(name) != 0 else None
            time = div.xpath('.//div[@class="content"]/p[@class="from"]//a[1]/text()')
            time = str(time[0]).strip() if len(time) != 0 else None
            f = div.xpath('.//div[@class="content"]/p[@class="from"]//a[2]/text()')
            f = str(f[0]).strip() if len(f) != 0 else None
            content = div.xpath('.//div[@class="content"]/p[@class="txt"]//text()')
            content = str(content[0]).strip() if len(content) != 0 else None
            transmit = div.xpath('.//div[@class="card-act"]/ul/li[1]/a/text()')
            transmit = str(transmit[0]).strip() if len(transmit) != 0 else None
            comment = div.xpath('.//div[@class="card-act"]/ul/li[2]/a/text()')
            comment = str(comment[0]).strip() if len(comment) != 0 else None
            praise = div.xpath('.//div[@class="card-act"]/ul/li[3]/a/button/span[2]/text()')
            praise = str(praise[0]).strip() if len(praise) != 0 else None
            item['name'] = name
            item['time'] = time
            item['f'] = f
            item['content'] = content
            item['transmit'] = transmit
            item['comment'] = comment
            item['praise'] = praise
            item['spiderTime'] = datetime.datetime.now().strftime('%Y-%m-%d')
            print(item)
            self.item_list.append(item)
        if "51" in str(next_url):
            print("已经到达尾页，程序结束!")
            self.close()
            self.download()
            sys.exit()
        else:
            self.url = next_url
            try:
                self.getData()
            except Exception as e:
                print(e)
                self.download()




    def run(self):
        """

        :return:
        """
        self.login()
        self.getData()


    def close(self):

        self.driver.close()


    def download(self):
        df = pd.DataFrame(self.item_list)
        df.to_csv(f"../static/{self.name}.csv",mode="a+",encoding="utf-8-sig",index=False)




if __name__ == '__main__':
    name = "疫情关键词实时舆论"
    keyword = "疫情"
    spider4 = Spider(name=name,keyword=keyword)
    spider4.run()



