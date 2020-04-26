# import requests
# header= {
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
# url="https://tieba.baidu.com/f?kw={}".format("李毅")
# respone=requests.get(url,headers=header)
# print(respone.content.decode())
# from selenium import webdriver
# browser = webdriver.Chrome()
# browser.get("http://www.baidu.com")
# browser.close()

# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# #这个是一个用来控制chrome以无界面模式打开的浏览器
# #创建一个参数对象，用来控制chrome以无界面的方式打开
# chrome_options = Options()
# #后面的两个是固定写法 必须这么写
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
#
#
# #创建浏览器对象
#
# browser = webdriver.Chrome()
#
# url ='http://www.baidu.com/'
#
# browser.get(url)
# time.sleep(3)
# browser.save_screenshot('baid.png')
#
# browser.quit()

from pymongo import MongoClient
client=MongoClient(host="127.0.0.1",port=27017)
collection=client['test']['test10']
# collection.insert({"name":"xiaozhang","age":18})
# data=[{"name":"test{}".format(i)}  for i in range(10)]
# # collection.insert(data)
# a=collection.find({"name":"xiaozhang"})
# print(list(a))
data=[{"_id":i,"name":"py{}".format(i)} for i in range(1000)]
# print(data)
# collection.insert_many(data)
collection.find("")

