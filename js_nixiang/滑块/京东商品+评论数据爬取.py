import execjs
import requests
from bs4 import BeautifulSoup
import time,math
import json

headers={
    'cookie': '__jdu=1833331475; shshshfpa=481e02e3-8f7d-05e6-646d-bc0cab689cc6-1593777581; shshshfpb=q8%2FQbdps2iF3a37y24zlFig%3D%3D; user-key=925f43cd-f3b5-4b70-879c-3f2d80f23989; cn=0; unpl=V2_ZzNtbRYFRxZ2WBEGch4PAmIEFlhLBEVAcAEWU3NLDgcyVBFeclRCFnQUR1JnGl0UZgoZWEdcQBBFCEdkeB5fA2AFEFlBZxBFLV0CFi9JH1c%2bbRJcRV5CE3cPRVB7Gmw1ZAMiXUNnQxx3CkRWexxaAVczFW1yZ0UcfQhCUEsYbARXQUYBQlJEEX1FRl15G14HZwYUWXJWcxY%3d; PCSYCityID=CN_140000_0_0; qrsc=3; areaId=6; ipLoc-djd=6-350-363-0; rkv=V0300; __jdv=76161171|baidu|-|organic|not set|1595208968984; __jda=122270672.1833331475.1593777578.1595205797.1595208969.4; __jdc=122270672; shshshfp=02662de1eddf263dde1e3a63cb1f0cfc; 3AB9D23F7A4B3C9B=KL744CPEZCLB7MVWKB3PKSFBSXH7GIF5YU4RXJSLKSHRNWJCIQCHOFQIQDMZSQCMWLHVDUU5PX4SVFMF6EKUFBDNFA; __jdb=122270672.4.1833331475|4.1595208969; shshshsID=0b8f61796b8eb047fad7dd4f06eb4c5f_4_1595208986941',
'referer': 'https://www.jd.com/',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

jscode="""
genPvid = function() {
            var a = (new Date).getTime();
            var b = "xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx".replace(/[xy]/g, function(b) {
                var c = (a + 16 * Math.random()) % 16 | 0;
                return a = Math.floor(a / 16),
                ("x" == b ? c : 3 & c | 8).toString(16)
            });
            return b
        }
"""
def getPvid():
    data=execjs.compile(jscode)
    result=data.call('genPvid')
    print('获取pvid：',result)
    return str(result)

params={
    'keyword': '手表',
    'enc': 'utf-8',
    'suggest': '1.his.0.0',
    'pvid':getPvid()
}

def getCommentCount(uid):
    params={
        'referenceIds': str(uid),
        'callback': 'jQuery2687893',
        '_': str(math.floor(time.time()*1000))
    }
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    url='https://club.jd.com/comment/productCommentSummaries.action'
    html=requests.get(url,params=params,headers=headers).text
    start=html.find('{"Comment')
    end=html.find('}]}')+len('}]}')
    jsonData=json.loads(html[start:end])
    return jsonData['CommentsCount'][0]['CommentCountStr']

def getComment(uid):
    url='https://club.jd.com/comment/productPageComments.action'
    params={
        'callback': 'fetchJSON_comment98',
        'productId': str(uid),
        'score': '0',
        'sortType': '5',
        'page': '1',
        'pageSize': '10',
        'isShadowSku': '0',
        'rid': '0',
        'fold': '1'
    }
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    html=requests.get(url,params=params,headers=headers).text
    start=html.find('{"productAtt')
    end=html.find('}]}')+len('}]}')
    jsonData=json.loads(html[start:end])
    for comment in jsonData['comments']:
        print('评论：',comment['content'])



url='https://search.jd.com/Search'

html=requests.get(url,params=params,headers=headers)
soup=BeautifulSoup(html.text,'lxml')
blocks=soup.select('li.gl-item')
print(blocks)
for block in blocks:
    dataId=block['data-sku']
    title=block.select('.p-name')[0].text.strip().replace(" ",'').replace('\n','')
    price=block.select(' .p-price')[0].text.strip().replace(" ",'').replace('\n','')
    shop=block.select('.p-shop')[0].text.strip().replace(" ",'').replace('\n','')
    comment=block.select(' .p-commit')[0].text.strip().replace(" ",'').replace('\n','')
    img=block.select(' .p-img a img')[0]
    innerHref='https:'+block.select('.p-name a ')[0]['href']
    print('商品ID：',dataId)
    print('商品标题：',title)
    print('商品价格：',price)
    print('商品店家：',shop)
    print('评论数：',getCommentCount(dataId))
    print('商品图片：',img['src'])
    #https://item.jd.com/25643111839.html
    #//item.jd.com/5398175.html
    print('内部链接：',innerHref)
    getComment(dataId)
    print('-'*10)
