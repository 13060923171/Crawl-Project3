import datetime  ##时间格式化
import json ##json序列化工具包，这里用来反序列化json数据为python类型数据
import os ##操作环境遍历，这里用来设置vpn代理地址，便于python能访问到外网
import random  ##随机操作函数，这里用来设置随机休眠时间
import re ##正则库，用来正则匹配
import time ##时间操作和线程休眠
import pandas ##数据导出
import requests ##网络发包库



##爬虫主要工具类
class Gtwitter():

    ##帖子接口
    search_api = 'https://twitter.com/i/api/graphql/NA567V_8AFwu0cZEkAAKcw/SearchTimeline'
    ##帖子存放列表
    resulst = []


    ##实例化方法
    def __init__(self,max_page):
        ##再实例化方法中添加每个关键字的采集的最大页码
        self.max_page = max_page


    def getblog(self,params): ##该方法主要用来发送获取博文
        while 1: ##
            try:##捕获页码
                cookie =random.choice(cookies)###随机获取一个账户信息

                sctoken = ''.join(re.findall(r'ct0=(.*?);', cookie)[:1])##从账户的cookie信息中正则匹配到从csrf-token字段
                ##网络请求头，从浏览器复制过来的
                headers = {
                    'Accept': '*/*',
                    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                    'Content-Type': 'application/json',
                    'Cookie': cookie,
                    'Referer': 'https://twitter.com/search?f=live&q=%22blackberry%22%20until%3A2023-06-29%20since%3A2018-06-23&src=typed_query',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
                    'X-Csrf-Token': sctoken,
                    'X-Twitter-Active-User': 'yes',
                    'X-Twitter-Auth-Type': 'OAuth2Session',
                    'X-Twitter-Client-Language': 'en'
                }###发送网络请求
                res = requests.get(
                    self.search_api,##请求地址
                    headers=headers,##请求头
                    params=params,##请求参数
                    timeout=(3,4)##请求超时时间
                )##判断当前请求是否因为账户限制访问，而没有获取到数据
                if 'Rate limit exceeded' in res.text:
                    print(f'Rate limit exceeded')
                    time.sleep(20)
                ##判断当前请求是否为正常响应请求，异常情况包括请求参数无法解析、网络波动、账户反爬等常见限制
                if res.status_code != 200:
                    print(res.status_code, res.text)
                    time.sleep(1)
                    continue
                return res.json()###正常请求，返回json数据

            except Exception as e:
                ##异常请求，重新发送链接
                print(f">>> parse error: {e}")
                time.sleep(1)




    def parse(self,data, enname, page,zhname,records):
        try:
            tweets = data.get("data").get("search_by_raw_query").get("search_timeline").get("timeline").get("instructions")[0].get("entries")###获取到博文的列表
        except Exception as e:
            print(f">>> error: {e}")
            time.sleep(1)
            return 0
        if tweets is None:
            tweets = []
        for it in tweets[:-2]:##遍历列表中的信息，提取到每一个博文需要的字段信息，解析方法为json格式解析
            try:
                dic = {}
                dic['关键词en'] = enname
                dic['关键词zhname'] = zhname
                dt_obj = datetime.datetime.strptime(
                    it['content']['itemContent']['tweet_results']['result']['legacy']['created_at'],
                    '%a %b %d %H:%M:%S %z %Y')
                dic['发表日期'] = dt_obj.astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')
                dic['用户名'] = \
                it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    'name']
                dic['账号id'] = \
                it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    'screen_name']
                a = it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    'screen_name']
                dic['个人主页'] = f'https://twitter.com/{a}'
                dic['发表内容'] = it['content']['itemContent']['tweet_results']['result']['legacy']['full_text']
                dic['博文id'] = it['content']['itemContent']['tweet_results']['result']['legacy']['id_str']
                dic['回复数量'] = it['content']['itemContent']['tweet_results']['result']['legacy']["reply_count"]
                dic['转发数量'] = it['content']['itemContent']['tweet_results']['result']['legacy']["retweet_count"]
                dic['点赞数'] = it['content']['itemContent']['tweet_results']['result']['legacy']["favorite_count"]
                dic['引用数量'] = it['content']['itemContent']['tweet_results']['result']['legacy']["quote_count"]
                try:
                    dic['浏览量'] = it['content']['itemContent']['tweet_results']['result']['views']["count"]
                except:
                    dic['浏览量'] = 0
                idd = it['content']['itemContent']['tweet_results']['result']['legacy']['id_str']
                dic['推文链接'] = f'https://twitter.com/Olympics/status/{idd}'
                dic['粉丝数量'] = \
                it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    "followers_count"]
                dic['关注数量'] = \
                it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    "friends_count"]
                dic['地理位置'] = \
                it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    "location"]
                print(enname,zhname,page,dic["发表日期"],dic["发表内容"])
                with open("temp.txt",'a',encoding='utf-8') as f:
                    f.write(json.dumps(dic))
                    f.write('\n')

            except:
                pass
        return tweets



    def generXlsx(self):
        try:
            with open("temp_first2.txt", 'r', encoding='utf-8') as f:
                resulst = [json.loads(i.strip()) for i in f.readlines()]

            pandas.DataFrame(resulst).to_excel(f"result2-{int(time.time())}.xlsx",index=False)
        except Exception as e:
            print(f">>> 拉取数据库 error:{e}")

    def changev(self,text):
        try:
            dt_obj = datetime.datetime.strptime(text, '%a %b %d %H:%M:%S %z %Y')
            return dt_obj.astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')

        except Exception as e:
            print(f">>> 时间格式异常： {text}")
            return text

    def blockdata(self,enname,zhname):
        records = []
        cursor = {"p":''}##控制下一页的页码


        for page in range(1,self.max_page):##遍历页码
            try:
                params = {
                    "fieldToggles": '{"withArticleRichContentState":false}',
                    "features": '{"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}',
                    "variables": json.dumps({"rawQuery":f"\"{enname}\" lang:en until:2023-09-14 since:2020-09-14","count":20,"cursor":cursor["p"],"querySource":"typed_query","product":"Latest"})
                }##构建请求参数
                blogInfo = self.getblog(params)##通过本地封装的函数，获取当前参数下的博文的原始json信息

                tweets = self.parse(blogInfo, enname, page,zhname,records)##通过本地封装的函数，去解析原始json信息
                pagelength = len(tweets)-2##解析到当前页的博文长度：这里-2是因为后面两项是翻页（上一页、下一页）的元素
                print(f">>> pagelength:{pagelength}")

                if pagelength < 0:##判断页码长度
                    break
                else:
                    ##获取到下一页的游标
                    if page == 1 and cursor["p"] == "":

                        cursor["p"] = tweets[-1].get("content").get("value")
                    else:
                        instructions = blogInfo.get("data").get("search_by_raw_query").get("search_timeline").get("timeline").get("instructions")[-1]
                        cursor["p"] = instructions.get("entry").get("content").get("value")
                    print(f"下一页：{cursor['p']}")
                if cursor["p"] is None:##判断是否有下一页
                    print('暂无下一页：')
                    break
            except Exception as e:
                print(f"eroro{e}")
                break



