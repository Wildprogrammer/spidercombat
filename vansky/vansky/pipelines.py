# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
class VanskyPipeline(object):
    def process_item(self, item, spider):
        name=item['name']
        tel=item['tel']
        with open("van14.csv", 'a',encoding='GBK', newline='') as csvfile:
            csvfile = csv.writer(csvfile, delimiter=",")
            csvfile.writerow([name,tel])
        # return item
