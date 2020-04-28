import requests
import time
from fake_useragent import UserAgent
import csv


class LagouSpider():
    def __init__(self):
        self.url = "https://www.lagou.com/jobs/positionAjax.json?px=default&city=杭州"
        ua = UserAgent()
        self.headers = {
            "origin": "www.lagou.com",
            "referer": "https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE/p-city_6?px=default",
            "sec - fetch - dest": "empty",
            "sec - fetch - mode": "cors",
            "sec - fetch - site": "same - origin",
            "User-Agent": ua.random}

    def get_next_data(self, i):
        form = {
            "first": "false",
            "pn": i,
            "kd": "数据",
        }
        return form

    def get_content(self, session, form):
        response = session.get(self.url, headers=self.headers, data=form).json()
        print(response)
        showid = response['content']['showId']
        return response, showid

    def sava_data(self, result):

        contents = result["content"]["positionResult"]["result"]
        for content in contents:
            city = content['city']  # 城市
            jobname = content['positionName']  # 职位名称
            companyname = content['companyFullName']  # 公司名称
            industry = content['industryField']  # 所属领域
            workyear = content['workYear']  # 工作经验
            education = content['education']  # 学历
            salary = content['salary']  # 薪资
            lastLogin = content['lastLogin']  # 最后发布时间
            # shortname = content['companyShortName']  # 公司简称
            # companysize = content['companySize']  # 公司规模
            # financestage = content['financeStage']  # 融资阶段
            # advantage = content['positionAdvantage']  # 职位福利
            # skillLables = content['skillLables']
            # if skillLables == []:
            #     skillLables = "无要求！"
            print(city, jobname, companyname, industry, workyear, education, salary, lastLogin, sep='|')
            with open("lagou.csv", 'a', encoding="utf-8", newline='') as filecsv:
                csvwriter = csv.writer(filecsv, delimiter=",")
                csvwriter.writerow([city, jobname, companyname, industry, workyear, education, salary, lastLogin])

    def run(self):
        session = requests.session()
        session.get(
            'https://www.lagou.com/jobs/list_数据/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput=',
            headers=self.headers)
        initial_form = self.get_next_data(1)
        initial_resopnse, showid = self.get_content(session, initial_form)
        self.sava_data(initial_resopnse)
        # time.sleep(3)
        for i in range(2, 31):
            data = self.get_next_data(i)
            data['sid'] = showid  # 不加这个字段，速度太快会反爬
            # print(data)
            response, showid = self.get_content(session, data)
            self.sava_data(response)
            time.sleep(2)


if __name__ == '__main__':
    lg = LagouSpider()
    lg.run()
