# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YangguangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    state=scrapy.Field()
    content= scrapy.Field()
    href= scrapy.Field()
    title=scrapy.Field()
    content_img=scrapy.Field()