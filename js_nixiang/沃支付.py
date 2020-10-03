import requests
import execjs
import time

def login():
    login_url = 'https://epay.10010.com/auth/Login'
    header = {
        'Host': 'epay.10010.com',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:80.0)Gecko/20100101Firefox/80.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate,br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '582',
        'Origin': 'https://epay.10010.com',
        'Connection': 'keep-alive',
        'Referer': 'https://epay.10010.com/auth/minipage/loginWindow_newlogin.jsp',
        'Cookie': 'JSESSIONID=E494832CC15AF55E03AC4F5C3E771E7B; epay-4=!0Q/mo6jy6eHzjRVhTcfnGVNBkShXKbg27u/+/C5SRvAg1V88uL8whVrGjv1R3XjvF/NwqKzlhBy41GU=; WT_FPC=id=2754915afa58a121c161599639912445:lv=1599639953994:ss=1599639912445; epay-3=!h5lpexg/fIznXmhPE/7nbu3JRU5Tky1a8v2RT/bCxlARKsCOoJaJABuhcj+KfDxwzpzUJrgDS2FwqVw=; _fmdata=Q%2FQkH0M4ZhudXexFDYjBZnbz6pSaFBixWmJx5n0vr38TMp1bXBKxzrUm9eru3fc2HqTj8%2BgusAwd3gnFRxyIGjsDjsVLisXRQSQJk7%2BQL6U%3D',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    with open('sources/沃支付_RAS.js', 'r')as f:
        content = f.read()
    ctx = execjs.compile(content)
    loginPwd = ctx.call('encryptRequest', "111111", getPubKey())
    print(loginPwd)

    data = {
        "errorurl": "https://epay.10010.com/auth/auth/errorPage.jsp",
        "RelayState": "type%3DC%3Bbackurl%3Dhttps%3A%2F%2Fepay.10010.com%2Fauth%2Fauth%2FloginBack.jsp%3Bspid%3D4028f09638eb576a013904e27b440002%3Bnl%3D8%3BloginFrom%3Dhttps%3A%2F%2Fepay.10010.com%2Fpss%2Fuser%2Fmy",
        "loginType": "1",
        "loginPwdType": "1",
        "loginPwd": loginPwd,
        "flag": "no",
        "userid": "15156751628",
        "pwd": "",
        "validCode": "uypd"
    }
    res = requests.post(url=login_url, data=data, headers=header)
    return res


def getPubKey():
    getPubKey_url = 'https://epay.10010.com/auth/auth/getPubKey.jsp'
    header = {
        'Host': 'epay.10010.com',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:80.0)Gecko/20100101Firefox/80.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate,br',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://epay.10010.com/auth/minipage/loginWindow_newlogin.jsp',
        'Cookie': 'JSESSIONID=E494832CC15AF55E03AC4F5C3E771E7B; epay-4=!0Q/mo6jy6eHzjRVhTcfnGVNBkShXKbg27u/+/C5SRvAg1V88uL8whVrGjv1R3XjvF/NwqKzlhBy41GU=; WT_FPC=id=2754915afa58a121c161599639912445:lv=1599640919024:ss=1599639912445; epay-3=!h5lpexg/fIznXmhPE/7nbu3JRU5Tky1a8v2RT/bCxlARKsCOoJaJABuhcj+KfDxwzpzUJrgDS2FwqVw=; _fmdata=Q%2FQkH0M4ZhudXexFDYjBZnbz6pSaFBixWmJx5n0vr38TMp1bXBKxzrUm9eru3fc2HqTj8%2BgusAwd3gnFRxyIGjsDjsVLisXRQSQJk7%2BQL6U%3D',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    result = requests.get(url=getPubKey_url, data={'_': str(format(time.time(), '.3f')).replace('.', '')}, headers=header)
    code = result.text.strip().split("--")[0]
    mer = result.text.strip().split("--")[1]
    if code != '200' and (mer == None or mer == ""):
        print("获取加密的公钥失败！")
        return -1
    print('获取加密的公钥:' + mer)
    return mer

if __name__ == '__main__':
    res = login()
    print(res.content.decode('utf8'))
    print(res.status_code)
