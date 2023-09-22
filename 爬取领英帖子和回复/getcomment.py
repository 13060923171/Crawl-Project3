import json
import os
import re
import time
import urllib.parse

import copyheaders
import pandas
import requests

headers = copyheaders.headers_raw_to_dict(b"""
Accept:application/vnd.linkedin.normalized+json+2.1
Cookie:li_sugr=5c7f5367-1013-440a-9f47-e247df68fbb3; bcookie="v=2&72b4ecd5-49c8-4ac6-8abe-73d2e2f759c4"; bscookie="v=1&20230609001640fa2b25ae-a31e-4446-8235-0cdf821bb786AQG74lTZ1kLp4QQgyXxMc0_JM7zCSgiN"; li_rm=AQGtv0xmTXSGswAAAYqHrAas9Cqt-8Hn0h_2xmtUTsr0sWJ29yLzBRir-Q2m_Ourc887jzPJvmThpQ28I2lxZG10YpE2t7Xff2gIS7lt0XimY2rrdpBr-CjO; aam_uuid=31184762345949947221600874795551838314; g_state={"i_l":0}; li_at=AQEDATaQrtsBjR5oAAABiom8dE0AAAGKrcj4TVYAr2jKoZszCgfkRZ-UNQo9RaZdpVbRlXT3VZRgtBLQr_ispnHBQWDIX0AMSMyS4ihpd-2SJpCaLRGwpXX6Z6a_4f9eltdUwIVTyDaXnABr8YmBqoBK; liap=true; JSESSIONID="ajax:2210591134930550786"; timezone=Asia/Shanghai; li_theme=light; li_theme_set=app; AnalyticsSyncHistory=AQJhuiQFRDx7zQAAAYqJvIuDq8dWSaENIE2-TpC-58PmlH78WPBzW4V1oOayytQouHhX87oHqp8cLFrfuKM7kQ; _guid=17699830-f0c3-47a7-93ab-4346281b9657; lms_ads=AQGS6EFRngtxjgAAAYqJvI3z4D-CbEGFQgLZgFhLt693tCzicDlDnKI2Y1CSQ7mUDYH2aFm4GWg2y1rGqtaAqOtTqY4FrmqT; lms_analytics=AQGS6EFRngtxjgAAAYqJvI3z4D-CbEGFQgLZgFhLt693tCzicDlDnKI2Y1CSQ7mUDYH2aFm4GWg2y1rGqtaAqOtTqY4FrmqT; li_cc=AQGdDi925dOP2gAAAYqJwqsmdNmIsnnNDNGXnAA5tYVywXcv3UywL0w9xBkYpMUcVxlcju8a-a6Q; li_ce=AQFze3547sKWfAAAAYqR0iXOckpq1tiJVF3fDsTzxb6e_qvI7XzlFwyP355BrXUrsMoURlA5ryRgLEA; lang=v=2&lang=zh-cn; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19615%7CMCMID%7C31367952125213229851655174128493962145%7CMCAAMLH-1695268425%7C3%7CMCAAMB-1695268425%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1694670825s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1613452186; UserMatchHistory=AQIPDvjRgnxDnQAAAYqSbAmN3FT8_OkdQGW2IFbsVshLXTWyBn-sV3bNcTibsJen38pDEAwQK6Vm_E1GAJKjfTVbWPbmb1Wi7anVh5-Jvk00HBNadwwWFIV94eP0vefCmxRv0sIWqQlUElwSvZDj7iqBkUaepwfXxF0WTsLDDs0uJcyp-d4lKNEnqbwR25QSleuU6LuLg3bsCau5KAXAGt_4GD1yfXvYis3TVBLPX0aWNWibyFudCmn1GhE4X_XCiH2YcTVhlsyGImPCUebUfyTGS2UrKo374qhyD1PmmCCfHTOb7DGqDgybfXKnNUinTySzpOS1LDwj31IG4APo6UiO6iwOvXI; lidc="b=VB11:s=V:r=V:a=V:p=V:g=4626:u=2:x=1:i=1694673673:t=1694749982:v=2:sig=AQEeCjSXNp9Ib6cPYC7US8n8xDccmZ8n"
Csrf-Token:ajax:2210591134930550786
Pragma:no-cache
Referer:https://www.linkedin.com/company/google/posts/
Sec-Ch-Ua:"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"
Sec-Ch-Ua-Mobile:?0
Sec-Ch-Ua-Platform:"Windows"
Sec-Fetch-Dest:empty
Sec-Fetch-Mode:cors
Sec-Fetch-Site:same-origin
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203
X-Li-Lang:zh_CN
X-Li-Page-Instance:urn:li:page:d_flagship3_company;82yyRjd5RaKU+BKbM+fhdA==
X-Li-Pem-Metadata:Voyager - Feed - Comments=load-comments
X-Li-Track:{"clientVersion":"1.13.3124","mpVersion":"1.13.3124","osName":"web","timezoneOffset":8,"timezone":"Asia/Shanghai","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1920,"displayHeight":1080}
X-Restli-Protocol-Version:2.0.0
""")

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"


