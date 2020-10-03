import json

import execjs
import requests
url = "https://www.cls.cn/v1/user/login?app=CailianpressWeb&os=web&sv=7.2.2&sign=6ac194f4b3b39d45631708474e058b73"

# payload = "{\"login_type\":1,\"password\":\"dc483e80a7a0bd9ef71d8cf973673924\",\"phone\":\"15156751827\",\"captcha\":\"\",\"os\":\"web\",\"sv\":\"7.2.2\",\"app\":\"CailianpressWeb\"}"
with open('sources/财联社md5.js', 'r')as f:
  content = f.read()
ctx = execjs.compile(content)
result = ctx.call('MD5', "a123456")
payload = {
  "app": "CailianpressWeb",
  "captcha": "",
  "login_type": 1,
  "os": "web",
  "password": result,
  "phone": "15156751917",
  "sv": "7.2.2",
}
payload = json.dumps(payload)
headers = {
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'Accept': 'application/json, text/plain, */*',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
  'Content-Type': 'application/json;charset=UTF-8',
  'Origin': 'https://www.cls.cn',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://www.cls.cn/',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'Cookie': 'HWWAFSESID=0342b941a616d3b0a4; HWWAFSESTIME=1599743015529; hasTelegraphNotification=on; hasTelegraphRemind=on; hasTelegraphSound=on; vipNotificationState=on; Hm_lvt_fa5455bb5e9f0f260c32a1d45603ba3e=1599712089,1599732116,1599743017; Hm_lpvt_fa5455bb5e9f0f260c32a1d45603ba3e=1599743017'
}
response = requests.request("POST", url, headers=headers, data = payload)

print(response.content.decode('utf8'))
