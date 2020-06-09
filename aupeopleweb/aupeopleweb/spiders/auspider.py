# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class AuspiderSpider(CrawlSpider):
    name = 'auspider'
    allowed_domains = ['aupeopleweb.com.au']
    start_urls = ['https://aupeopleweb.com.au/1/aupeople/plugin.php?id=aljlp&page=1']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@id="normal-list"]//div[@class="media-body-title"]/a[1]'),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pagenav clearfix sep"]/div[@class="pg"]'),follow=True),
    )

    def parse_item(self, response):
        item = {}
        item['name']=re.sub(r'\xa0','',response.xpath('//h2/text()').extract_first())
        item['tel']=response.xpath('//span[@id="num"]/text()').extract_first()
        item['area']=response.xpath('//span[@class="long"]/a[1]/text()').extract_first()
        print(item)
        return item
