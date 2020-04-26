import requests
from fake_useragent import UserAgent


class Tbspider():
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        ua = UserAgent()
        self.headers = {
            "User-Agent": ua.random}
        self.url_temp = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}"

    # 控制页数
    def get_url_list(self):
        return [self.url_temp.format(self.tieba_name, i * 50) for i in range(3)]

    # url获取
    def get_content(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    # 数据保存
    def save_data(self, text, page):
        file_path = "{}第{}页.html".format(self.tieba_name, page)
        print(file_path)
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(text)

    # 主逻辑
    def run(self):
        url_list = self.get_url_list()
        for url in url_list:
            text = self.get_content(url)
            page = url_list.index(url) + 1
            self.save_data(text, page)


if __name__ == '__main__':
    t1 = Tbspider("李毅")
    t1.run()
