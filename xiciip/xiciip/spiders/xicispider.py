# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from xiciip.items import ipItem
import requests


class XicispiderSpider(CrawlSpider):
    name = 'xicispider'
    # download_delay = 2
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn/']

    rules = (
        Rule(LinkExtractor(allow=r"/nn/\d+", restrict_xpaths='//div[@class="pagination"]'), callback="parse_item",
             follow=True),
    )#顺序是先请求匹配网址，在callback所以初始页面写第一页会被忽视，直接取了第二页地址

    def parse_item(self, response):
        ipItems = response.css('#ip_list tr:not(:first-child)')
        for tr in ipItems:
            item = {}
            ip = tr.css("td:nth-child(2)::text").extract_first()
            port = tr.css("td:nth-child(3)::text").extract_first()
            type = tr.css("td:nth-child(5)::text").extract_first()
            if type == "HTTP":
                item["http"] = "http://" + ip + ":" + port
            else:
                item["http"] = "https://" + ip + ":" + port
            try:
                # print(item)
                response = requests.get(url='http://www.win4000.com', headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'},
                                        proxies=item, timeout=1)
                if response.status_code == 200:
                    print(item)
                    yield item
            except:
                pass
