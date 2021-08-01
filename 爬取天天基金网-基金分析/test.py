# -*- coding:utf-8 -*-
import requests
import time
import json
import re
headers = {
    "Host": "fund.eastmoney.com",
    "Referer": "http://fund.eastmoney.com/data/fundranking.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Cookie": "qgqp_b_id=a786b82ae98eb5e86c8c0d8c9da4daa5; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; Eastmoney_Fund=003096_001986_260108_001632_001551; ct=0ZjS5eJp26ACYMaIsTALCDa5KaduH9ybCCCH-UNuHEu6G_wa8CGP4QsNgwsqCkzpltJxlpf1M3fbXAAKO0J-AmZIVGLid9De51t5reWoCMvv4X_J8NmMnZP3W-cvNBUw0eJClAf-1ieeMWehO5y6XAYGDbLfU2V1kvURuJC_7BY; ut=FobyicMgeV4n4cCT8MJKZPXTUWPMm--eDUq0iCDxuEGU2-5VMb42ex6cq0Uewx05NYqRD8D7tCkrQOeQgbQ3aqdktzXEDsAz0h9ASUw6mDnbALSep6OrzxwrcmB27lLSFGTzZpiZdbCX4Q8x4LHjAuLzoXB6Ifeu4RjrtKzj0YqneId3pvs6AwykmackL1DiA-s3rtay0j5NQ7wQjRooBPqjMSDazN1cuzl02-_qcMiIgg8Jirk8k-kmhMsMfZpWt9hnBVs9cpLqaUfShK0LqdB4xgsdfHAw; pi=9926316275701270%3bv9926316275701270%3b%e8%82%a1%e5%8f%8b7N598777e0%3b9HviUjs8OeFXSmOd%2fkKtI94bP1uEAvL7ism6F%2bLNt%2bkLJS7yekwwl8dPgfwk49IHVu9OwScj7t35LTuAMtggy3qSWS0YZ0euVn%2bST2r2XyPoLcF08pTQ2iRrkkH0MzbnXyJTvqO%2fQibDS2lEVPD%2f0IhdMZS1QpC8uV%2bdrl6fw6IdAxYe3%2fnxqNy7t40atrGsGVb%2bJu6%2f%3bzAJUbkSauN6jbdDH9OTbMXUtox25yddUB%2bid2yV3bwLMPLxfJj2rAouNPEaspGDxdC8SIjXroNcx%2b7cF0PGOeDCTQXfStrRI9858Zx2gBkMibArx6X%2b6VhNtEmSt1gmQKJPXj0ndGTbxmXQF59Qi2zK4WeQpfQ%3d%3d; uidal=9926316275701270%e8%82%a1%e5%8f%8b7N598777e0; sid=167948003; vtpst=|; EmFundFavorVersion=0; st_si=24598731245369; st_asi=delete; EmFundFavorVersion2=1627570229901; ASP.NET_SessionId=hfgredmuhjpx1dfviccck0ac; EMFUND0=null; EMFUND6=07-04%2022%3A00%3A32@%23%24%u5357%u65B9%u660C%u5143%u8F6C%u503AA@%23%24006030; EMFUND7=07-29%2022%3A25%3A40@%23%24%u7533%u4E07%u83F1%u4FE1%u6CAA%u6DF1300%u6307%u6570%u589E%u5F3AA@%23%24310318; EMFUND8=07-29%2022%3A39%3A49@%23%24%u534E%u590F%u6210%u957F%u6DF7%u5408@%23%24000001; EMFUND9=07-31 22:01:28@#$%u957F%u57CE%u884C%u4E1A%u8F6E%u52A8%u6DF7%u5408@%23%24002296; st_pvi=64450143788844; st_sp=2021-07-04%2014%3A19%3A15; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2F; st_sn=6; st_psi=20210731220408754-112200312936-6154233039",
}

list_code = []

def get_status(now,over_the_past_year,days):
    params = {
        "op": "ph",
        "dt": "kf",
        "ft": "all",
        "rs": None,
        "gs": 0,
        "sc": "1yzf",
        "st": "desc",
        "sd": over_the_past_year,
        "ed": now,
        "qdii": None,
        "tabSubtype": ",,,,,",
        "pi": days,
        "pn": 50,
        "dx": 1,
    }
    url = 'http://fund.eastmoney.com/data/rankhandler.aspx?'
    html = requests.get(url,headers=headers,params=params)
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)

def get_html(html):
    global list_code
    content = html.text
    content = content.replace('var rankData = ','')
    content = content.replace('};','}')
    content = content.replace('{datas:','')
    all = re.compile('"](.*?)}')
    alls = all.findall(content)
    content = content.replace(alls[0],'')
    content = content.replace('}','')
    content = eval(content)
    for c in content:
        c = c.split(',')
        list_code.append(c[0])

def write_code(list_code):
    with open('代码.txt','w',encoding='utf-8')as f:
        str = '\n'
        f.write(str.join(list_code))


if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    over_the_past_year = str(int(now[0:4]) - 1) + now[4:]
    for i in range(1,11):
        get_status(now,over_the_past_year,i)
    write_code(list_code)