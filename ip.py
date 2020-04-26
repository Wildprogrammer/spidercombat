import requests
import parsel
import time
import json
from pymongo import MongoClient


class IpSpider():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        self.url = 'https://www.kuaidaili.com/free/inha/{}/'
        self.correct_ip=[]
        # client=MongoClient()
        # self.collection=client["ip"]["kuaidaili"]

    def get_url(self):
        return [self.url.format(i) for i in range(501,600)]


    def get_content(self,url):
        response = requests.get(url, headers=self.headers)
        time.sleep(1)
        html = parsel.Selector(response.content.decode())
        tr_list = html.xpath('//table[@class="table table-bordered table-striped"]//tbody/tr')
        print(len(tr_list))
        ip_list=[]
        for tr in tr_list:
                item = {}
                type = tr.xpath('./td[4]/text()').extract_first()
                ip = tr.xpath('./td[1]/text()').extract_first()
                port = tr.xpath('./td[2]/text()').extract_first()
                # item["num"]=0
                if type=="HTTP":
                    item["http"]="http://"+ip+":"+port
                else:
                    item["http"]="https://"+ip+":"+port
                ip_list.append(item)
        return ip_list

    def save_data(self,data_list):
        for proxy in data_list:
            try:
                print(proxy)
                response = requests.get(url='http://www.chinaedu.edu.cn/', headers=self.headers, proxies=proxy, timeout=1)
                if response.status_code == 200:
                    # proxy["num"]=0
                    self.correct_ip.append(proxy)
            except:
                pass

    # def save_data(self, data):
    #     self.collection.insert(dict(data))

    def run(self):
        url_list=self.get_url()
        for url in url_list:
            data_list=self.get_content(url)
            self.save_data(data_list)
        with open("代理ip.txt", 'a') as f:
            f.write(json.dumps(self.correct_ip))

if __name__ == '__main__':
    i=IpSpider()
    i.run()
