import requests
from lxml import etree
import numpy as np
import pandas as pd
from tqdm import tqdm
import re
import time
import random


user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

headers = {
    "user-agent": random.choice(user_agent),
    "cookie": "ttwid=1%7C7ft2I6VOwdq6hOZh7IyZnUsQXF3ABVx7uU11GSnzqRY%7C1670994384%7Cd1b8892b0c52b9cad86b25daac7eb96a5007694d8399fd1867940d836262b32b; ttcid=982711f18dc24f96b01746aa4bbb8b7188; xgplayer_user_id=69596003583; passport_csrf_token=a8d67bb48e9cd0b6fc128ec19bde4b00; passport_csrf_token_default=a8d67bb48e9cd0b6fc128ec19bde4b00; s_v_web_id=verify_lepe898k_dRIcxON0_iVrH_4fkC_9lKK_xHwsgZ7dZm9U; csrf_session_id=0b5e2e1e0cfc200c134f8fa4dd285652; d_ticket=457a29bd35c9f85eef099d40a1cf4de4da5e8; passport_assist_user=CkHt24TeCqn_7tdqNaYPmUH8ezJUoVAX9LhE2Mar8hCU0E_SXhJwgbmsjJd7DRPNc0xWENrhJJG681SA27kiaffjIBpICjynfDWtFJ0RceVeS0zktvRUf4NaBrs7dSgVaqyx9qMOGhZRz0FGFlZ97j6aXtWxH0pORtDCtY14kBkC7gYQhMuqDRiJr9ZUIgEDpyY8fQ%3D%3D; n_mh=tAEuoAg1La9sYtHwxmG5tufR23dc2gronxORACD3EAs; sso_auth_status=e43086892b2e8fed11990b14c9f3940e; sso_auth_status_ss=e43086892b2e8fed11990b14c9f3940e; sso_uid_tt=0cf8e8dc39fd88b191f5cfb3e333aa51; sso_uid_tt_ss=0cf8e8dc39fd88b191f5cfb3e333aa51; toutiao_sso_user=8e756e48173ac3eae5a38dd132058119; toutiao_sso_user_ss=8e756e48173ac3eae5a38dd132058119; sid_ucp_sso_v1=1.0.0-KGQ3ZGViODZkNTNjMDdkYTM2ODc3ZjdmYTVlZmQwODdmNmEwYzI3NGIKHwjduaD60IyjAhCkkfyfBhjvMSAMMM_ow5oGOAJA8QcaAmxmIiA4ZTc1NmU0ODE3M2FjM2VhZTVhMzhkZDEzMjA1ODExOQ; ssid_ucp_sso_v1=1.0.0-KGQ3ZGViODZkNTNjMDdkYTM2ODc3ZjdmYTVlZmQwODdmNmEwYzI3NGIKHwjduaD60IyjAhCkkfyfBhjvMSAMMM_ow5oGOAJA8QcaAmxmIiA4ZTc1NmU0ODE3M2FjM2VhZTVhMzhkZDEzMjA1ODExOQ; odin_tt=3e7df116996ee3cb8c2496e5118b25274c198ae6f75c0e620c4ecc680f50a2f657eb0da58c2c597066cf60c1d8a9d920a0901d51832ed6e15bba1278d073790d; passport_auth_status=fc33e08836b8fb71d765963cfb789b8e%2Cd002a20af7c2a4c861ddc2da246bf349; passport_auth_status_ss=fc33e08836b8fb71d765963cfb789b8e%2Cd002a20af7c2a4c861ddc2da246bf349; uid_tt=fc15144a7af909ca5327bf36d94f9f70; uid_tt_ss=fc15144a7af909ca5327bf36d94f9f70; sid_tt=9bb67bd2a8cfe617269a9758c5b964dd; sessionid=9bb67bd2a8cfe617269a9758c5b964dd; sessionid_ss=9bb67bd2a8cfe617269a9758c5b964dd; LOGIN_STATUS=1; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jZXJ0IjoiLS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tXG5NSUlDRkRDQ0FicWdBd0lCQWdJVWVRbGl0OWNVMU1KK0l1NldGMGc5VUYrZVFpZ3dDZ1lJS29aSXpqMEVBd0l3XG5NVEVMTUFrR0ExVUVCaE1DUTA0eElqQWdCZ05WQkFNTUdYUnBZMnRsZEY5bmRXRnlaRjlqWVY5bFkyUnpZVjh5XG5OVFl3SGhjTk1qTXdNekF4TURneE1URTJXaGNOTXpNd016QXhNVFl4TVRFMldqQW5NUXN3Q1FZRFZRUUdFd0pEXG5UakVZTUJZR0ExVUVBd3dQWW1SZmRHbGphMlYwWDJkMVlYSmtNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEXG5BUWNEUWdBRXgrbndCbWtvYXpLMmMwdzFxVHAvNjVJRDJGSzZTVmdIRHpCdEJHaytYaGFlaUNNanFKNVVmZWU3XG50ZHFXcUtLWC9FQUFZQTU0WUd1aDJNSi9FSHg1VGFPQnVUQ0J0akFPQmdOVkhROEJBZjhFQkFNQ0JhQXdNUVlEXG5WUjBsQkNvd0tBWUlLd1lCQlFVSEF3RUdDQ3NHQVFVRkJ3TUNCZ2dyQmdFRkJRY0RBd1lJS3dZQkJRVUhBd1F3XG5LUVlEVlIwT0JDSUVJQWhDU20wNDR6ZnQwMXZ0QnZtUTgvYVNMNFY4b3hjZWM5L3B2REx3Kzd6N01Dc0dBMVVkXG5Jd1FrTUNLQUlES2xaK3FPWkVnU2pjeE9UVUI3Y3hTYlIyMVRlcVRSZ05kNWxKZDdJa2VETUJrR0ExVWRFUVFTXG5NQkNDRG5kM2R5NWtiM1Y1YVc0dVkyOXRNQW9HQ0NxR1NNNDlCQU1DQTBnQU1FVUNJUUNnaWNXNklMK2pQSjExXG5Rb3FkejBMWVZkZkR6N0dXNHRjcGZGcVhHYjhESHdJZ0RjbDJSeEhWN2V4R1FxOXA4L3FOUjdZbEYrRzRGa1VrXG52dVN4OVE2VDVXST1cbi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS1cbiJ9; bd_ticket_guard_server_data=; store-region=cn-gd; store-region-src=uid; sid_guard=9bb67bd2a8cfe617269a9758c5b964dd%7C1677658281%7C5183995%7CSun%2C+30-Apr-2023+08%3A11%3A16+GMT; sid_ucp_v1=1.0.0-KDY4NmUzZjQ0MTQ3MzkxZjIyNDczN2MzMGIxMGRiOWJlMjkwNDRjNzkKGwjduaD60IyjAhCpkfyfBhjvMSAMOAJA8QdIBBoCaGwiIDliYjY3YmQyYThjZmU2MTcyNjlhOTc1OGM1Yjk2NGRk; ssid_ucp_v1=1.0.0-KDY4NmUzZjQ0MTQ3MzkxZjIyNDczN2MzMGIxMGRiOWJlMjkwNDRjNzkKGwjduaD60IyjAhCpkfyfBhjvMSAMOAJA8QdIBBoCaGwiIDliYjY3YmQyYThjZmU2MTcyNjlhOTc1OGM1Yjk2NGRk; download_guide=%223%2F20230301%22; strategyABtestKey=%221677738014.903%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAD04IqC2-QsIMFSo0aSsrl12XaLdND6Px5uJnvqf9ppSodcOlkF8Uuz-nbOORSFXC%2F1677772800000%2F0%2F0%2F1677741780372%22; tt_scid=CndmRie4Y4EAMu4s2pEl561aD.FWyOyxCe05Yu5RvFOru08VnA1jEq5Vx3-mxeYY1c2c; __ac_nonce=0640050ca00babfe3dbbf; __ac_signature=_02B4Z6wo00f01j9V9eQAAIDCv1cPpe0BEfY.dfFAAOvjXVRh3WFf5kczrxHG93vCub0ejEySLArWFdsCSxLNnHhBVcDFbz9oKN-R4tAXWUqH6jzRGD-X.1p5XXoZ47AaIj8QAAlyD6919RWZc1; douyin.com; msToken=m60RWjygmc_8_VdIhYBBcC7Ro8WttoKDwZQ8_YlZvkVjmpYfoZyUr0w3R5mE6s21SnIDYt3QSM1MuGTewO6cd-9lWTiVtnboGNi69IVFHteHKYAmzuoD; home_can_add_dy_2_desktop=%220%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1678347093206%2C%22type%22%3A1%7D; passport_fe_beating_status=true; msToken=LVWA__4mVmvN_c2v_T-I9mnXB_kmp7bpAWzUkN2WdKtid17RjLUcjVXNJ0vbpVVccZlugtIcdT24E4ftdV8lYGpGADy6elG6NuBRxfDcmH31lx-ruReO",
}

