# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GpannounItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题,发布者,发布日期,公告正文,公告链接
    TITLE = scrapy.Field()
    PUBLISHER = scrapy.Field()
    PUBLISH_DATE = scrapy.Field()
    ARTICLE = scrapy.Field()
    ANNOUN_URL = scrapy.Field()