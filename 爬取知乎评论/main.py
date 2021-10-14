import requests
import hashlib
import execjs
import chardet
import re


def zse():
    url = '/api/v4/search_v3?t=general&q=%E5%9F%BA%E9%87%91&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0'
    f = "+".join(["101_3_2.0", url, '"AKBZK4t3wBKPTtjh3eimAwjXLGUs6yLL4yo=|1614933884"'])
    fmd5 = hashlib.new('md5', f.encode()).hexdigest()
    with open('m.js', 'r') as f:
        ctx1 = execjs.compile(f.read())
    encrypt_str = ctx1.call('b', fmd5)
    zse_96 = '2.0_' + encrypt_str
    return zse_96

print(zse())
# def parse_url(url):
#     zse_96 = zse(url)
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
#         'cookie': '_zap=586214e2-eb68-473c-aa37-0f561b032fb3; d_c0="AfAdGglIxxOPTqgIZnOWVWcMjOz8dJ-o2ik=|1632571062"; _9755xjdesxxd_=32; YD00517437729195%3AWM_TID=aHRoYQIkzWVBBQQQURcqwIznRcZYXsPS; captcha_session_v2="2|1:0|10:1633093348|18:captcha_session_v2|88:ekVUYUcxUzFjcFc5REp4ck5maUZKT0tDMVN5ckZPT1hoeW1YdTBqMXQ2YlByM3NoQzlubDR6Mk51ZzNvclFGZA==|4cc8a0ee3d09b63409732e85339d7fbc88203fbf4903377ee153b729807d3844"; __snaker__id=JtscdFq4wHKaSK58; gdxidpyhxdE=J6dwqLtR47BG%2F0CxGv1To7zHCMz%2F2tlNt0tZZgL5huQSrBwv7uDDbClb%2BTKbXIALPpzcAu3tlopyHGtqhlSAqGmfHEWjIwdIuK%2B6x3X%2Ft1Sgl4%2BkV0j2cqyZxxNsAnELUSdQN7RQzzuuwy%2FvT4fn355AAZP7mvpQODHWEVEJcKWGgVT4%3A1633094247130; YD00517437729195%3AWM_NI=vZ6%2FPge2T2NVR1XsYg1wpCSgZfnxkleZv5QwEuo%2F5KyYM0uaI%2BAPReRttvTwXvNUsA8qeF8QCMviiY6CD48SopTcsIsKmx3hxO0E2G0hf8DQkAIkNQ7U0m1ZM1X%2BNxtFQ3A%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb8cf74abae89bbc44fa78e8ea6d55e938e8eaff83382f185d7b366b6bd98a4c52af0fea7c3b92ab686fad0d36da7ee9cd3cd5e92ef9894dc6df3a9c0a4d26d9abaa299ea68a786bad6d47d87aba1d0b841bb8783d1f86b8bf58fb1d16f92acbc97d77d9caa82b6f24bfcafaba7bb5b8193ba8aec53f69d8cd5bb59adb09c84f243b195a399b264bc9100a6b14df4b8aad9c75ba99f878ccd5bf58b008eb4528fef98cccd74b89a9fd4c437e2a3; captcha_ticket_v2="2|1:0|10:1633093411|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfTi5Bd3hRZlJnVHo1T01lOVowMC1nU2NURHpuY1pLQ2dLdVRlMXBhMklpS21oTWJCRzVlb0N4TWRkWW04d2VmaGNGaWNRb3hwc3d3eXgwejE4Q250UjVDY0VjbEhOaWJyb0t6ODdHdzVXdFlObzdybVM1TTZCXy1JZkV2ZXZ3TThsTjViYTJISmxEaEZkV2FCTG0yQzRlZXJwemNNSDB2SmRNbHZjbm9Zd1ZRemwtNWpJTlV2ZVpOZzhCelJJcC1VOWNuVzZRMG1JNnd5bmtMUFE1NS05UFdjbHo0OHAwZ1RGOExyVnU5d1JKbXpmUHdSLWJSNzItQU9MVUJZYW1HenhWWm40QWprNVFqNHlQYVo3SHhGWjA1NkU2MFlJOE0udEs4T2VaeFd0bFI0NlZMUFJUYnYwOWFHcnBRbmZrVDBDN0FZam9yenBXQXFaaVoxbkxhRW1QT0haa0ZKNUsyTElYS0RIOGRwMkJCNS5DeG9HLjBPRGlyeUJyc2t2dklIWUV1UmZrV0VSZy5NWWM5UnNKYVFVbE1tS09xRFhLdmY5ZmR0Ql9XVjRaVzRZV2lIVmV2NS56RjVDTDZWTTlqQnItdFk2cUhaQXZja1dsQ2R0Qm5PVVdOZUVIbGN2ZlI2SHRPMlA1bHVRTEc3Wmo0Q0VUcTF0Q2dOcGNtMyJ9|490c73975c767f1e669c52174bd4340e71d3067f5a4f3d9194f10f71db3cd539"; z_c0="2|1:0|10:1633093427|4:z_c0|92:Mi4xR09sNERnQUFBQUFCOEIwYUNVakhFeVlBQUFCZ0FsVk5NMVZFWWdDQm94TWU5ZEg2dkVUVzl4R1NQVV94MENFSW1n|218f1f1a9ac938ce850162bca588335a3bd566d4ead29732ab19311d3f2936e2"; ff_supports_webp=1; _xsrf=6jfeHJiZW1JSmjcgr8tmhdFsOSUYyvhI; q_c1=e30a8c85a3e747b0bd1f77d54d67737d|1634050001000|1634050001000; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1633964929,1634049625,1634126660,1634130764; SESSIONID=IiPiN1jGy47KibNpsahFHnuAJ3w27q8YPZUTVICKdo6; JOID=UF8XAEtXyd7j4G5SSlZuyxBpvmdYG6WPiaxaPQws-Oypig4ZPwUWuoPnblZIvOWv4ILwOuH7K-S479Mumiw1KJM=; osd=UVAXBk9Wxt7l5G9dSlBqyh9puGNZFKWJja1VPQoo-eOpjAoYMAUQvoLoblBMveqv5obxNeH9L-W379UqmyM1Lpc=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1634130773; KLBRSID=d1f07ca9b929274b65d830a00cbd719a|1634130782|1634130764',
#         'x-zse-93': '101_3_2.0',
#         'x-zse-96':zse_96,
#         'referer': 'https://www.zhihu.com/',
#     }
#     html = requests.get(url,headers=headers)
#     html.encoding = chardet.detect(html.content)['encoding']
#     if html.status_code == 200:
#         get_html(html)
#     else:
#         print(html.status_code)
#
#
# def get_html(html):
#     coment = html.text
#     content = re.compile('"title":"(.*?)",')
#     contents = content.findall(coment)
#     voteup = re.compile('"voteup_count":(.*?),"')
#     voteups = voteup.findall(coment)
#     comment_count = re.compile('"comment_count":(.*?),"')
#     comment_counts = comment_count.findall(coment)
#     try:
#         for i in range(len(contents)):
#             c = contents[i]
#             v = voteups[i]
#             cc = comment_counts[i]
#             print(c,v,cc)
#     except:
#         pass




