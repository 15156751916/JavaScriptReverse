import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'cookie': ''
}
url = "https://xueqiu.com/"
req = requests.get(url, headers=headers)
cookies = requests.utils.dict_from_cookiejar(req.cookies)  # 转成字典格式
cookie = "; ".join([str(x)+"="+str(y) for x,y in cookies.items()])  # 将dict格式的拼接成可以放到请求头中的字符串格式
print(cookie)