# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DjangospidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #博主
    author = scrapy.Field()
    #博主简介
    author_brief = scrapy.Field()
    #博文
    post = scrapy.Field()
    #博文详情
    post_detail = scrapy.Field()
    #发表时间
    post_time = scrapy.Field()
    #item_unique id
    itemid = scrapy.Field()