def send_get(api,headers,params):
    while 1:
        try:
            res = requests.get(
                api,
                headers=headers,
                params=params,
                timeout=(4,5)
            )
            time.sleep(1.5)
            return res
        except Exception as e:
            print(f"some errror:{e}")
            time.sleep(.4)


def download_comments(ipost):
    shareUrn = ipost.get("shareUrn")
    numComments = ipost.get("numComments")
    print(f">>> 访问帖子：",shareUrn,numComments,ipost.get("numComments")//10 + 2)
    pageconfig = {"p":''}
    active_post = shareUrn.replace("urn:li:fs_socialDetail:",'')
    aid = urllib.parse.quote(f':li:fsd_socialDetail:({active_post},{active_post},urn:li:highlightedReply:-)')
    print(active_post,aid)
    for page in range(0,ipost.get("numComments")//10 + 2):
        start_offset = page * 10
        if page == 0:
            api = 'https://www.linkedin.com/voyager/api/graphql?variables=(count:10,numReplies:1,' \
                  'socialDetailUrn:urn' \
                  f'{aid}' \
                  ',sortOrder:RELEVANCE,start:'+str(start_offset)+')&&queryId=voyagerSocialDashComments.7f84231f883eba7ea2f0c6d0783e5b3b'
        else:

            api = 'https://www.linkedin.com/voyager/api/graphql?variables=(count:10,numReplies:1,paginationToken:915451611-1694674079466-97a6ab1a76ffbc2a75fd6c90f964def8,' \
                  'socialDetailUrn:urn' \
                  f'{aid}' \
                  ',sortOrder:RELEVANCE,start:'+str(start_offset)+')&&queryId=voyagerSocialDashComments.7f84231f883eba7ea2f0c6d0783e5b3b'
        response = send_get(api,headers,{})
        pageconfig["p"] = response.json().get("data").get("data").get("socialDashCommentsBySocialDetail").get("metadata").get("paginationToken")
        if pageconfig["p"] == None:
            break

        dict_map = {}
        includeds = response.json().get("included")
        for included in includeds:
            urn = included.get("urn")
            if urn is None:
                continue

            saveitem = {}
            saveitem["post_id"] =shareUrn
            saveitem["comment_id"] = urn
            saveitem["urn"] = urn
            saveitem["comment"] = included.get("commentary",{}).get("text")
            saveitem["commenter_id"] = included.get("commenter",{}).get("urn")
            saveitem["commenter_name"] = included.get("commenter",{}).get("title",{}).get("text")
            saveitem["commenter_createdAt"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(included.get("createdAt")//1000))
            dict_map[urn] = saveitem

        for included in includeds:
            reactionTypeCounts = included.get("reactionTypeCounts")
            if reactionTypeCounts is None:
                continue

            entityUrn = included.get("entityUrn","").replace("urn:li:fsd_socialActivityCounts:",'')

            dict_map[entityUrn]["numComments"] = included.get("numComments")
            try:
                dict_map[entityUrn]["reactionTypeCounts"] = included.get("reactionTypeCounts", [{}])[0].get("count")
            except:
                dict_map[entityUrn]["reactionTypeCounts"] = ''
            print(active_post,page,dict_map[entityUrn])
            with open("comment.txt",'a',encoding='utf-8') as f:
                f.write(json.dumps(dict_map[entityUrn]))
                f.write('\n')







if  __name__ == "__main__":

    with open("./company.txt",'r',encoding='utf-8') as f:
        posts = [json.loads(i.strip()) for i in f.readlines()][100:][::-1]
    for ipost in posts:
        download_comments(ipost)

    with open("comment.txt",'r',encoding='utf-8') as f:
        lines = [json.loads(i.strip()) for i in f.readlines()]
    df = pandas.DataFrame(lines)
    df.to_excel("comment.xlsx",index=False)