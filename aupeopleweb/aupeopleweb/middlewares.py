# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from fake_useragent import UserAgent
import random
class RandomUserAgentMiddleware:
    def process_request(self, request, spider):
        ua=UserAgent()
        request.headers["User-Agent"]=ua.random
# class RandomProxyMiddleware:
#     def process_request(self, request, spider):
#         proxy = random.choice(spider.settings['PROXIES'])
#         request.meta['proxy'] = proxy
class CheckUserAgent:
    def process_response(self,request,response,spider):
        print(dir(response.request))
        print(request.headers["User-Agent"])
        # return 必须有，表示响应经过引擎交给爬虫
        return response

