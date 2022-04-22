import scrapy
from blbl.items import BlblItem
import json
import copyheaders

class BlSpider(scrapy.Spider):
    name = 'bl'
    allowed_domains = ['bilibili.com']
    # start_urls默认为'http：//'+allowed_domains[0]
    # 所以这里我们要重写start_urls，把排行榜页面的url列表赋值给start_urls
    start_urls = [
        # 'https://www.bilibili.com/v/popular/rank/all',
        # 'https://www.bilibili.com/v/popular/rank/douga',
        # 'https://www.bilibili.com/v/popular/rank/guochuang',
        # 'https://www.bilibili.com/v/popular/rank/music',
        # 'https://www.bilibili.com/v/popular/rank/dance',
        # 'https://www.bilibili.com/v/popular/rank/game',
        # 'https://www.bilibili.com/v/popular/rank/tech',
        # 'https://www.bilibili.com/v/popular/rank/life',
        # 'https://www.bilibili.com/v/popular/rank/kichiku',
        # 'https://www.bilibili.com/v/popular/rank/fashion',
        # 'https://www.bilibili.com/v/popular/rank/ent',
        'https://www.bilibili.com/v/popular/rank/cinephile',
        'https://www.bilibili.com/v/popular/rank/car'
    ]
    headers = copyheaders.headers_raw_to_dict(b"""
    accept: application/json, text/plain, */*
    accept-language: zh-CN,zh;q=0.9
    cookie: buvid3=9CEC4F0F-0D95-CF25-D34F-7F96F1CA2A1A39360infoc; i-wanna-go-back=-1; _uuid=8B128D1010-A2BD-61089-762A-10DB2510FDF37C39344infoc; buvid4=670943B6-B3A7-069B-0062-5338DEEC416A40351-022032001-xdRu6UKxhSQszd00OL8qiQ%3D%3D; rpdid=|(umuum||kkR0J'uYR~~|mlRR; fingerprint=50d5c9025eaa806940343ee50d3f0dc2; buvid_fp_plain=undefined; buvid_fp=13d6429bb415a7edf11f62f8ba981782; SESSDATA=5b71daf4%2C1663654701%2Cd6a10%2A31; bili_jct=08f2dac0e08371eb8acef6b8b597324c; DedeUserID=68451030; DedeUserID__ckMd5=e48931738cbc5eac; sid=6apm0eh9; b_ut=5; bp_video_offset_68451030=640292968651030500; CURRENT_BLACKGAP=0; blackside_state=0; b_lsid=FBE3A8CB_1803D120BE2; PVID=5; is-2022-channel=1; innersign=1; CURRENT_FNVAL=4048
    origin: https://www.bilibili.com
    referer: https://www.bilibili.com/video/BV1Su411C7d8?spm_id_from=333.1073.high_energy.content.click
    sec-ch-ua: "Chromium";v="21", " Not;A Brand";v="99"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    sec-fetch-dest: empty
    sec-fetch-mode: cors
    sec-fetch-site: same-site
    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
    """)

    def parse(self, response):
        # 获取当前爬取的榜单
        rank_tab = response.xpath('//ul[@class="rank-tab"]/li[@class="rank-tab--active"]/text()').getall()[0]
        print('=' * 50, '当前爬取榜单为:', rank_tab, '=' * 50)

        # 视频的信息都放在li标签中，这里先获取所有的li标签
        # 之后遍历rank_lists获取每个视频的信息
        rank_lists = response.xpath('//ul[@class="rank-list"]/li')
        for rank_list in rank_lists:
            rank_num = rank_list.xpath('./@data-rank').get().split('/av')[-1]
            title = rank_list.xpath('div/div[@class="info"]/a/text()').get()
            # 抓取视频的url，切片后获得视频的id
            id = rank_list.xpath('./@data-id').get().split('/av')[-1]
            # 拼接详情页api的url
            Detail_link = f'https://api.bilibili.com/x/web-interface/archive/stat?aid={id}'
            Labels_link = f'https://api.bilibili.com/x/web-interface/view/detail/tag?aid={id}'
            author = rank_list.xpath('div/div[@class="info"]/div[@class="detail"]/a/span/text()').get()
            score = rank_list.xpath('div/div[@class="info"]/div[@class="pts"]/div/text()').get()
            # 如用requests库发送请求，要再写多一次请求头
            # 因此我们继续使用Scrapy向api发送请求
            # 这里创建一个字典去储存我们已经抓到的数据
            # 这样能保证我们的详细数据和排行数据能一 一对应无需进一步合并
            # 如果这里直接给到Scrapy的Item的话，最后排行页的数据会有缺失
            items = {
                'rank_tab': rank_tab,
                'rank_num': rank_num,
                'title': title,
                'id': id,
                'author': author,
                'score': score,
                'Detail_link': Detail_link
            }
            # 将api发送给调度器进行详情页的请求，通过meta传递排行页数据
            print(f'>>>url: {Labels_link}')
            yield scrapy.Request(url=Labels_link, callback=self.Get_labels, meta={'item': items}, dont_filter=True,headers=self.headers)

    def Get_labels(self, response):
        # 获取热门标签数据
        items = response.meta['item']
        Detail_link = items['Detail_link']
        # 解析json数据
        html = json.loads(response.body)
        Tags = html['data']  # 视频标签数据
        # 利用逗号分割列表，返回字符串
        tag_name = ','.join([i['tag_name'] for i in Tags])
        items['tag_name'] = tag_name
        yield scrapy.Request(url=Detail_link, callback=self.Get_detail, meta={'item': items}, dont_filter=True)

    def Get_detail(self, response):
        # 获取排行页数据
        items = response.meta['item']
        rank_tab = items['rank_tab']
        rank_num = str(items['rank_num'])
        title = items['title']
        id = items['id']
        author = items['author']
        score = str(items['score'])
        tag_name = str(items['tag_name'])

        # 解析json数据
        html = json.loads(response.body)

        # 获取详细播放信息
        stat = html['data']

        view = stat['view']
        danmaku = stat['danmaku']
        reply = stat['reply']
        favorite = stat['favorite']
        coin = stat['coin']
        share = stat['share']
        like = stat['like']

        # 把所有爬取的信息传递给Item
        item = BlblItem(
            rank_tab=rank_tab,
            rank_num=rank_num,
            title=title,
            id=id,
            author=author,
            score=score,
            view=view,
            danmaku=danmaku,
            reply=reply,
            favorite=favorite,
            coin=coin,
            share=share,
            like=like,
            tag_name=tag_name
        )
        print(item)
        yield item