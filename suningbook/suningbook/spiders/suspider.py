# -*- coding: utf-8 -*-
import scrapy
# from suningbook.items import SuningbookItem
import re
from copy import deepcopy


class SuspiderSpider(scrapy.Spider):
    name = 'suspider'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com']

    def parse(self, response):
        list_a = response.xpath('//div[@class="menu-sub"]//li')
        for div in list_a:
            item = {}
            item["kind"] = div.xpath("./a/text()").extract_first()
            item["page_url"] = div.xpath('./a/@href').extract_first()
            # print(item)
            yield scrapy.Request(
                item["page_url"],
                callback=self.parse_page,
                meta={"item": deepcopy(item)}
            )

    def parse_page(self, response):
        item = response.meta["item"]
        list_b = response.xpath('//div[@id="filter-results"]/ul[@class="clearfix"]/li')
        for li in list_b:
            item["detail_url"] = 'https:' + li.xpath('.//p[@class="sell-point"]/a/@href').extract_first()
            # print(item)
            yield scrapy.Request(
                item["detail_url"],
                callback=self.parse_detail,
                meta={"item": deepcopy(item)}
            )
        # next_url="https://list.suning.com"+response.xpath('//a[@id="nextPage"]/@href').extract_first()
        # print(response.xpath('//a[@id="nextPage"]/@href').extract_first())
        # if next_url is not None:
        #     yield scrapy.Request(
        #         next_url,
        #         callback=self.parse_page,
        #         meta={"item":item}#parse_page函数重新调用需要用到item，不传会找不到报错，不过我这种传法会多一个参数，不过没关系有新数据换掉，如果新数据没传进来就还是老数据
        #     )
        # 翻页法二:
        # page_current=int(re.findall(r'"currentPage":"(.*?)"',response.text)[0])+1
        # page_num = int(re.findall(r'"pageNumbers":"(.*?)"', response.text)[0])
        page_current = int(re.findall(r'param\.currentPage = "(.*?)";', response.text)[0]) + 1
        page_num = int(re.findall(r'param\.pageNumbers = "(.*?)";', response.text)[0])
        try:
            if page_current == 1:
                num = re.findall(r'<link rel="canonical" href="//list\.suning.com/(.*?)-0.html">', response.text)[0]
            else:
                num = response.meta["num"]
            # param.currentPage = "(.*?)";
            # param.pageNumbers = "(.*?)";
            # print(page_current,page_num,num)
            if page_current < page_num:
                next_url = "https://list.suning.com/{}-{}.html".format(num, page_current)
                # print(item)
                item["page_url"] = next_url
            # print(item)
            # print(next_url)
            # print("正在抓取第{}页".format(page_current))
            yield scrapy.Request(
                next_url,
                callback=self.parse_page,
                meta={"item": deepcopy(item), "num": num}
            )
        except:
            pass

    def parse_detail(self, response):
        item = response.meta["item"]
        item["title"] = response.xpath("//head/title/text()").extract_first()
        item["author"] = re.sub(r"\s", "", response.xpath('//li[@class="pb-item"][1]/text()').extract_first()) if len(
            response.xpath('//li[@class="pb-item"][1]/text()')) > 0 else None
        # item["publish"] = re.sub(r"\s","",response.xpath('//li[@class="pb-item"][2]/text()').extract_first())
        item["publish"] = re.findall('<li>出版社：(.*?)</li>', response.text)[0] if len(
            re.findall('<li>出版社：(.*?)</li>', response.text)) > 0 else None
        # item["publish_time"]=str(response.xpath('//li[@class="pb-item"][3]/span[2]/text()').extract_first())
        item["publish_time"] = re.findall('<li>出版时间：(.*?)</li>', response.text)[0] if len(
            re.findall('<li>出版时间：(.*?)</li>', response.text)) > 0 else None
        # item["price"]=re.findall('<em id="qg_promotionPrice">(.*?)</em>',response.text)[0]
        # print(item)
        yield item
