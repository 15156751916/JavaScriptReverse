from bs4 import BeautifulSoup
import requests
from lxml import etree
import os

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}
# with requests.session() as session:
#     html = session.get("https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4", headers =  head)
#     #print(html.text)
#     #soup = BeautifulSoup(html.text, "html.parser")
#     soup = BeautifulSoup(html.text, "lxml")
#     print(soup)
#     print("\n======================================================")
#     tbody = soup.select("#wrapper li h2 a")
#     #tbody = soup.select("")
#     #print(tbody)
#     for t in tbody:
#         if t.text == "\r\n":
#             print("空行")
#             continue
#         print(t.text.strip().replace("\n", ""))

# with requests.session() as session:
#     html = session.get("https://www.zygx8.com/forum.php", headers = head)
#     soup = etree.HTML(html.text)
#     result = soup.xpath("//a/font/b/text()")
#     #print(result)
#     for i in  result:
#         print(i)

# trash = ["javascript:void(0);"]
# with requests.session() as  session:
#     html = session.get("https://www.zygx8.com/forum.php", headers = head)
#     soup = etree.HTML(html.text)
#     result = soup.xpath("//div[@id='wp']//td/a/@href")
#     for i in  result:
#         if i in trash:
#             continue
#         print(i)
#//li[@class="subject-item"]//img/@src
# with requests.session() as  session:
#     html = session.get("https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4", headers = head)
#     soup = etree.HTML(html.text)
#     result = soup.xpath("//li[@class='subject-item']//img/@src")
#     #print(result)
#     for i in  result:
#         print(i)

# with requests.session() as session:
#     html = session.get("https://news.sina.com.cn/")
#     html.encoding = "utf8"
#
#     soup = BeautifulSoup(html.text, "lxml")
#     s = soup.select("#syncad_1 a")
#     #soup = soup.select("//div[@id='syncad_1']//a") etree
#     for i in s:
#         print(i.text)
#         print(i["href"])
#     print("====================================================================")
#     # soup = etree.HTML(html.text)
#     # soup = soup.xpath("//div[@id='syncad_1']//a")
#     # for i in  soup:
#     #     print(i.text)
#     #     #print(i["@href"])
#
#     s = soup.select("#blk_ndxw_01 ul a")
#     for i in s:
#         print(i.text)
#         print(i["href"])

#千图网
#https://www.58pic.com/piccate/53-0-0-g1862_1846-p1.html
#https://www.58pic.com/piccate/53-0-0-g1862_1846-p2.html

with requests.session() as  s:
    html = s.get("https://www.58pic.com/piccate/53-0-0-g1862_1846-p1.html", headers = head)
    soup = BeautifulSoup(html.text, "lxml")
    result = soup.select(".qtw-card.item a")
    for i in result:
        #print(i)
        imgUrl = "https:" + i["href"]
        print(imgUrl)
        name = i.img["alt"]
        print(name)


        with requests.session() as ss:
            imgHtml = ss.get(imgUrl, headers = head)
            soup2 = BeautifulSoup(imgHtml.text, "lxml")
            result2 = soup2.select("#show-area-height img")

            if not os.path.exists("qt"):
                os.mkdir("qt")

            #with open("qt/{}.jpg".format(name), "wb") as f:
            f = open("qt/{}.jpg".format(name), "wb")
            #i = 0
            for j in  result2:
                png = "https:" + j["src"]
                print(png)
                f.write(requests.get(png, headers=head).content)
            f.close()

                # with open("qt/{}.jpg".format(i), "wb") as f:
                #     f.write(requests.get(png, headers=head).content)
        break