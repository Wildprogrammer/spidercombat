import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
url_temp = "https://www.vmgirls.com/13344/page-{}.html"
num = 1


def run(url):
    respone = requests.get(url, headers=headers)
    result = re.findall('<a href="(.*?)" alt="少女情怀总是诗" title="少女情怀总是诗">', respone.text)
    print(result)
    for r in result:
        name = r.split("/")[-1]
        print(name)
        respone_image = requests.get(r, headers=headers)
        with open("image\\" + name, mode='wb') as f:
            f.write(respone_image.content)


while num < 8:
    url = url_temp.format(num)
    run(url)
    num += 1
