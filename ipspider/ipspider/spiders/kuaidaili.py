# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time


class KuaidailiSpider(CrawlSpider):
    name = 'kuaidaili'
    allowed_domains = ['kuaidaili.com']
    start_urls = ['https://www.kuaidaili.com/free/']

    rules = (
        Rule(LinkExtractor(allow=r'/free/inha/\d+/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        time.sleep(2)
        ip_list = []
        tr_list = response.xpath('//table[@class="table table-bordered table-striped"]//tbody/tr')
        for tr in tr_list:
            item = {}
            item["type"] = tr.xpath('./td[4]/text()').extract_first()
            item["ip"] = tr.xpath('./td[1]/text()').extract_first()
            item["port"] = tr.xpath('./td[2]/text()').extract_first()
            ip_list.append(item)
            yield ip_list
            # return item
