import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests


def downloadfile(filename, content):
    with open(filename, 'w', encoding='utf8') as f:
        f.write(content)

def parse_video():
    re_m3u8 = re.compile('now="(.*?)"', re.I|re.S)
    re_main = re.compile('main = "(.*?)"', re.I|re.S)
    # html = requests.get('http://www.332dy.com/dili/38977.html')   ##  更换目标视频的url
    html = requests.get('http://www.332dy.com/dili/53296.html')   ##  更换目标视频的url
    soup = BeautifulSoup(html.text, 'lxml')
    lis = soup.select('ul.stui-content__playlist.sort-list.column8.clearfix li a')
    base = 'http://www.332dy.com/'
    for li in lis:
        print('li["href"]:', li['href'])
        innerUrl = urljoin(base, li['href'])
        print('innerUrl:', innerUrl)
        detail_html = requests.get(innerUrl)
        m3u8Result = re_m3u8.findall(detail_html.text)[0]
        if m3u8Result == []:
            base = 'http://www.332dy.com/'
            innerUrl = urljoin(base, li['href'])
            detail_html = requests.get(innerUrl)
            m3u8Result = re_m3u8.findall(detail_html.text)[0]
        video_html = requests.get(m3u8Result)   #
        mainResult = re_main.findall(video_html.text)[0]
        base = 'https://you-ku.qingyu-zuida.com/'
        m3u8Url = urljoin(base, mainResult)
        print('m3u8Url:', m3u8Url)
        downloadfile('m3u81.txt', requests.get(m3u8Url).text)

        print('----------------m3u81 保存完毕--------------')

        with open('m3u81.txt', 'r', encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("#"):
                    continue
                base = 'https://you-ku.qingyu-zuida.com/20200406/21853_bd33844a/'
                url = urljoin(base, line)
                break
        print('获取到最终url:', url)

        downloadfile('m3u82.txt', requests.get(url).text)

        print("---------------m3u82保存完毕---------------")

        with open('m3u82.txt', 'r', encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("#"):
                    continue
                print(line)
                base = 'https://you-ku.qingyu-zuida.com/20200406/21853_bd33844a/1000k/hls/'
                url = urljoin(base, line).replace('\n', '')
                print(url)
                with open('demo.mp4', 'ab') as f:
                    f.write(requests.get(url).content)



if __name__ == '__main__':
    parse_video()








































































