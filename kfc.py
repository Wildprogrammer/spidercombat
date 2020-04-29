import requests
import csv

for i in range(1, 23):#json数据有一个rowcount可控制自动获取页数
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
    data = {
        "cname": "杭州",
        "pageIndex": i,
        "pageSize": 10
    }
    response = requests.get(url, data)
    json_data = response.json()
    print(json_data)
    data_list = json_data['Table1']
    for li in data_list:
        print(li)
        cityName = li['cityName']
        storeName = li['storeName']
        addressDetail = li['addressDetail']
        pro = li['pro']
        print(cityName, storeName, addressDetail, pro)
        with open('肯德基门店.csv', 'a', encoding="utf-8", newline='') as csvfile:
            csvfile = csv.writer(csvfile, delimiter=",")
            csvfile.writerow([cityName, storeName, addressDetail, pro])