def getdaterange(starttime,endtime):
    time_str = []
    start_samp = time.mktime(time.strptime(starttime, '%Y-%m-%d'))
    while True:
        time_str.append(time.strftime('%Y-%m-%d', time.localtime(start_samp)))
        start_samp += 24 * 60 * 60
        if start_samp > time.mktime(time.strptime(endtime, '%Y-%m-%d')):
            break
    return time_str


if  __name__ == "__main__":

    ##账号池
    cookies = [
        'ct0=5e7bd4ae3018934df3a4aaf03caaf92cfc8adac3ae5c7d45581f4dc1face5af7b93d7a6442efcffe4caafc80dc3671285c8c2c326fe75d79887224d23471dd14683dbfcd949423c8e250accce21c96a3; guest_id_marketing=v1%3A169441283378026239; guest_id_ads=v1%3A169441283378026239; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCPcD4IKKAToMY3NyZl9p%250AZCIlNmI1MTAwOWQ4OWU2NGE5ZjYwZTQ1OWEyOTg0YWI1Y2I6B2lkIiVkYTQ5%250AYTQzODBhMDk4MzU2MDUzOTBiM2QxYzg2YjcwNA%253D%253D--f90441c5710806cc92da782e8d6e9424a377cbb1; personalization_id="v1_tvAqBgp8gbt08b4gYmA1Bg=="; guest_id=v1%3A169441283378026239; kdt=XSQocHE5t4CYxrYgPtXOhljzNrSH0ZQ4abR58Sdj; twid="u=1701116888867106816"; auth_token=fa6ce9b7a2d4bd31a7c44bfbcbb6a430cc6acabb',
        'guest_id_marketing=v1%3A169166115591780722; guest_id_ads=v1%3A169166115591780722; personalization_id="v1_9o9FhJK39A9waXIP7XYN2A=="; guest_id=v1%3A169166115591780722; ct0=8f9d63b4b4b676158dea3571a419114a95e348209a80b1aaefb0714d4220c2681673b80e32206eff68feff0e1ba12507fd3c1b8c084171ea2d267b237ef67bc2aec28d5e1a660d1c916a99878d83d7d3; _ga=GA1.2.505451109.1691661156; kdt=YQKWYPd1AHeddxUAK2mD7nioOufdDtpSBvXNbvCJ; twid=u%3D1677970978469711878; auth_token=ab4c712609e09a17098791f771653078bbcb6ffe; lang=en; _gid=GA1.2.1871236937.1694872179',
        '_ga=GA1.2.544820069.1694872147; _gid=GA1.2.237328157.1694872147; guest_id=v1%3A169487214989525801; guest_id_marketing=v1%3A169487214989525801; guest_id_ads=v1%3A169487214989525801; gt=1703044636997280148; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCLNXRZ6KAToMY3NyZl9p%250AZCIlN2UxNTA1ODNjMDNhOGIwZWRlZTE4ODYxZDQ2MTIxOWU6B2lkIiVlOWNj%250AOTcxZThiYzBmNDBhYzI4OWQ5NDU1MWUzNzBiOQ%253D%253D--b824d994701cb0d993efa658b08adafe85c58fef; kdt=cuXBIcdowS9AFMKCuKSWftV5eZRLmt6ttbQNiths; auth_token=5e607f7cb3c3bf4dbc4079378c77a4c65f5e49bd; ct0=95054246d19d09408e6eab5146e62387138f7782d2e2da3c3ce20c495c06f983d7a2670aaf4a596239e41e5cc7cf9095180de744a3bc98395c18417158734690d790cad3d070f23561ae1ae1e4b3f031; lang=en; twid=u%3D1677960686872465409; personalization_id="v1_nNPCT5jjZr4i/pIS0e0qnQ=="',
        '_ga=GA1.2.544820069.1694872147; _gid=GA1.2.237328157.1694872147; gt=1703044636997280148; kdt=cuXBIcdowS9AFMKCuKSWftV5eZRLmt6ttbQNiths; dnt=1; auth_multi="1677960686872465409:5e607f7cb3c3bf4dbc4079378c77a4c65f5e49bd"; auth_token=5ac9aa94b863a6495d3982d28a7da7313e35a629; guest_id=v1%3A169487259833497962; ct0=e702b4699242025fb6f1bcaf96d1b2f1bce9a2eedd883b2a0f9d74b702fb2334deaac0b333bfcb750c0ed45e77915422911a69ad590718240aa2764dd57510aea880578964510a810a6559173bf843af; guest_id_ads=v1%3A169487259833497962; guest_id_marketing=v1%3A169487259833497962; personalization_id="v1_CRpnNauyVPs0BmQpWqF02Q=="; twid=u%3D1677969021592043521',
        '_ga=GA1.2.544820069.1694872147; _gid=GA1.2.237328157.1694872147; gt=1703044636997280148; kdt=cuXBIcdowS9AFMKCuKSWftV5eZRLmt6ttbQNiths; lang=en; dnt=1; auth_multi="1677969021592043521:5ac9aa94b863a6495d3982d28a7da7313e35a629|1677960686872465409:5e607f7cb3c3bf4dbc4079378c77a4c65f5e49bd"; auth_token=e96012645b95e5941663ae0b39cb2756d2f2d398; guest_id=v1%3A169487267552511573; ct0=dc68f1fd2150201aefdf0c0794b16934de5df4d4660a72f64112d13aa9aeb208c6c3dbf21acfa52c986374daf8f59dba79445be45d8729c15ae8a8c296baea019c1366744fb97d01f2fdae927cf9872e; guest_id_ads=v1%3A169487267552511573; guest_id_marketing=v1%3A169487267552511573; twid=u%3D1677970978469711878; personalization_id="v1_sHhiilAUsqeXLxF4Vbsh1Q=="',
        '_ga=GA1.2.544820069.1694872147; _gid=GA1.2.237328157.1694872147; gt=1703044636997280148; kdt=cuXBIcdowS9AFMKCuKSWftV5eZRLmt6ttbQNiths; dnt=1; auth_multi="1677970978469711878:e96012645b95e5941663ae0b39cb2756d2f2d398|1677969021592043521:5ac9aa94b863a6495d3982d28a7da7313e35a629|1677960686872465409:5e607f7cb3c3bf4dbc4079378c77a4c65f5e49bd"; auth_token=828093581af38971295a349235938e253c9e6d7a; guest_id=v1%3A169487276783555871; ct0=6c4129933a80b80274671bfb5c37488194f1e26b824186b6f514b8dda10c0fc03d1ae6f2204d5c1350a3c851f5c1e534a1124a02f52da420d43616ba4585542d4ee4a1d90ac5e671f78d3e4dff4c0f2c; guest_id_ads=v1%3A169487276783555871; guest_id_marketing=v1%3A169487276783555871; twid=u%3D1677932686739120128; personalization_id="v1_7XX9lX+LDpkoOUhfXslgOA=="',
        '_ga=GA1.2.544820069.1694872147; _gid=GA1.2.237328157.1694872147; gt=1703044636997280148; kdt=cuXBIcdowS9AFMKCuKSWftV5eZRLmt6ttbQNiths; dnt=1; auth_multi="1677932686739120128:828093581af38971295a349235938e253c9e6d7a|1677970978469711878:e96012645b95e5941663ae0b39cb2756d2f2d398|1677969021592043521:5ac9aa94b863a6495d3982d28a7da7313e35a629|1677960686872465409:5e607f7cb3c3bf4dbc4079378c77a4c65f5e49bd"; auth_token=590bb7a85b220b6e7ffd032d06457459bb24ce90; guest_id=v1%3A169487380403473493; ct0=56a59709da02c98ae54e1fdf68fb099eacc5d6ae2f77269560570512f8ea1916caac1b9f9d98ad4444ddd21c97aea719c4c0b4c76afc508ce50d8f633ca6e0afb0e4096727e77df4a7774688348f495a; guest_id_ads=v1%3A169487380403473493; guest_id_marketing=v1%3A169487380403473493; twid=u%3D1701237556946333697; personalization_id="v1_f7RY+RIps+0vvrsNUGBDkw=="',
        'ct0=44a33b7c496fb4d8335ea0bf84de6defaf7a7c3039c24b3fdf830efbd991d219159041d0d2980fa3af83a62979003512b1be432eddb428a075e93d337f2b413203b32b63c2f9b55cb89a5e8469295cdc; guest_id_marketing=v1%3A169270740614619225; guest_id_ads=v1%3A169270740614619225; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCERBOR2KAToMY3NyZl9p%250AZCIlMjQ1ZGQ2ZWZkMjZkNTdkYTEzM2ZhOTEwNWRhZjU2NTc6B2lkIiVkNDhj%250ANDYzNTdmOWY1MTE1Yjc1NWUyN2Q4ZDg2N2MyNg%253D%253D--2a4cfdd960229219f0a30f55c6bf18a7b557aa8b; personalization_id="v1_WXACyQi7vScqB1cWoVmg3g=="; guest_id=v1%3A169270740614619225; kdt=TzyHerqZ1oiFH2lJ6fCUS9D1EdlVw8hKopmxqkKo; twid="u=1693963826822070272"; auth_token=35b2133de68351647b7ac91dc0e8060d12cde547',
        'ct0=4890661f00dd8c126a00f8cb166767834fc7185befc725b0001648d82843fbda6684be6080d8601c44eb5adde7dc422a6e26007779494961a9ecac16fd560d803a380270dc0e30645d358688f6f00b78; guest_id_marketing=v1%3A169270739055487428; guest_id_ads=v1%3A169270739055487428; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCF4EOR2KAToMY3NyZl9p%250AZCIlYmVkZjc1OGEzOGQwMDYxMDA3ZWI3ODgyYWQ2NjlmYzA6B2lkIiViYjIw%250AMzkwODBkNzA1YmQ5MzRlNGZhNGI5YjQzNGJjYQ%253D%253D--81c17d78acb40a9e672a8372bcd0ca33d69dc8c8; personalization_id="v1_JyO9fao+SxbXnRA6g9Mh6w=="; guest_id=v1%3A169270739055487428; kdt=3n2U54IGfWhnIXO03Bu0bBw5T3lL3tzso3mb3pSg; twid="u=1693963761990987776"; auth_token=9866a35b4ac4dfa578f707974ccac4e6591d7d09',
        'ct0=ff303e6fae71b23b26ddad90c4655f7465e29e4dd2c213ed35d29da52ff96154153de5b9082dcc2b3e2bb0bfa3af66cee001c4b9d03fe0cc5a39a458c763fd5df02f19d2f69dfd938409b3fc4d4432e3; guest_id_marketing=v1%3A169270738205367590; guest_id_ads=v1%3A169270738205367590; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCjjOB2KAToMY3NyZl9p%250AZCIlYjA0NDkxMzFiOWVmMDdlYzVhZjYxOTNlZDU0ZWQyYTU6B2lkIiU1NjM0%250AZDY5MGZhN2RkYTg3ODc5YmVhNzI0NDEzYTk5Ng%253D%253D--b9ad78a68f8b061e6f0f54311a1bb98dbb05ba7c; personalization_id="v1_U0mT5HoBawRQJTD0IjvhEg=="; guest_id=v1%3A169270738205367590; kdt=YJTfLxgUtqpDTlObHj5csZ96rqiO1YX8Y5RiRPOs; twid="u=1693963705979944961"; auth_token=84a85014ab3e190a02b4116528cca88859e02870',
        'ct0=34660933a67870b67f93c4f03c055a7dcc3224bb23017b838c68deef3bcf8a2c7062c49ef2b3e2efc4f6c9a726885ba23f6cdd2cd237c2fc263b1f260765bb3f72d2cb9508baca709650cdd31aba7124; guest_id_marketing=v1%3A169270735486186461; guest_id_ads=v1%3A169270735486186461; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCPB4OB2KAToMY3NyZl9p%250AZCIlYTk3MTFlMTliYTcyNzgxMGQ1NDU2N2YwM2FjOGZhMWY6B2lkIiU5Mjlk%250AYjg0MjIyZTJkZjM5ZjdhMTMzNzZlM2EyNDg2MQ%253D%253D--480e05ce215a47c099e88cbf96d1175a44faa505; personalization_id="v1_Bmi7JsF1aEO9XEi/bABRgQ=="; guest_id=v1%3A169270735486186461; kdt=Ix6necP3dTCEpl6Tnx3vifHi2cKynGclbXGgwUEh; twid="u=1693963639542394880"; auth_token=0ea45a2fdc5ccb957b1043e5fe5855c50da1d6a5',
        'ct0=61abc8fd2937fc871b44839674c1260edc9f93f82b74a5be39d588887390461b6073b0d8f01298a320f0b848375a5b64f57ce15b712cc607b5ad2cdff05fbee7d465fc79ee36da4df2df5f1fcf8ba38b; guest_id_marketing=v1%3A169270735388062274; guest_id_ads=v1%3A169270735388062274; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCB11OB2KAToMY3NyZl9p%250AZCIlMWM3ZjY0ODc1MDAzZDEzMmRiNTUwZDdjZTRkMmZmN2E6B2lkIiVhYTE0%250AYjk0ZDE1NWQzOGVjYmQyYzhmMDQ1NzZmNGQwYQ%253D%253D--c723c50441965c27b1fec7932efd7655dd890eb3; personalization_id="v1_u4XZr0kGw7HX5odeygzrIQ=="; guest_id=v1%3A169270735388062274; kdt=ZeKpbgHL2TxLDnYST3vInIQDl7Kvx1rnCGUnAItu; twid="u=1693963607107624960"; auth_token=0390fe9e9740bf143d9530a633ca697bae8a462a',
    ]
    tt = Gtwitter(3000)

    ##待采集的关键字
    params_data ="""
    计算机科学与信息系统	Computer Science and Information Systems
    土木工程	Civil Engineering
    机械工程	Mechanical Engineering
    电子工程	Electronic Engineering
    航空航天工程	Aeronautical Engineering
    医学	Medicine
    护理学	Nursing
    生物科学	Biological Sciences
    药学	Pharmacy
    公共卫生	Public Health
    物理	Physics
    化学	Chemistry
    生物学	Biology
    环境科学	Environmental Sciences
    地理科学	Geographical Sciences
    经济学	Economics
    心理学	Psychology
    社会学	Sociology
    政治学	Political Science
    管理学	Management
    历史学	History
    文学	Literature major
    文学	Literature major
    艺术学	Art Studies
    音乐学	Music Studies
    法律学	Law Studies
    国际法	International Law
    商法	Commercial Law
    刑法	Criminal Law
    环境法	Environmental Law
    """

    ##关键字分割
    params_data_ = [(i.strip().split('\t')[-1],i.strip().split('\t')[0]) for i in params_data.split('\n') if i.strip() != '']

    ##遍历关键字，采集每一个关键字信息
    for enname,zhname in params_data_:
        print(enname,zhname)
        tt.blockdata(enname=enname, zhname=zhname)

    with open("temp.txt",'r',encoding='utf-8') as f:
        lines = [json.loads(i.strip()) for i in f.readlines() ]
        df = pandas.DataFrame(lines)
        df.to_excel("处理结果.xlsx",index=False)
