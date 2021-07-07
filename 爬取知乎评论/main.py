import requests
import re
import chardet
from lxml import etree

headers = {

    'x-zse-93': '101_3_2.0',
    'x-zse-96': '2.0_aXN0kirqeLNxgqO0f82qgvr8k7Fpo_2qKRY8c7Xqr_SY',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'referer': 'https://www.zhihu.com/',
    'cookie': '_zap=5b3012c1-6a33-453a-8f30-b19c23123fbc; d_c0="AKBZK4t3wBKPTtjh3eimAwjXLGUs6yLL4yo=|1614933884"; _xsrf=7466a4be-ff14-4e8c-a706-a558af8c1d90; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1622451884,1622773987,1623030424,1623222909; SESSIONID=qSfOfj9A0Gyk5u6BAG97T8ee1lq7hnB5kYVciRFkjg4; JOID=VF8QAk2g9X3wr-SMJKfkpckilE010KQfuMmPt2GQswafnZG7ZN2Zvpeu54onrmzeqamzRNtWjwAGhQWVVjMgI3U=; osd=W10UBUKv93n3oOuOIKDrqssmk0I60qAYt8aNs2afvASbmp60ZtmesZis440ooW7arqa8Rt9RgA8EgQKaWTEkJHo=; __snaker__id=WiaVCMMjC9fHiHtj; gdxidpyhxdE=fRrCdKCGt7DbUNTO0Pl342huIgPT2E%5CerbD2qqp4EOvH%2FQ%2F1JfmE%2Bghq1bzKgYeA1Y0vwxrDPmdwEim1fTvcwONiTLLH9CurOSqeQrU%2FrO0%2BaVcoPJfmO8Kb2W53ciMUy5bQZUiZvh%5CRnz2B9h%2FBUGb%2BjwWxJIMX9oKrgwBLetEGNi3v%3A1623223811134; _9755xjdesxxd_=32; YD00517437729195%3AWM_NI=EDkOlCjqIVONtPCD1NRTxPapmCXHziZ1LTR38mK81FGZT5Sk9BhpKZdEmuRnBwARknRpjnCYVlEO5EuKoxvyHA%2FKsMy1XzFwbh0HC9Zu8b0WKs5THg8TNcCjmhbVMCrVcUE%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed9d96983b3aaacf04192ef8fb3d84f838a9aaab53cf5b2e59bc44e82998490d62af0fea7c3b92a879ca5b0ef49aaaf87b7ce46b8908da5b446928cb8b1e47caf9d98a9f9639aef84b5d139fcb385d9b44e85869cd6d261fb9ea891ca52a89ba396d16682a98fb3ea6692b0a68fc25396b48bb0b84fb795a199f5738c9fe1acf247bbef989bc57da2b800a9c2339aabf883b35d89adfbb5cb6dfc8c8284c262afb8aeb7d049b28aadb6c837e2a3; YD00517437729195%3AWM_TID=DmCRHC%2BEB85BVBVQRRNqg%2Byv2EUVSK9D; captcha_ticket_v2="2|1:0|10:1623222917|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfbHIydXM4X2ZBLUtxeC1wb0NzYTY1NGtqYlFULWpzUVV4UTdwTTJpbUxhWVZlTWlGbGRQWDBuVlA0VlgtenBVUEhfNGJsNy1xZDhhMHR5R20yblJmczJ2WjR5d2pKYTFzLUsyZlhPTHpiSFUtU3ZmZG9DSmphb01mN1VWYUFtN3VGODJkYWJSMjcxeUh0X3o2aFFCaVpqUWFUV1FPUW5KaWVlTG1qUDV1cVFJTVJKTk1aVVhvLUl4Vl9CTlFuWUVzQklNTXh5SE9fYV8uU0YyV3hhalVqU0ROOWpZcGlHODZnVHQxV21HclR6ZHZPUUU1T0RYcnpjd1NEUUlFdno1UkZaVnNCTVlydHpfQ1ZkMUxyZzVWLjZBUWVHVFNRc2FrWWFtS0xyX0F5c29jYWFqbjIxbDBIWVRoTmhfRTBObFhyUmpveDZhN2NrMm5vN1I0ZW90LWpTZmRrbGFGN3dDeGNvMWltaTVwZE5SS2Z2Lmg5TTJCLVRlWmlxVkl1OENHRUltcXk0T3ZyZE42cFFiUFE1WXJCOFk3RGFodkZpZ2pUcHBOTHlrbEhTZ25DLnp6U1VyeEIuX1p2Q0lvRHkybHdiTW5xT3FHQWVtc2JDSE1uUVQtQnp3YXhhcjBHTy5VdktJVUQ1ajlXczBLY1VQV1JHQWl0LS4ydWRwMyJ9|f72c58c3e81fd7742eab8ffc9c35138e9234327f77d3d58f0b6dc170cde6c228"; z_c0="2|1:0|10:1623222929|4:z_c0|92:Mi4xR09sNERnQUFBQUFBb0ZrcmkzZkFFaVlBQUFCZ0FsVk5rYml0WVFEUWVvMTR2cXdOOURfbEtQOEpjZGVEYjNORTNn|c576d0622807b2cc11f05add77efce9e7f1615f7d477e501095cd2cd979dcd59"; captcha_session_v2="2|1:0|10:1623222930|18:captcha_session_v2|88:bnk3SlE3b2lPWmN6b2MxRy9PZFpXS2F2Qno0ZE1QdzRGSGpZaEE2TXZuY2EwcW40ek5SMVdBQ0xtWEFrVllCbA==|044b8b404af8b25cdbd2e471dc3b17c49f2a3661f5b81e1965e95696392ffc58"; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1623225780; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1623225780|1623222907',
}

def get_parse():
    url = 'https://www.zhihu.com/api/v4/topics/19841068/feeds/essence?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F(target.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.paid_info%3Bdata%5B%3F(target.type%3Darticle)%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.annotation_detail%2Ccomment_count%3B&offset=5&limit=10'
    html = requests.get(url,headers=headers)
    html.encoding = chardet.detect(html.content)['encoding']
    coment = html.text
    print(coment)
    content = re.compile('"title":"(.*?)",')
    contents = content.findall(coment)
    voteup = re.compile('"voteup_count":(.*?),"')
    voteups = voteup.findall(coment)
    comment_count = re.compile('"comment_count":(.*?),"')
    comment_counts = comment_count.findall(coment)

    try:
        for i in range(len(contents)):
            c = contents[i]
            v = voteups[i]
            cc = comment_counts[i]
            print(c,v,cc)
    except:
        pass

if __name__ == '__main__':
    get_parse()