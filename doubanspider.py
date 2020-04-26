import json
from parse_url import parse_url


class DouBanSpider():
    def __init__(self):
        self.url_temp = ["https://movie.douban.com/j/search_subjects?type=tv&tag=热门&page_limit=20&page_start={}",
                         "https://movie.douban.com/j/search_subjects?type=tv&tag=美剧&page_limit=20&page_start={}",
                         "https://movie.douban.com/j/search_subjects?type=tv&tag=英剧&page_limit=20&page_start={}"]

    # 字符串转JSON
    def get_json_str(self, html_str):
        json_str = json.loads(html_str)
        return json_str

    # 写进文件
    def save_file(self, ret):
        with open("douban.text", "a", encoding="utf-8") as f:
            f.write(json.dumps(ret, ensure_ascii=False))
            f.write("\n")

    def run(self):  # 实现主逻辑
        i = 0
        for url1 in self.url_temp:
            num = 0
            total = 60
            i += 1
            print(i)
            while num < total:
                url = url1.format(num)
                # print(url)
                html_str = parse_url(url)
                # print(html_str)
                ret = self.get_json_str(html_str)
                self.save_file(ret)
                num += 20


if __name__ == '__main__':
    a = DouBanSpider()
    a.run()
