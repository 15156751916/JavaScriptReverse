import json
import requests
import execjs

def login(username, password, companyName):
    url = 'http://passport.wsgjp.com.cn/erp/login'
    header = {
        'Accept': 'application/json,text/javascript,*/*;q=0.01',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '1470',
        'Content-Type': 'application/json',
        # 'Cookie': 'Hm_lvt_1712ba79db147472df18b469e42780b8=1599546232;_ga=GA1.3.1599689521.1599546235;_gid=GA1.3.1819722937.1599546235;Qs_lvt_68170=1599559444;Qs_pv_68170=623827412289810600;__root_domain_v=.wsgjp.com.cn;_qddaz=QD.v8u2kk.7n2hos.ketse6ay;Hm_lpvt_1712ba79db147472df18b469e42780b8=1599585967;_gat=1;SERVERID=b06d0a4b12f7d80bec1b05bc6c98deae|1599585974|1599546233',
        'Host': 'passport.wsgjp.com.cn',
        'Origin': 'http://passport.wsgjp.com.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://passport.wsgjp.com.cn/erp/login?productid=0',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/85.0.4183.83Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    with open('sources/管家婆_RAS.js', 'r')as f:
        content = f.read()
    ctx = execjs.compile(content)
    result = ctx.call('test', username, password)
    print(result)

    data = {
        "clientinfo": "Zmxhc2g6YmVnaW5eXm5hdmlnYXRvcjpiZWdpbl5ec2NyZWVuRFBJOnVuZGVmaW5lZF5eY29va2llRW5hYmxlZDp0cnVlXl5wbGF0Zm9ybTpXaW4zMl5eYXBwQ29kZU5hbWU6TW96aWxsYV5eYXBwTWlub3JWZXJzaW9uOnVuZGVmaW5lZF5eYXBwTmFtZTpOZXRzY2FwZV5eYXBwVmVyc2lvbjo1LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg1LjAuNDE4My44MyBTYWZhcmkvNTM3LjM2Xl5icm93c2VyTGFuZ3VhZ2U6dW5kZWZpbmVkXl5jcHVDbGFzczp1bmRlZmluZWReXnN5c3RlbUxhbmd1YWdlOnVuZGVmaW5lZF5edXNlckFnZW50Ok1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84NS4wLjQxODMuODMgU2FmYXJpLzUzNy4zNl5edXNlckxhbmd1YWdlOnVuZGVmaW5lZF5ebGFuZ3VhZ2U6emgtQ05eXmxhbmd1YWdlOnpoLUNOXl5vc2NwdTp1bmRlZmluZWQ=",
        "companyName": companyName,
        "host": "wsgjp.com.cn",
        "https": False,
        "password": result["password"],
        "productId": "14",
        "ref": "http://passport.wsgjp.com.cn/erp/login?productid=0",
        "rememberMe": False,
        "showNotice": True,
        "userName": result["usename"],
        "validateCode": "",
    }
    data = json.dumps(data)
    res = requests.post(url=url, data=data, headers=header).json()
    print(res)

if __name__ == '__main__':
    data = login("yun",'study000@', "yuhuitong")
    print(data)
