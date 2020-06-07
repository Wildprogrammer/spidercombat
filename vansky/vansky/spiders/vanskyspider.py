# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class VanskyspiderSpider(CrawlSpider):
    name = 'vanskyspider'
    allowed_domains = ['vansky.com']
    start_urls = ['https://www.vansky.com/info/ZPQZ02.html']

    rules = (
        Rule(LinkExtractor(allow=r'adfree/\d+\.html',restrict_xpaths='//tr[@class="freeAdPadding"]'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'\?page=\d+',restrict_xpaths='//ul[@class="pagination"]'), follow=True),
    )

    def parse_item(self, response):
        print('*'*20)
        item = {}
        item['name']=response.xpath('//*[@id="af-content"]/div[2]/div/div[1]/div[1]/div/span[2]/text()').extract_first()
        item['tel']=response.xpath('//*[@id="info-phone"]/text()').extract_first()
        print(item)
        return item
