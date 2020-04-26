# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from pymongo import MongoClient


client = MongoClient()
collection =client["yangguang"]["zw"]

class YangguangPipeline(object):
    def process_item(self, item, spider):
        item['content']=self.process_content(item['content'])
        item['state']=self.process_content(item['state'])
        # self.mongo(item)
        collection.insert(dict(item))
        print(item)
        return item
    def process_content(self,data):
        # da=data.strip()
        da=re.sub(r"\s","",data)
        return da
    # def mongo(self,item):
    #     client = MongoClient()
    #     collection =client["yangguang"]["zw"]
    #     collection.insert(item)