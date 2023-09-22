import json
import os
import re
import time
import copyheaders
import pandas
import requests

headers = copyheaders.headers_raw_to_dict(b"""
Accept:application/vnd.linkedin.normalized+json+2.1
Cookie:li_sugr=5c7f5367-1013-440a-9f47-e247df68fbb3; bcookie="v=2&72b4ecd5-49c8-4ac6-8abe-73d2e2f759c4"; bscookie="v=1&20230609001640fa2b25ae-a31e-4446-8235-0cdf821bb786AQG74lTZ1kLp4QQgyXxMc0_JM7zCSgiN"; li_rm=AQGtv0xmTXSGswAAAYqHrAas9Cqt-8Hn0h_2xmtUTsr0sWJ29yLzBRir-Q2m_Ourc887jzPJvmThpQ28I2lxZG10YpE2t7Xff2gIS7lt0XimY2rrdpBr-CjO; aam_uuid=31184762345949947221600874795551838314; g_state={"i_l":0}; li_at=AQEDATaQrtsBjR5oAAABiom8dE0AAAGKrcj4TVYAr2jKoZszCgfkRZ-UNQo9RaZdpVbRlXT3VZRgtBLQr_ispnHBQWDIX0AMSMyS4ihpd-2SJpCaLRGwpXX6Z6a_4f9eltdUwIVTyDaXnABr8YmBqoBK; liap=true; JSESSIONID="ajax:2210591134930550786"; timezone=Asia/Shanghai; li_theme=light; li_theme_set=app; AnalyticsSyncHistory=AQJhuiQFRDx7zQAAAYqJvIuDq8dWSaENIE2-TpC-58PmlH78WPBzW4V1oOayytQouHhX87oHqp8cLFrfuKM7kQ; _guid=17699830-f0c3-47a7-93ab-4346281b9657; lms_ads=AQGS6EFRngtxjgAAAYqJvI3z4D-CbEGFQgLZgFhLt693tCzicDlDnKI2Y1CSQ7mUDYH2aFm4GWg2y1rGqtaAqOtTqY4FrmqT; lms_analytics=AQGS6EFRngtxjgAAAYqJvI3z4D-CbEGFQgLZgFhLt693tCzicDlDnKI2Y1CSQ7mUDYH2aFm4GWg2y1rGqtaAqOtTqY4FrmqT; li_cc=AQGdDi925dOP2gAAAYqJwqsmdNmIsnnNDNGXnAA5tYVywXcv3UywL0w9xBkYpMUcVxlcju8a-a6Q; li_ce=AQFze3547sKWfAAAAYqR0iXOckpq1tiJVF3fDsTzxb6e_qvI7XzlFwyP355BrXUrsMoURlA5ryRgLEA; lang=v=2&lang=zh-cn; UserMatchHistory=AQKjM7tfoIKsAwAAAYqR0sJ2vpJpNoz4VLog-dHm--ED906kJGo5hdyX7FzIBmwWu9F8p0FfqCk4xhn2hU2UeKKxvb59gE11OXtSL2ZTer9AcIEbAlvUbNf9K2cbD7eWNimeMhwjA5UPTPfO9bmwYxLN0uK3wGp1gtvHab2qQlJCgEwwJCUdZmk3FgjpST7U_0ZEYC7KWiHWUjGtIqqtyCTwi78SwAzs0DC3-JpujJHX0AsvX1p_PyM3u4G_eCaBnuyW3u5cIGURBp4y4GTmz96a51_-n19kT-6xc1sttRKFlO0jjRI8h9ohujw1TzC_vBXgcK07M2HhPr9tYWwqXSFaHdkG3QQ; lidc="b=VB11:s=V:r=V:a=V:p=V:g=4626:u=2:x=1:i=1694663624:t=1694749982:v=2:sig=AQFZvB9aGJeWrXm14_YTPAM2jZCHyh8j"; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19615%7CMCMID%7C31367952125213229851655174128493962145%7CMCAAMLH-1695268425%7C3%7CMCAAMB-1695268425%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1694670825s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1613452186
Csrf-Token:ajax:2210591134930550786
Pragma:no-cache
Referer:https://www.linkedin.com/company/amazon/posts/?feedView=images
Sec-Ch-Ua:"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"
Sec-Ch-Ua-Mobile:?0
Sec-Ch-Ua-Platform:"Windows"
Sec-Fetch-Dest:empty
Sec-Fetch-Mode:cors
Sec-Fetch-Site:same-origin
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203
X-Li-Lang:zh_CN
X-Li-Page-Instance:urn:li:page:companies_company_posts_index;372b92df-21e7-408a-907f-360d2cf94bbe
X-Li-Pem-Metadata:Voyager - Organization - Member=organization-feed-updates
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


def search(name,nid):
    params = {
        "companyUniversalName": nid,
        "count": 10,
        "moduleKey": 'ORGANIZATION_MEMBER_FEED_DESKTOP',
        "numComments": 0,
        "numLikes": 0,
        "q": 'companyFeedByUniversalName',
    }
    count_ = 0
    for page in range(0,3):
        api = f'https://www.linkedin.com/voyager/api/organization/updatesV2'
        params["start"] = page * 30
        dict_map = {}
        response = send_get(api, headers, params).json()
        params["paginationToken"] = response.get("data").get("metadata").get("paginationToken")
        response = response.get("included")
        for it in response:
            try:
                shareUrn = it.get("*socialDetail", "")
                try:
                    commentary = it.get("commentary", {}).get("text", {}).get("text")
                except:
                    commentary = ""

                try:
                    actorurn = it.get("actor", {}).get("urn")
                except:
                    actorurn = "-"

                if nid not in str(actorurn):
                    continue
                updateMetadata = it.get("updateMetadata",{}).get("urn")
                subDescription = it.get("actor", {}).get("subDescription", {}).get("text")
                if shareUrn is None or shareUrn == "" or commentary == "":
                    continue
                saveitem = {
                    "search_company": name,
                    "actorurn": actorurn,
                    "updateMetadata":updateMetadata,
                    "shareUrn": shareUrn,
                    "commentary": commentary,
                    "subDescription": subDescription
                }
                print(saveitem)
                dict_map[shareUrn] = saveitem
            except Exception as e:
                print(f"key error:{e}")
        print(10 * "*")
        for it in response:
            try:
                urn = it.get("socialDetailEntityUrn")
                if urn not in dict_map.keys():
                    continue
                numLikes = it.get("numLikes")
                numComments = it.get("numComments")
                numShares = it.get("numShares")
                if urn is None or numShares is None:
                    continue
                print(urn, numLikes, numShares, numComments)
                dict_map[urn]["numLikes"] = numLikes
                dict_map[urn]["numComments"] = numComments
                dict_map[urn]["numShares"] = numShares

                print(dict_map[urn])

                count_+=1

                if count_>10:
                    return


                with open("company.txt", 'a', encoding='utf-8') as f:
                    f.write(json.dumps(dict_map[urn]))
                    f.write('\n')
            except Exception as e:
                print(f"value error:{e}")


if  __name__ == "__main__":

    # search("Amazon",'1586')
    # search("google",'1441')
    # search("linkedin",'1337')
    #
    # search("Microsoft", '1035')
    # search("IBM", '1009')
    # search("Tesla", '15564')
    # search("Meta", '10667')
    # search("Netflix", '165158')
    # search("Walt Disney", '1292')
    # search("Accenture", '1033')
    """
    Shopee
    Lazada
    DBS
    grab
    Flex
    Singapore Airlines
    UOB
    Garena
    SIngtel
    Razer
    """
    search("Shopee", '6451760')
    search("Lazada", '2725478')
    search("DBS", '163379')
    search("grab", '5382086')
    search("Flex", '2279')
    search("Singapore Airlines", '1887052')
    search("UOB", '6883')
    search("Garena", '13678254')
    search("SIngtel", '5334')
    search("Razer", '56737')

    with open("company.txt",'r',encoding='utf-8') as f:
        lines = [json.loads(i.strip()) for i in f.readlines()]
    df = pandas.DataFrame(lines)
    df.to_excel("company_post.xlsx",index=False)