# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiubaidbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 声明属性
    author = scrapy.Field()
    content = scrapy.Field()
