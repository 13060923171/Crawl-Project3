# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BlblItem(scrapy.Item):
    # # define the fields for your item here like:
    # # name = scrapy.Field()
    # pass
    rank_tab=scrapy.Field()
    rank_num =scrapy.Field()
    id=scrapy.Field()
    title =scrapy.Field()
    author =scrapy.Field()
    score =scrapy.Field()
    view=scrapy.Field()
    danmaku=scrapy.Field()
    reply=scrapy.Field()
    favorite=scrapy.Field()
    coin=scrapy.Field()
    share=scrapy.Field()
    like=scrapy.Field()
    tag_name=scrapy.Field()
