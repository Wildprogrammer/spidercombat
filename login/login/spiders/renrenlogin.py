# -*- coding: utf-8 -*-
import scrapy
import re


class RenrenloginSpider(scrapy.Spider):
    name = 'renrenlogin'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/SysHome.do']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

    def parse(self, response):
        # form_url='http://www.renren.com/PLogin.do'#action地址
        yield scrapy.FormRequest.from_response(response,
                                               formdata={"email": "15281764859", "password": "123456789"},
                                               headers=self.headers,
                                               formid="loginForm",
                                               callback=self.get_data,
                                               )

    def get_data(self, response):
        print(re.findall("野生程序猿", response.body.decode()))