import pandas as pd
import requests
import time
import csv
import json

def gaode(addr):
        para = {
            'key':'2e5bd3a4e45b8a17ea0de5ad4ebac248',  #高德地图开放平台申请的key
            'address':addr #传入地址参数
        }
        url = 'https://restapi.amap.com/v3/geocode/geo?' #高德地图API接口
        req = requests.get(url,para)
        req = req.json()
        print('-' * 30)
        m = req['geocodes'][0]['location']
        print(m)
        return m
gaode(addr="深圳")