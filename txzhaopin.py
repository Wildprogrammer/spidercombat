import requests
import json
import threading
from queue import Queue


class TxSpider():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
        self.url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1585833929692&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        start_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1585833929692&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn'
        start_response = requests.get(start_url, headers=self.headers).json()
        self.count = int((int(start_response["Data"]["Count"]) + 9) / 10) + 1
        self.post_list = []
        self.url_queue = Queue()
        self.html_queue = Queue()
        # self.content_queue=Queue()

    def get_url(self):
        for i in range(1, self.count):
            self.url_queue.put(self.url.format(i))
        # next_url_list=[self.url.format(i) for i in range(1,self.count+10)]
        # return  next_url_list

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            print(url)
            self.html_queue.put(response.json())
            self.url_queue.task_done()
            # return response.json()

    def save_data(self):
        while True:
            data = self.html_queue.get()
            temp_list = data["Data"]["Posts"]
            self.post_list.extend(temp_list)
            with open("tx.text", "w", encoding="utf-8") as f:
                f.write(json.dumps(self.post_list, ensure_ascii=False))
                f.write("\n")
            self.html_queue.task_done()

    def run(self):
        thread_list = []
        t_url = threading.Thread(target=self.get_url)
        thread_list.append(t_url)
        for i in range(3):
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)
        for i in range(2):
            t_save = threading.Thread(target=self.save_data)
            thread_list.append(t_save)
        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程，主线程结束，子线程结束
            t.start()
        for q in [self.url_queue, self.html_queue]:
            q.join()
        # url_list=self.get_url()
        # for url in url_list:
        #     data=self.parse_url(url)
        #     self.save_data(data)
        #


if __name__ == '__main__':
    tx = TxSpider()
    tx.run()

    # start_url='https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1585833929692&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn'
    # start_response=requests.get(start_url,headers=self.headers).json()
    # count=int(int(start_response["Data"]["Count"])/10)
