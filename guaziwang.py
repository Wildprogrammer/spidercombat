import requests
import parsel
import threading
from queue import Queue


class GuaziSpider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Cookie": "antipas=00l496320119129575vi2431; uuid=eb2aa1fa-7eb0-4367-e821-b3826e30ba54; cityDomain=shaoxing; clueSourceCode=%2A%2300; user_city_id=31; ganji_uuid=9529352347384775786996; sessionid=aba5414e-c0a2-4900-d612-8784a0991e92; lg=1; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1586867445; gr_user_id=997db2f0-eafa-416d-81bb-d4a00f3fe938; gr_session_id_bf5e6f1c1bf9a992=011bdc2c-ba74-4aaa-b7e0-7dcce394bb6b; gr_session_id_bf5e6f1c1bf9a992_011bdc2c-ba74-4aaa-b7e0-7dcce394bb6b=true; close_finance_popup=2020-04-14; lng_lat=120.53949_30.03312; gps_type=1; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22eb2aa1fa-7eb0-4367-e821-b3826e30ba54%22%2C%22ca_city%22%3A%22shaoxing%22%2C%22sessionid%22%3A%22aba5414e-c0a2-4900-d612-8784a0991e92%22%7D; preTime=%7B%22last%22%3A1586867437%2C%22this%22%3A1586867421%2C%22pre%22%3A1586867421%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1586867460"}
        self.next_queue = Queue()
        self.detail_queue = Queue()
        self.content_queue = Queue()

    def get_next_url(self):  # 获得翻页url
        temp_url = 'https://www.guazi.com/shaoxing/buy/o{}h2/'
        for i in range(1, 51):
            self.next_queue.put(temp_url.format(i))
            print(temp_url.format(i))
        # return [temp_url.format(i) for i in range(1, 3)]

    def get_detail_list(self):  # 发送请求
        while True:
            url = self.next_queue.get()
            response = requests.get(url, headers=self.headers).content.decode()
            html = parsel.Selector(response)
            li_list = html.xpath('//ul[@class="carlist clearfix js-top"]/li')
            # url_list = []
            for li in li_list:
                detail_url = "https://www.guazi.com" + li.xpath('./a/@href').extract_first()
                # url_list.append(detail_url)
                self.detail_queue.put(detail_url)
            self.next_queue.task_done()
            # return url_list

    def get_content(self):  # 通过详情链接访问详情地址
        while True:
            i = self.detail_queue.get()
            response = requests.get(i, headers=self.headers).content.decode()
            html = parsel.Selector(response)
            item = {}
            item["title"] = html.xpath('//h2[@class="titlebox"]/text()').extract_first()
            item["title"] = item["title"].strip() if item["title"] != None else None
            item["cardtime"] = \
                html.xpath(
                    '//div[@class="basic-infor js-basic-infor js-top"]//ul/li[@class="one"]/div/text()').extract_first()
            item["km"] = \
                html.xpath(
                    '//div[@class="basic-infor js-basic-infor js-top"]//ul/li[@class="two"]/div/text()').extract_first()
            item["mode"] = \
                html.xpath(
                    '//div[@class="basic-infor js-basic-infor js-top"]//ul/li[@class="five"]/div/text()').extract_first()
            item["displacement"] = \
                html.xpath(
                    '//div[@class="basic-infor js-basic-infor js-top"]//ul/li[@class="six"]/div/text()').extract_first()
            item["num"] = \
                html.xpath(
                    '//div[@class="basic-infor js-basic-infor js-top"]//ul/li[@class="seven"]/div/text()').extract_first()
            item["num"] = item["num"].strip() if item["num"] != None else None
            print(item)
            # yield item
            self.content_queue.put(item)
            self.detail_queue.task_done()

    def save_data(self):
        while True:
            with open("guazi.csv", 'a', encoding="utf-8") as f:
                f.write(str(self.content_queue.get()))
                f.write(",")
                f.write("\n")
                self.content_queue.task_done()
                # print(i)

    def run(self):  # 主逻辑实现
        thread_list = []
        t_url = threading.Thread(target=self.get_next_url)  # 放到翻页队列
        thread_list.append(t_url)
        for i in range(1):
            t_detail_url = threading.Thread(target=self.get_detail_list)  # 放到详情队列
            thread_list.append(t_detail_url)
        for i in range(3):
            t_content = threading.Thread(target=self.get_content)  # 放到内容队列
            thread_list.append(t_content)
        for i in range(2):
            t_save = threading.Thread(target=self.save_data)
            thread_list.append(t_save)
        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程，主线程结束，子线程结束
            t.start()
        for q in [self.next_queue, self.detail_queue, self.content_queue]:
            q.join()
        # url_list=se

        # url_list = self.get_detail_list(url)
        # data = self.get_content(url_list)
        # with open("guazi.csv", 'a', encoding="utf-8") as f:
        #     for i in data:
        #         f.write(str(i))
        #         f.write(",")
        #         f.write("\n")
        #         print(i)


if __name__ == '__main__':
    g = GuaziSpider()
    g.run()
