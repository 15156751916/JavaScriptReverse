import json
import requests
import execjs

def youdaofanyi(word):
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    header = {
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-1334003568@10.108.160.17; OUTFOX_SEARCH_USER_ID_NCOO=670129948.8810779; _ga=GA1.2.63385724.1582769633; JSESSIONID=aaaTqfgI67jLlcro_ztmx; ___rl__test__cookies=1593761131267',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }

    js_code = '''
         var md5 = function(content) {
             var crypto = require('crypto');
             var result = crypto.createHash('md5').update(content).digest("hex")
             console.log(result);
             return result
        };
        var r = function(e) {
            var t = md5("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36")
              , r = "" + (new Date).getTime()
              , i = r + parseInt(10 * Math.random(), 10);
            return {
                ts: r,
                bv: t,
                salt: i,
                sign: md5("fanyideskweb" + e + i + "Nw(nmmbP%A-r6U3EUn]Aj")
            }
        };
    '''
    ctx = execjs.compile(js_code)
    result = ctx.call('r', word)
    print(result)
    data = {
        'i': f'{word}',
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': f'{result["salt"]}',
        'sign': f'{result["sign"]}',
        'ts': f'{result["ts"]}',
        'bv': f'{result["bv"]}',
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