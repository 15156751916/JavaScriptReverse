import json
import requests
from random import randint
import time
import hashlib

def youdaofanyi(word):
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    ts = format(time.time() , '.3f').replace('.', '')
    salt = ts + str(randint(1, 10))
    bv = hashlib.md5(ua.encode('utf-8'))
    sign_temp = "fanyideskweb" + str(word) + str(salt) + "mmbP%A-r6U3Nw(n]BjuEU"
    # sign_temp = "fanyideskweb" + "中国" + "15999930300858" + "]BjuETDhU)zqSxf-=B#7m"
    sign = hashlib.md5(sign_temp.encode('utf-8'))


    header = {
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-1334003568@10.108.160.17; OUTFOX_SEARCH_USER_ID_NCOO=670129948.8810779; _ga=GA1.2.63385724.1582769633; JSESSIONID=aaaTqfgI67jLlcro_ztmx; ___rl__test__cookies=1593761131267',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': ua,
    }
    data = {
        'i': f'{word}',
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': f'{salt}',
        'sign': f'{sign.hexdigest()}',
        'ts': f'{ts}',
        'bv': f'{bv.hexdigest()}',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME',
    }

    param = {

        'smartresult': 'dict',
        'smartresult': 'rule',

    }
    param = json.dumps(param)

    res = requests.post(url=url, data=data, json=param, headers=header).json()
    print(res)
    # json_data = json.loads(res.text)
    if res['errorCode'] != 0:
        return res['errorCode']
    for i in res['translateResult'][0]:
        return i['tgt']

if __name__ == '__main__':
    data = youdaofanyi(input('Please input the content of the translation you need:'))
    print('翻译结果为:' + data)