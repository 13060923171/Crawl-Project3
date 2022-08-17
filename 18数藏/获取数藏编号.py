import requests
import json
import pandas as pd

session = requests.session()

def get_page(url=None):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "content-type": "application/json;charset=UTF-8",
        "accept": "application/json",
        "cookie": "_dx_captcha_cid=37997214; _dx_uzZo5y=15351f08daa7557de642ce5963a6da91dfbc6b21de65cae42795bd9ecab5462bc9bdf296; _dx_app_a851c32ee3494848e5a939d4c5c95994=62ea8908pmHEJlSVnA8QqlgKX3LZ1DNv9PYx25r1; _dx_captcha_vid=85DF038E8F6326892BB8A6DAEEA697FFFC4337DDC0F0E71CF7EAC82A697A6A634A0B40A07F66DBE9E12ADC89A8D4AF3F9913B7DF63436F9F798FC9F1FB0B818B63C77D2E73C7259465649025C9EFEA53",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOjEzNTg3NSwiVXNlckluZm8iOiJDRVcvSys4cExoeFZ5cTJ6MmVVQmh5aGpNYzZUZDFUK1VBS3lmbi94Znp0TzV1ZXpHTXpLejY0KzIrc214UWhyY2R1eFVDMW5HM1hYelpvQ0J2T1kvS0FtVVhwN2ZKUDNqQ2hNa1duVTBIeHJ1UnRuRFYyMmhNTURLb0VOWkgycDEvbHc2aFZGVklUQitRMmROd01aelE9PSIsIm5iZiI6MTY1OTc5NTk4OSwiZXhwIjoxNjYwMjI3OTg5LCJpYXQiOjE2NTk3OTU5ODksImlzcyI6InNoaWJhX2FkbWluIiwiYXVkIjoic2hpYmFfYWRtaW4ifQ.XxJ7KvbuMKtAodOiKDPf4LsqrJH_pOuRTKt0CnN0lWE",
    }
    data = {
        "categoryId": 0,
        #物品编码号
        "pageIndex":1,
        "pageSize":10
    }
    html = session.post(url=url,headers=headers,data=json.dumps(data))
    if html.status_code == 200:
        content = html.json()
        print(content['data']['totalPages'])
        return content['data']['totalPages']
    else:
        print(html.status_code)


def get_id(url=None,page=None):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "content-type": "application/json;charset=UTF-8",
        "accept": "application/json",
        "origin": "https://m.18art.art",
        "referer": "https://m.18art.art/market",
        "cookie": "_dx_captcha_cid=21478213; _dx_uzZo5y=35955fd1c22cfde0f700ae8558c570cbb530cd6470e9c0eb532b64e15511fe85bb2f329d; _dx_app_a851c32ee3494848e5a939d4c5c95994=62eb793beBIgYocEtQeDHnZwomt88a6GPWQdscM1; _dx_captcha_vid=41CD5AECBCEA6D7A623F717FE9E9D36BA5216F0BB5D003C92175733B0564CB5AE8142739A920D285D9F50613CF34A7D54E288CD2BE0C07F14AE284D35DEED8DA6CE7C3274C83E7AAFB4824447A872A62",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOjEzNTg3NSwiVXNlckluZm8iOiJDRVcvSys4cExoeFZ5cTJ6MmVVQmh5aGpNYzZUZDFUK1VBS3lmbi94Znp0TzV1ZXpHTXpLejY0KzIrc214UWhyY2R1eFVDMW5HM1hYelpvQ0J2T1kvS0FtVVhwN2ZKUDNqQ2hNa1duVTBIeHJ1UnRuRFYyMmhNTURLb0VOWkgycDEvbHc2aFZGVklUQitRMmROd01aelE9PSIsIm5iZiI6MTY1OTc5NTk4OSwiZXhwIjoxNjYwMjI3OTg5LCJpYXQiOjE2NTk3OTU5ODksImlzcyI6InNoaWJhX2FkbWluIiwiYXVkIjoic2hpYmFfYWRtaW4ifQ.XxJ7KvbuMKtAodOiKDPf4LsqrJH_pOuRTKt0CnN0lWE",
    }
    data = {
        "categoryId": 0,
        #页数
        "pageIndex":page,
        "pageSize":10
    }
    html = session.post(url=url,headers=headers,data=json.dumps(data))
    if html.status_code == 200:
        content = html.json()
        for i in content['data']['items']:
            id = i['id']
            name = i['name']
            df = pd.DataFrame()
            df['name'] = [name]
            df['id'] = [id]
            df.to_csv('商品编号.csv', encoding='utf-8-sig', mode='a+', index=False, header=False)
    else:
        print(html.status_code)






if __name__ == '__main__':
    df = pd.DataFrame()
    df['name'] = ['name']
    df['id'] = ['id']
    df.to_csv('商品编号.csv',encoding='utf-8-sig',mode='w',index=False,header=False)
    url = 'https://m.18art.art/api/agg/market/pages'
    page = get_page(url)
    for p in range(1,int(page+1)):
        get_id(url,p)


