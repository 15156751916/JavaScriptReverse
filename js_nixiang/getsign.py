"""
    coding: utf-8

    @author: 吃多了没事做

    @time:2020-09-10:21:46

"""

import hashlib
import time
from pprint import pprint

import requests
from loguru import logger

class GetSign:

    def __init__(self):
        self.uuid = 'IMEI352531084029493-IMSI460NNNNANNNNQWE'       # 手机的 uuid
        self._str = 'f1190aca-d08e-4041-8666-29931cd89dde'          # 固定值



    def getSign(self):
        _time = str(int(time.time()))
        _str = self.uuid + '&&' +_time + '&&' + self._str
        # _str = self.uuid + '&&' +  str(1599745445) + '&&' + self._str
        logger.info(f'原始的字符串为：{_str}')

        signature = hashlib.md5(_str.encode()).hexdigest()
        logger.info(f'字符串经过 MD5 之后 signature 为：{signature}')

        headers = {
            'Host': 'app.suzhou-news.cn',
            'sys': 'Android',
            'sysversion': '8.1.0',
            'appversion': '8.2',
            'appversioncode': '54',
            'udid': self.uuid,
            'clienttype': 'android',
            'timestamp': _time,
            'signature':  signature,
            'user-agent': 'okhttp/3.9.0',
        }

        # params = (
        #     ('page', '2'),
        #     ('bannerID', '11'),
        # )
        params = {
            'page': '2',
            'bannerID':'11'
            }
        response = requests.get('https://app.suzhou-news.cn/api/v1/appNews/getBannerNewsList7', headers=headers, params=params)
        pprint(response.text)




    def _main(self):
        self.getSign()


if __name__ == '__main__':
    gs = GetSign()
    gs._main()
