import requests
import json

for page in range(1, 4):
    print("*****")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "cookie": "BAIDUID=B6E6B233AFAAAAF37765F3C974DC3950:FG=1; PSTM=1554283608; BIDUPSID=CD3B24AC2F7AF51AD4DA17CA02D7932F; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=1vY3JSVWRSVzdHY3A2bXJCYzlwMkVaMUJuakJvQWc2WFF1bk1tNDc0RGdDcFplSVFBQUFBJCQAAAAAAAAAAAEAAAAkecu4ZGRka2tybgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOB9bl7gfW5edG; H_PS_PSSID=30962_1460_31119_21108_30902_30823_31086; BCLID=8408990772980894651; BDSFRCVID=Ih-OJeC62CStsMcutGsT-bkat225W-JTH6aoFk1LqS0yJBeU7IrjEG0PDM8g0KubHvBtogKKKgOTHItF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJIJ_K02tCL3j5r6-tTfhnLtK2T22-usQmjl2hcH0KLKMh6nD4K55J09LN_L5tnKbg3d5R5TaMb1MRjvhbJlWKuwhU8tb47J0KjLaq5TtUJ8JKnTDMRh-6_ZQhQyKMniWKv9-pnYbpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuDju2j5v3DGtsbtQb26r-3--8-bTVHRDk5-Qo-4_eqxby26nA2Pj9aJ5nJDoTVPbRXtbh5M-y32caa-oJtJut-56FQpP-HJ7DMTQdKqJQ2t6GKlLfW6rBKl0MLpbYbb0xynoDybKY5MnMBMni52OnapT23fAKftnOM46JehL3346-35543bRTLnLy5KJYMDcnK4-Xj5Q-DHJP; delPer=0; PSINO=5; PC_TAB_LOG=haokan_website_page; Hm_lvt_4aadd610dfd2f5972f1efee2653a2bc5=1584620466; Hm_lpvt_4aadd610dfd2f5972f1efee2653a2bc5=1584620466; reptileData=%7B%22data%22%3A%22d56da725529795f05d2468c8a823ccf9c6aae1827a634ac56c58b9b5032b3bf0e4aa561a467b306f581191b16422c9877919d99cc2265f3150d6a0727958e1c1c25cc3ee4110ebf50b2debeeda9a21e0914977884f49b03361c0676a61e0f99135d7f74e417900d4b3f2ef298ade173c3bf1993081904bf5f23642fa3f569f0c%22%2C%22key_id%22%3A%2230%22%2C%22sign%22%3A%22f7dfd4a1%22%7D"
    }
    base_url = "https://haokan.baidu.com/videoui/api/videorec?tab=gaoxiao&act=pcFeed&pd=pc&num=20&shuaxin_id=1584621018800"

    response = requests.get(base_url, headers=headers)
    data = response.text

    json_data = json.loads(data)
    data_list = json_data['data']['response']['videos']

    for data1 in data_list:
        video_title = data1['title'] + '.mp4'
        video_url = data1['play_url']
        print(video_title, video_url)
        video_data = requests.get(video_url, headers=headers).content
        with open("video\\" + video_title, 'wb') as f:
            f.write(video_data)
