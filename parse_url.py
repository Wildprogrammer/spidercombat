import requests
from retrying import retry

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36"}


@retry(stop_max_attempt_number=3)
def _parse_url(url):
    response = requests.get(url, headers=headers, timeout=3)
    assert response.status_code == 200
    return response.content.decode("utf-8")


def parse_url(url):
    try:
        html_str = _parse_url(url)
        # print(html_str)
    except:
        html_str = None
    return html_str
