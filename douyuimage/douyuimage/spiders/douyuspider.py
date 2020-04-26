# -*- coding: utf-8 -*-
import scrapy
import json
from douyuimage.items import DouyuimageItem


class DouyuspiderSpider(scrapy.Spider):
    name = 'douyuspider'
    allowed_domains = ['douyu.com']
    base_url='http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    offset=0
    start_urls = [base_url+str(offset)]

    def parse(self, response):
        data_list=json.loads(response.body)['data']
        if len(data_list)==0:
            return
        for data in data_list:
            item=DouyuimageItem()
            item['anchor_name']=data['nickname']
            item['anchor_img']=data['vertical_src']
            yield item
        self.offset+=20
        url=self.base_url+str(self.offset)
        yield scrapy.Request(
                url,
                callback=self.parse,
                dont_filter=True
        )

