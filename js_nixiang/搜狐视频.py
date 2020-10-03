import requests

url = "https://v4.passport.sohu.com/i/login/107405"

data = {
'userid':'15156751628',
'password':'1f9a42d485170fbfab29376a49ebe06f',
'persistentCookie':'1',
'appid':'107405',
'callback':'passport403_cb1599690960698',
}
payload = 'userid=15156751628&password=1f9a42d485170fbfab29376a49ebe06f&persistentCookie=1&appid=107405&callback=passport403_cb1599690960707'
headers = {
  'authority': 'v4.passport.sohu.com',
  'pragma': 'no-cache',
  'cache-control': 'no-cache',
  'upgrade-insecure-requests': '1',
  'origin': 'https://tv.sohu.com',
  'content-type': 'application/x-www-form-urlencoded',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'sec-fetch-site': 'same-site',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-user': '?1',
  'sec-fetch-dest': 'iframe',
  'referer': 'https://tv.sohu.com/',
  'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'cookie': 't=1599690960690; IPLOC=CN3400; SUV=2009100636022Z7N; reqtype=pc; gidinf=x099980109ee12181d7cf20120000ea7cff238e10582; lastpassport=15156751628; jv=4c417bb9a974790b1e28990ea4fb9a42-c4s3qUe11599693789116'
}

response = requests.request("POST", url, headers=headers, data = data)

print(response.text.encode('utf8'))
