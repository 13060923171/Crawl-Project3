# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from scrapy.exporters import CsvItemExporter
import os
import pandas


class BlblPipeline:

    def __init__(self) -> None:
        pass

    def open_spider(self,spider):
        pass

    # 向csv文件中写入数据
    def process_item(self,item,spider):
        with open('temp.txt','a',encoding='utf-8') as ff:
            ff.write(json.dumps(dict(item)))
            ff.write("\n")
        print(f'>>>dataitem ',item)
        return item

    def close_spider(self, spider):
        if os.path.exists("temp.txt"):
            with open("temp.txt",'r',encoding='utf-8') as ff:
                lines = [json.loads(i.strip()) for i in ff.readlines()]
            pda = pandas.DataFrame(lines)
            pda.to_excel("data.xlsx")
            # os.remove('temp.txt')

