import requests
import json
import asyncio
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import time
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from smtplib import SMTP_SSL
from tqdm import tqdm
import concurrent.futures

session = requests.session()

def get_content(url=None,id=None,price1=None,page=None):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "content-type": "application/json;charset=UTF-8",
        "accept": "application/json",
        "cookie": "_dx_captcha_cid=37997214; _dx_uzZo5y=15351f08daa7557de642ce5963a6da91dfbc6b21de65cae42795bd9ecab5462bc9bdf296; _dx_app_a851c32ee3494848e5a939d4c5c95994=62ea8908pmHEJlSVnA8QqlgKX3LZ1DNv9PYx25r1; _dx_captcha_vid=85DF038E8F6326892BB8A6DAEEA697FFFC4337DDC0F0E71CF7EAC82A697A6A634A0B40A07F66DBE9E12ADC89A8D4AF3F9913B7DF63436F9F798FC9F1FB0B818B63C77D2E73C7259465649025C9EFEA53",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOjEzNTg3NSwiVXNlckluZm8iOiJDRVcvSys4cExoeFZ5cTJ6MmVVQmh5aGpNYzZUZDFUK1VBS3lmbi94Znp0TzV1ZXpHTXpLejY0KzIrc214UWhyY2R1eFVDMW5HM1hYelpvQ0J2T1kvS0FtVVhwN2ZKUDNqQ2hNa1duVTBIeHJ1UnRuRFYyMmhNTURLb0VOWkgycDEvbHc2aFZGVklUQitRMmROd01aelE9PSIsIm5iZiI6MTY1OTc5NTk4OSwiZXhwIjoxNjYwMjI3OTg5LCJpYXQiOjE2NTk3OTU5ODksImlzcyI6InNoaWJhX2FkbWluIiwiYXVkIjoic2hpYmFfYWRtaW4ifQ.XxJ7KvbuMKtAodOiKDPf4LsqrJH_pOuRTKt0CnN0lWE",
    }
    data = {
        "pageIndex": page,
        "pageSize": 10,
        #物品编码号
        "groupId": id,
        "order":
            [{"fieldName": "DbPrice",
              "order": "Asc"}]
    }
    html = session.post(url=url,headers=headers,data=json.dumps(data))
    if html.status_code == 200:
        content = html.json()
        for c in content['data']['items']:
            print(c)
            commodityId = c['id']
            #2 是支付锁定 3 是寄售
            saleStatus = c['saleStatus']
            price = c['price']
            if saleStatus == 3 and price < price1:
                buy_main(commodityId)
                return True
            else:
                return False
    else:
        print(html.status_code)


def buy_main(commodityId):
    url = 'https://m.18art.art/api/wagg/order/buy'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "content-type": "application/json;charset=UTF-8",
        "accept": "application/json",
        "origin": "https://m.18art.art",
        "referer": "https://m.18art.art/page/order/create-order",
        "cookie": "_dx_captcha_cid=37997214; _dx_uzZo5y=15351f08daa7557de642ce5963a6da91dfbc6b21de65cae42795bd9ecab5462bc9bdf296; _dx_app_a851c32ee3494848e5a939d4c5c95994=62ea8908pmHEJlSVnA8QqlgKX3LZ1DNv9PYx25r1; _dx_captcha_vid=85DF038E8F6326892BB8A6DAEEA697FFFC4337DDC0F0E71CF7EAC82A697A6A634A0B40A07F66DBE9E12ADC89A8D4AF3F9913B7DF63436F9F798FC9F1FB0B818B63C77D2E73C7259465649025C9EFEA53",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOjEzNTg3NSwiVXNlckluZm8iOiJDRVcvSys4cExoeFZ5cTJ6MmVVQmh5aGpNYzZUZDFUK1VBS3lmbi94Znp0TzV1ZXpHTXpLejY0KzIrc214UWhyY2R1eFVDMW5HM1hYelpvQ0J2T1kvS0FtVVhwN2ZKUDNqQ2hNa1duVTBIeHJ1UnRuRFYyMmhNTURLb0VOWkgycDEvbHc2aFZGVklUQitRMmROd01aelE9PSIsIm5iZiI6MTY1OTc5NTk4OSwiZXhwIjoxNjYwMjI3OTg5LCJpYXQiOjE2NTk3OTU5ODksImlzcyI6InNoaWJhX2FkbWluIiwiYXVkIjoic2hpYmFfYWRtaW4ifQ.XxJ7KvbuMKtAodOiKDPf4LsqrJH_pOuRTKt0CnN0lWE",
    }
    data = {
        "commodityId": commodityId,
        "addressId": 0,
        #1是银行卡 2是钱包
        "payType": 2,
    }
    html = session.post(url=url, headers=headers, data=json.dumps(data))
    if html.status_code == 200:
        content = html.json()
        statusCode = content['statusCode']
        success = content['success']
        if statusCode == 200 and success == True:
            print('请求成功,请尽快支付')
            send_mail()
    else:
        print(html.status_code)


def send_mail():
    host_server = 'smtp.qq.com'  # QQ邮箱的SMTP服务器
    sender_qq = '960751327'  # 发件人的QQ号码
    pwd = 'fdrrjmiqqnaubdcj'  # QQ邮箱的授权码
    sender_qq_mail = '960751327@qq.com'  # 发件人邮箱地址

    mail_title = '请求成功,请在2分钟之内尽快支付'  # 设置邮件标题

    msg = MIMEMultipart('related')
    msg["Subject"] = Header(mail_title, 'utf-8')  # 填写邮件标题
    msg["From"] = sender_qq_mail  # 发送者邮箱地址
    msg["To"] = sender_qq_mail  # 接收者邮件地址

    smtp = SMTP_SSL(host_server)  # SSL 登录
    smtp.set_debuglevel(0)  # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.ehlo(host_server)  # 连接服务器
    smtp.login(sender_qq, pwd)  # 邮箱登录
    try:
        smtp.sendmail(sender_qq_mail, sender_qq_mail, msg.as_string())  # 发送邮件函数
        smtp.quit()  # 发送邮件结束
        print("Successfully Send！")  # 输出成功标志
    except Exception as e:
        print("The sever is busy,please continue later.",e)


def dq_csv():
    df = pd.read_csv('商品编号.csv')
    d = {}
    for n,i in zip(df['name'],df['id']):
        d[n] = i
    return d



if __name__ == '__main__':
    url = 'https://m.18art.art/api/agg/market/commodity-items'
    dict1 = dq_csv()
    #老鼠 215 鸡220
    id = dict1['运粮鼠']
    #价格位
    price1 = 6000
    s2 = time.time()

    for i in range(1,5):
        status = get_content(url,id,price1,i)
        if status == True:
            break

