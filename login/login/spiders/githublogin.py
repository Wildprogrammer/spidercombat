# -*- coding: utf-8 -*-
import scrapy
import re
'''遵守robots无数据,需要设置下'''

class GithubloginSpider(scrapy.Spider):
    name = 'githublogin'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    # print(str(int(time.time() * 1000)))  # 时间戳
    def parse(self, response):
#方法二:
        authenticity_token=response.xpath('//input[@name="authenticity_token"]/@value').extract_first()
        timestamp=response.xpath('//input[@name="timestamp"]/@value').extract_first()
        timestamp_secret=response.xpath('//input[@name="timestamp_secret"]/@value').extract_first()
        print(timestamp,timestamp_secret)
        yield scrapy.FormRequest('https://github.com/session',
                                 headers=self.headers,
                                 formdata={
                                    'commit': 'Sign in',
                                    'authenticity_token':authenticity_token,
                                    'login': '',#你的账号
                                    'password': '',#你的密码
                                    'timestamp': timestamp,
                                    'timestamp_secret': timestamp_secret

                                 },
                                 callback=self.get_data
                                 )

# # 方法二:
#         yield scrapy.FormRequest.from_response(response,
#                                                formdata={'login':'','password':''},#账号和密码
#                                                headers=self.headers,
#                                                formxpath='//*[@id="login"]/form',
#                                                callback=self.get_data,)


    def get_data(self,response):
        # print(re.findall('python',response.body.decode()))
        print(response.body.decode())