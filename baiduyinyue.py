import requests
import re


class MusicSpider():
    def __init__(self):
        self.song_url = "http://play.taihe.com/data/music/songlink"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
        self.page_url = 'http://music.taihe.com/data/user/getsongs?start={}&size=15&ting_uid=2517'

    def get_page_music_list(self, last_url):
        html = requests.get(last_url, headers=self.headers).json()['data']['html']
        song_list = re.findall('href="/song/(.*?)"', html)
        print(song_list)
        print(len(song_list))
        return song_list
        # for page_song in song_list:
        #     self.get_one_music(page_song)

    def get_one_music(self, song_id):
        data = 'songIds=' + str(
            song_id) + '&hq=0&type=m4a%2Cmp3&rate=&pt=0&flag=-1&s2p=-1&prerate=-1&bwt=-1&dur=-1&bat=-1&bp=-1&pos=-1&auto=-1'
        response = requests.post(self.song_url, headers=self.headers, data=data).json()
        song_name = response['data']['songList'][0]['songName']
        song_temp = response['data']['songList'][0]['songLink']
        print(song_name)
        try:
            song_response = requests.get(song_temp, headers=self.headers)
            with open("music\\" + song_name + ".mp3", 'wb') as  f:
                f.write(song_response.content)
        except:
            print("版权问题，无法下载")

    def run(self):
        for num in range(9):
            last_url = self.page_url.format(15 * num)
            print(last_url)
            song_list = self.get_page_music_list(last_url)
            for song_id in song_list:
                self.get_one_music(song_id)
            pass


if __name__ == '__main__':
    r = MusicSpider()
    r.run()
