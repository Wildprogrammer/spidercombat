# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningbookItem(scrapy.Item):
    # define the fields for your item here like:
    detail_url= scrapy.Field()
    page_url=scrapy.Field()
    # kind_url=scrapy.Field()
    kind = scrapy.Field()
    title=scrapy.Field()
    price= scrapy.Field()
    publish=scrapy.Field()
    publish_time=scrapy.Field()
    author=scrapy.Field()