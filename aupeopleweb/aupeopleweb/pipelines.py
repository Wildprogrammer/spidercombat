# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import re
class AupeoplewebPipeline(object):
    def process_item(self, item, spider):
        name = item['name']
        tel = item['tel']
        area= item['area']
        tel=re.findall('\d+',str(tel))[0]
        if tel[0:2]=='04' or tel[0:1]=='4':
            if len(tel)==10:
                print(tel)
                with open("au3.csv", 'a',  newline='') as csvfile:
                    csvfile = csv.writer(csvfile, delimiter=",")
                    csvfile.writerow([name, tel, area])