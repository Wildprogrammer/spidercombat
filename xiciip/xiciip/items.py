# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiciipItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ipItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    address = scrapy.Field()
    type = scrapy.Field()
    protocol = scrapy.Field()
    speed = scrapy.Field()
    time = scrapy.Field()
    alive = scrapy.Field()
    proof = scrapy.Field()