a = random.random()

def check_status(url):
    url = 'https://www.douyin.com' +url
    html = requests.get(url,headers=headers)
    if html.status_code == 200:
        get_html(html,url)
        time.sleep(a)
    else:
        print(html.status_code)


def get_html(html,url):
    soup = etree.HTML(html.text)
    try:
        data = soup.xpath('//div[@class="kr4MM4DQ"]/span/text()')
        like = data[0]
        pinglun = data[1]
        shoucan = data[2]
    except:
        like = np.NAN
        pinglun = np.NAN
        shoucan = np.NAN

    try:
        title = re.compile('name="description" content="(.*?)"')
        title1 = title.findall(html.text)
        title1 = str(title1).split('-')[0].replace("['","")
        if '来抖音，记录美好生活！' in title1:
            title1 = np.NAN
    except:
        title1 =np.NAN

    try:
        timedate = soup.xpath('//div[@class="JvhAw4hP"]/span/text()')
        timedate = timedate[-1]
    except:
        timedate = np.NAN

    # try:
    #     biaoqian = soup.xpath('//h1[@class="z8_VexPf"]/span[@class="Nu66P_ba"]/span[2]/a/span/text()')
    #     biaoqian = ','.join(biaoqian)
    # except:
    #     biaoqian = np.NAN

    df = pd.DataFrame()
    df['链接'] = [url]
    df['标题+标签'] = [title1]
    df['发布时间'] = [timedate]
    # df['标签'] = [biaoqian]
    df['点赞'] = [like]
    df['评论数'] = [pinglun]
    df['收藏'] = [shoucan]
    df.to_csv('数据.csv', encoding='utf-8-sig', mode='a+', index=None, header=None)

# def note_html(html,url):
#     content = html.text
#     pinglun = re.compile('<div class="yCJWkVDx">(.*?)</div>')
#     pinglun1 = pinglun.findall(content)
#     try:
#         pinglun1 = pinglun1[0]
#     except:
#         pinglun1 =np.NAN
#
#     like = re.compile('<span class="htnqqoaP">(\d+)</span>')
#     like1 = like.findall(content)
#     try:
#         like1 = like1[0]
#     except:
#         like1 = np.NAN


if __name__ == '__main__':
    df = pd.DataFrame()
    df['链接'] = ['链接']
    df['标题'] = ['标题']
    df['发布时间'] = ['发布时间']
    # df['标签'] = ['标签']
    df['点赞'] = ['点赞']
    df['评论数'] = ['评论数']
    df['收藏'] = ['收藏']
    df.to_csv('数据.csv',encoding='utf-8-sig',mode='w',index=None,header=None)
    data = pd.read_csv('data.csv')
    for u in tqdm(data['视频链接']):
        check_status(u)
    # data = pd.read_excel('0809数据.xlsx')
    # data = data[data['站点名称'] == '抖音app']
    # for u in tqdm(data['文章地址']):
    #     if '?schema_type=37' not in u:
    #         check_status(u)