from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # expected_conditions类提供预制条件判断的方法
from selenium.webdriver.support.wait import WebDriverWait


class DouyuSpider():
    def __init__(self):
        self.driver = webdriver.Firefox()

    def get_data(self):
        # self.driver.get(url)
        live_list = self.driver.find_elements_by_xpath(
            '//div[@class="layout-Module-container layout-Cover ListContent"]/ul[@class="layout-Cover-list"]/li')
        data_dict = []
        for live in live_list:
            item = {}
            item["image_url"] = live.find_element_by_xpath(
                './/div[@class="DyListCover-imgWrap"]/div/img').get_attribute("src")
            item["room_title"] = live.find_element_by_xpath('.//div[@class="DyListCover-info"]/h3').get_attribute(
                "title")
            item["room_cate"] = live.find_element_by_xpath('.//div[@class="DyListCover-info"]/span').text
            item["watch_num"] = live.find_element_by_xpath('.//span[@class="DyListCover-hot"]').text
            item["anchor_name"] = live.find_element_by_xpath('.//h2[@class="DyListCover-user"]').text
            data_dict.append(item)
        temp = self.driver.find_element_by_xpath('//ul[@class="dy-Pagination ListPagination"]/li[9]').get_attribute(
            'aria-disabled')
        # print(temp)
        if temp != "ture":
            next_url = self.driver.find_elements_by_xpath('//span[@class="dy-Pagination-item-custom"]')
            next_url = next_url[1]
        else:
            next_url = None
        return data_dict, next_url

    def save_data(self, data_dict):
        pass

    def run(self):
        # 开始提供，提供start_url
        start_url = 'https://www.douyu.com/directory/all'
        self.driver.get(start_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="DyListCover-imgWrap"]/div/img')))
        data_dict, next_url = self.get_data()
        print(data_dict)
        self.save_data(data_dict)
        # 循环:
        while next_url is not None:
            next_url.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="DyListCover-imgWrap"]/div/img')))
            # 访问网站，提取数据，转换为字典格式,同时提取下一页地址,此处采用显式等待，效率更高找到指定元素就执行
            data_dict, next_url = self.get_data()
            print(data_dict)
            # 保存数据，存到文件
            self.save_data(data_dict)
        self.driver.quit()


if __name__ == '__main__':
    d = DouyuSpider()
    d.run()
#
