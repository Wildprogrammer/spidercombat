import requests
import pandas as pd
from urllib.parse import urlencode

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
data = []
for i in range(1, 3):
    paras = {
        'reportTime': '2019-12-31',
        'pageNum': i
    }
    url = "https://s.askci.com/stock/a/0-0?" + urlencode(paras)
    # print(url)
    response = requests.get(url, headers=headers).text
    tb = pd.read_html(response, header=0)[3]
    data.append(tb)
    print(tb)
df = pd.concat(data)
df.to_csv("zhongshang.csv")
#
