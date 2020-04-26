# -*- coding: utf-8 -*-
import scrapy
from yangguang.items import YangguangItem


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest']

    def parse(self, response):
        li_list = response.xpath('//ul[@class="title-state-ul"]/li')
        for li in li_list:
            item = YangguangItem()
            item["state"] = li.xpath('.//span[@class="state2"]/text()').extract_first()
            item["title"] = li.xpath('.//span[@class="state3"]/a/text()').extract_first()
            item["href"] = 'http://wz.sun0769.com' + li.xpath('.//span[@class="state3"]/a/@href').extract_first()
            # print(item)
            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item": item}
            )
        next_url = 'http://wz.sun0769.com' + response.xpath(
            '//div[@class="mr-three paging-box"]/a[2]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["content"] = response.xpath('//div[@class="details-box"]/pre/text()').extract_first()
        item["content_img"] = response.xpath('//div[@class="mr-three"]/div[3]/img/@src').extract_first()
        # print(item)
        yield item
