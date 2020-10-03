import json
import os
import re
from pprint import pprint

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'cookie': 'kg_mid=fa123fe2c3e1ef211f8f36f8c9939e55; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1600565207; kg_dfid=2B4WfR1KbldX0sulfx0ayWXT; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1600565822'
}
def get_hash():
    hash_re = re.compile('"Hash":"(.*?)"',re.I|re.S)
    hash_url = 'https://www.kugou.com/yy/html/rank.html'
    hash_html = requests.get(url=hash_url,headers=headers)
    hash_music = hash_re.findall(hash_html.text)
    # print(hash_music)
    return hash_music


def down_music(title,content):
    if not os.path.exists('kg'):
        os.mkdir('kg')

    with open(f'kg/{title}.mp3', 'wb') as f:
        f.write(content)
        print(f'正在下载音乐。。。{title}')

def parse_music(hash_music):
    base_url = "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash="
    for hash in hash_music:
        url = base_url + hash
        response = requests.request("GET", url, headers=headers).json()
        # start = response.text.find('{"status":1')
        # end = response.text.find('mp3"}}') + len('mp3"}}')
        # json_data = json.loads(response.text[start:end], strict=False)
        songurl = response['data']['play_url']
        title = response['data']['song_name']
        down_music(title, requests.get(songurl).content)
        # print(songurl,title)


if __name__ == '__main__':
    hash_music = get_hash()
    parse_music(hash_music)


# str = '1 1 234 134 '
# def split(a):
#     return a.split('1')
#
# print(split(str))
#
# def func(ls=[]):
#     print('id(ls):',id(ls))
#     ls.append(1)
#     print('ls', ls)
#     return ls
#
# a= func()
# print(id(a))
# print(a)
# c =func()
# print(id(c))
# print(c)


