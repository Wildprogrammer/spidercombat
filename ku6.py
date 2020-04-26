import requests
import json

for page in range(2):
    print("正在抓取第{}页".format(page))
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    url = 'https://www.ku6.com/video/feed?pageNo={}&pageSize=40&subjectId=76'.format(page)
    respone = requests.get(url, headers=header)
    data = respone.text
    print(data)
    json_data = json.loads(data)
    print(json_data)
    data_list = json_data['data']
    # print(data_list)
    for data1 in data_list:
        video_title = data1['title'] + '.mp4'
        video_url = data1['playUrl']
        # print(video_title,video_url)
        video_data = requests.get(video_url, headers=header).content
        with open('video\ku6\\' + video_title, 'wb') as f:
            f.write(video_data)
            print("下载成功")
#
