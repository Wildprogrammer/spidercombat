# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import time


class WallpaperSpider(CrawlSpider):
    name = 'wallpaper'
    # download_delay = 2
    allowed_domains = ['win4000.com']
    start_urls = ['http://www.win4000.com/wallpaper.html']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.win4000.com/wallpaper_detail_\d+.html',
                           restrict_xpaths='//div[@class="main_cont"]/div[@class="list_cont list_cont1 w1180"]//ul[@class="clearfix"]/li/a'),
             callback='parse_item'),
    )

    def parse_item(self, response):
        # item={}
        # img_list=response.xpath('//ul[@id="scroll"]/li/a/img/@src').extract()
        # item["img_list"]=img_list
        img_list = response.xpath('//ul[@id="scroll"]/li')
        for img in img_list:
            item = {}
            item['image'] = img.xpath('./a/img/@data-original').extract_first()
            print(item)
            yield item

        # print(item)
        # yield item
