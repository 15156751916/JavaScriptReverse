import requests
import execjs
import re
from fake_useragent import UserAgent

def hongshuspider(url):
    ua = UserAgent()
    headers = {"User-Agent":ua.random}
    response = requests.get(url=url, headers=headers).text
    js_code = 'function run(){'
    js_code += re.findall(r"(var CryptoJS=CryptoJS[\s\S]*?)</script>", response)[0]
    js_code += 'return words;}'
    ctx = execjs.compile(js_code)
    res = ctx.call('run')
    print(res)

if __name__ == '__main__':
    hongshuspider(url = 'https://m.hongshu.com/content/93416/13877912.html')