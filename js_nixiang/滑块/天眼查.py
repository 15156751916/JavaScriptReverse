import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def parse_ty(keyword):
    url = 'https://www.tianyancha.com/search?key=' + quote(keyword)

if __name__ == '__main__':
    keyword = input('输入查询的公司：')
    parse_ty(keyword)

