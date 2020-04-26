# -*- coding: utf-8 -*-
import scrapy_redis
import scrapy
from copy import deepcopy
from urllib import parse
import json


class JdspiderSpider(scrapy.Spider):
    name = 'jdspider'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath('//div[@class="mc"]/dl/dt')
        for dt in dt_list:
            item = {}
            item["a_kind"] = dt.xpath('./a/text()').extract_first()
            em_list = dt.xpath('./following-sibling::dd[1]/em')
            for em in em_list:
                item["detail_url"] = em.xpath('./a/@href').extract_first()
                item["b_kind"] = em.xpath('./a/text()').extract_first()
                if item["detail_url"] is not None:
                    item["detail_url"] = "https:" + item["detail_url"]
                    yield scrapy.Request(
                        item["detail_url"],
                        callback=self.detail_url,
                        meta={"item": deepcopy(item)}
                    )

    def detail_url(self, response):
        li_list = response.xpath('//ul[@class="gl-warp clearfix"]/li')
        for li in li_list:
            item = response.meta["item"]
            item["book_name"] = li.xpath('.//div[@class="p-name"]//em/text()').extract_first()
            item["book_name"] = item["book_name"].strip() if item["book_name"] != None else None
            item["book_author"] = li.xpath(
                './/div[@class="p-bookdetails"]/span[@class="p-bi-name"]/span/a/text()').extract_first()
            item["book_publish"] = li.xpath('.//span[@class="p-bi-store"]/a/text()').extract_first()
            item["publish_date"] = li.xpath(
                '//ul[@class="gl-warp clearfix"]/li//span[@class="p-bi-date"]/text()').extract_first()
            item["publish_date"] = item["publish_date"].strip() if item["publish_date"] != None else None
            item["book_sku"] = li.xpath('./div/@data-sku').extract_first()
            yield scrapy.Request(
                'https://p.3.cn/prices/mgets?type=1&skuIds=J_{}'.format(item["book_sku"]),
                callback=self.book_price,
                meta={"item": deepcopy(item)}
            )
        next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()
        if next_url is not None:
            next_url = parse.urljoin(response.url, next_url)
            item["detail_url"] = next_url
            yield scrapy.Request(
                next_url,
                callback=self.detail_url,
                meta={"item": item}
            )

    def book_price(self, response):
        item = response.meta["item"]
        item["book_price"] = json.loads(response.body.decode())[0]["op"]
        yield item
