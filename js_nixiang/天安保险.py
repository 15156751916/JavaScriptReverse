import json

import execjs
import requests
def login(name, password):
  url = "https://tianaw.95505.cn/tacpc/tiananapp/customer_login/taPcLogin?jsonKey=NBLetNAD6tHSqG1kmgP12SFiv6oyyRDdvklJemP%2BPaVt2ZXfShmGHupsfnZhroojbcgcdTqremqbaTJCNH82dNV316ZBxZFEtZ15QT4nXl6RuAl9v8xKEzLoEd%2FUOnEhzL%2BK3huYiXo3%2F4kYWWLnjV69qy4UcZ7RQHxI%2Fs%2Fo114XxGuSkWYkJgtCEqMZkMO7E9tJLijKzi9SUqyvKGABU5tad7qVRpEvYeUrQe%2B5vlIkLamkhGR0ox7sVQGdyvKwX81%2FQf0S0%2BUsqCVkTzkKYw%3D%3D"
  # rawdata = '"{"body":{"loginMethod":"1","name":"%s","password":"%s"},"head":{"userCode":null,"channelCode":"101","transTime":1600046799393,"transToken":"","customerId":null,"transSerialNumber":""}}"'%('1111','2222')
  rawdata = '"{"body":{"loginMethod":"1","name":"%(name)s","password":"%(password)s"},"head":{"userCode":null,"channelCode":"101","transTime":1600046799393,"transToken":"","customerId":null,"transSerialNumber":""}}"'%{'name': name,'password': password}
  with open('sources/天安保险.js', 'r')as f:
    content = f.read()
  ctx = execjs.compile(content)
  result = ctx.call('Encrypt', json.dumps(rawdata))
  payload = {
    'jsonKey':result
  }
  payload = json.dumps(payload)

  headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'https://tianaw.95505.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://tianaw.95505.cn/tacpc/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'JSESSIONID=CFF1C75868044C0E399611D3D766632D; cookiesession1=1C998C8F1OOVQ6QN2JDS24G0NJCE2068'
  }
  proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
  response = requests.request("POST", url, headers=headers, proxies=proxies, verify=False, data = payload)
  # response = requests.post(url=url, headers=headers, proxies=proxies, verify=False, data = payload)
  return response

if __name__ == '__main__':
  response = login('15156127362', '15156127362')
  print(response.content.decode('utf8'))