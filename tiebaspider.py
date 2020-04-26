import requests
from lxml import etree
import json
import re


class TiebaSpider():
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        self.url_temp = "https://tieba.baidu.com/f?kw=" + tieba_name + "&pn=0"
        self.second_url = 'https://tieba.baidu.com'

    def parse_url(self, url):  # 发送请求，获取数据
        response = requests.get(url, headers=self.headers)
        html_str = response.text
        return html_str

    def get_data(self, html_temp):
        html = etree.HTML(html_temp)
        # li_list=html.xpath("//*[@id='thread_list']/li")
        page_url_list = html.xpath('//*[@id="thread_list"]/li//div[@class="threadlist_lz clearfix"]/div[1]')
        # second_url='https://tieba.baidu.com'
        content_list = []
        picture_list = []
        for page_url in page_url_list:
            item = {}
            # item["title"]=li.xpath(".//div[@class='threadlist_lz clearfix']/div[1]/a/@href")
            item["title"] = page_url.xpath('./a/text()')[0] if len(page_url.xpath('./a/text()')) > 0 else None
            item["href"] = self.second_url + page_url.xpath('./a/@href')[0] if len(
                page_url.xpath('./a/@href')) > 0 else None
            item["img_list"] = self.get_image(item["href"], [])
            picture_list.extend(item["img_list"])
            content_list.append(item)
            print(picture_list)
        next_url = html.xpath('//a[text()="下一页"]/@href')[0] if len(html.xpath('//a[text()="下一页"]/@href')) > 0 else None
        print(next_url)
        return content_list, next_url, picture_list

    def get_image(self, detail_url, total):
        detail_url_str = self.parse_url(detail_url)
        detail_html = etree.HTML(detail_url_str)
        image_list = detail_html.xpath("//cc//img/@src")
        total.extend(image_list)
        detail_temp_url = detail_html.xpath('//a[text()="下一页"]/@href')
        if len(detail_html.xpath('//a[text()="下一页"]/@href')) > 0:
            detail_next_url = self.second_url + detail_temp_url[0]
            return self.get_image(detail_next_url, total)
        return total

    def sava_picture(self, picture):
        for picture_data in picture:
            pic_data = requests.get(picture_data, headers=self.headers).content
            file_path = picture_data.split('/')[-1]
            try:
                with open("image\\" + file_path, 'wb') as f:
                    f.write(pic_data)
            except:
                pass

    def run(self):
        # 发送请求，获取数据
        next_url = self.url_temp
        while next_url is not None:
            # 提取数据，获取字段
            html_temp = self.parse_url(next_url)
            content_list, next_url, picture = self.get_data(html_temp)
            # 保存数据
            self.sava_picture(picture)


if __name__ == '__main__':
    a = TiebaSpider("python")
    a.run()

