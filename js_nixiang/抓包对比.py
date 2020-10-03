import requests
proxies = {'http': 'http://localhost:8888', 'https':'http://localhost:8888'}
url = 'http://www.baidu.com'
requests.post(url, proxies=proxies, verify=False)