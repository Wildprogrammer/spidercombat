# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import re
from fake_useragent import UserAgent
class MeizhuowangPipeline(object):
    def process_item(self, item, spider):
        # for i in item["img_list"]:
                i=item["image"]
                # print(i)
                response=requests.get(i,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'})
                filename=i.split("/")[-1]
                print(filename)
                with open("image\\"+filename, mode='wb') as f:
                    f.write(response.content)
        # print(item["img_list"])
        # return item
