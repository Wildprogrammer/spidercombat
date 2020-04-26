# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
from scrapy.pipelines.images import ImagesPipeline

class DouyuimagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_link=item['anchor_img']
        print(image_link)
        yield  scrapy.Request(image_link)

    def item_completed(self, results, item, info):
        path="C:/Users/Administrator/Desktop/douyu/"
        if results[0][0]==True:
            os.rename(path+results[0][1]['path'],path+str(item['anchor_name']+".jpg"))
        return item