from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC #expected_conditions类提供预制条件判断的方法
from selenium.webdriver.support.wait import WebDriverWait
import time
import csv
import re

'''
方法	说明
title_is	判断当前页面的 title 是否完全等于（==）预期字符串，返回布尔值
title_contains	判断当前页面的 title 是否包含预期字符串，返回布尔值
presence_of_element_located	判断某个元素是否被加到了 dom 树里，并不代表该元素一定可见
visibility_of_element_located	判断某个元素是否可见. 可见代表元素非隐藏，并且元素的宽和高都不等于 0
visibility_of	跟上面的方法做一样的事情，只是上面的方法要传入 locator，这个方法直接传定位到的 element 就好了
presence_of_all_elements_located	判断是否至少有 1 个元素存在于 dom 树中。举个例子，如果页面上有 n 个元素的 class 都是'column-md-3'，那么只要有 1 个元素存在，这个方法就返回 True
text_to_be_present_in_element	判断某个元素中的 text 是否 包含 了预期的字符串
text_to_be_present_in_element_value	判断某个元素中的 value 属性是否包含 了预期的字符串
frame_to_be_available_and_switch_to_it	判断该 frame 是否可以 switch进去，如果可以的话，返回 True 并且 switch 进去，否则返回 False
invisibility_of_element_located	判断某个元素中是否不存在于dom树或不可见
element_to_be_clickable	判断某个元素中是否可见并且是 enable 的，这样的话才叫 clickable
staleness_of	等某个元素从 dom 树中移除，注意，这个方法也是返回 True或 False
element_to_be_selected	判断某个元素是否被选中了,一般用在下拉列表
element_selection_state_to_be	判断某个元素的选中状态是否符合预期
element_located_selection_state_to_be	跟上面的方法作用一样，只是上面的方法传入定位到的 element，而这个方法传入 locator
alert_is_present	判断页面上是否存在 alert
'''
class TaobaoSpider():
    def __init__(self):
        self.keyword = input('请输入要搜索商品:')
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)#隐式等待，需要页面加载完
    def search_product(self):
        self.driver.find_element_by_id('q').send_keys(self.keyword)
        self.driver.find_element_by_class_name('btn-search').click()
        self.driver.maximize_window()
        time.sleep(10)

    def get_page(self):
        try:
            page = self.driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[1]').text
            page = int(re.findall('(\d+)', page)[0])
        except:
            page=1
        return page
    def get_message(self):
        div_list= self.driver.find_elements_by_xpath('//div[@class="items"]/div[@class="item J_MouserOnverReq item-ad  "]')\
                  +self.driver.find_elements_by_xpath('//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
        for div in div_list:
            info = div.find_element_by_xpath('.//div[@class="row row-2 title"]/a').text
            price = div.find_element_by_xpath('.//strong').text + "元"
            deal = div.find_element_by_xpath('.//div[@class="deal-cnt"]').text
            name = div.find_element_by_xpath('.//div[@class="shop"]/a').text
            print(info, price, deal, name, sep='|')
            with open("data.csv", 'a', encoding="utf-8", newline='') as filecsv:
                csvwriter = csv.writer(filecsv, delimiter=",")
                csvwriter.writerow([info, price, deal, name])

    def run(self):
        self.driver.get('https://www.taobao.com')
        self.search_product()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "mainsrp-itemlist")))
        page=self.get_page()
        self.get_message()
        page_num = 1
        while page_num != page:
            self.driver.get('https://s.taobao.com/search?q={}&s={}'.format(self.keyword, page_num * 44))
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "mainsrp-itemlist")))
            self.get_message()
            page_num += 1
        self.driver.quit()

if __name__ == '__main__':
    tb=TaobaoSpider()
    tb.run()
