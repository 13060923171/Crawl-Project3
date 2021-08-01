import requests
import pandas as pd
import time
def tengxun(addr):
    url = "https://apis.map.qq.com/jsapi?"   #腾讯地图API接口
    para = {
        "qt": "geoc",
        "addr":addr, #传入地址参数
        "output": "json",
        "key": "UT3BZ-GAMK3-VJP3W-3WEQY-EMB27-RJBBA", #即腾讯地图API的key
        "pf":"jsapi",
        "ref":"jsapi"
    }
    req = requests.get(url,para) #请求数据
    req = req.json() #转为json格式
    #print(req)
    m = req["detail"]
    g = f"{m['pointx']},{m['pointy']}" #解析到经纬度数据
    print(g)
    return g

tengxun('深圳')