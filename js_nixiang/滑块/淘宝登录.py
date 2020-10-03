from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
# 创建WebDriver对象
browser = webdriver.Chrome()
# 等待变量
wait = WebDriverWait(browser, 10)
# 模拟搜索Python编程基础
# 打开淘宝首页
def search():
    try:
        browser.get('https://www.taobao.com/')
        # 等待输入框加载完成
        tb_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        # 等待搜索按钮加载完成
        search_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )
        # 输入框中传入书包
        # time.sleep(20)  # 登录淘宝的时间
        tb_input.send_keys('python书籍')
        # 点击搜索

        search_btn.click()
        # 加载完成，获取页数元素
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'))
        )
        print('获取页数元素:',total.text)
        # 获取元素中的文本
        get_products()
        return total.text
    # 若发生异常，重新调用自己
    except TimeoutException:
        return search()


# 翻页函数
# 等待翻页输入框加载完成
def next_page(page_number):
    try:
        page_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        confirm_btn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )  # 等待确认按钮加载完成
        page_input.clear()  # 清空翻页输入框
        page_input.send_keys(page_number)  # 传入页数
        confirm_btn.click()  # 确认点击翻页
        # #根据高亮区域显示数字来判断页面是否跳转成功
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number))
        )
        get_products()
    # 若发生异常，重新调用自己
    except TimeoutException:
        next_page(page_number)


# 获取商品信息
# 等待商品信息加载完成，商品信息的CSS选择器分析HTML源码得到
def get_products():
    # 判断商品的item是否加载出来
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'))
    )
    # 得到页面HTML源码
    html = browser.page_source
    from lxml import etree
    res = etree.HTML(html)
    div_list = res.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
    result_all = []
    for div in div_list:
        result = {}
        result['price'] = div.xpath('./div[2]/div[1]/div[1]/strong/text()')[0]
        result['name'] = div.xpath('./div[2]/div[2]/a/text()')
        result['name'] = ''.join(result['name']).replace(' ', '').replace('\n', '')
        result['Sales_volume'] = div.xpath('./div[2]/div[1]/div[2]/text()')[0].split('人')[0]
        result['store_name'] = div.xpath('./div[2]/div[3]/div[1]/a/span[2]/text()')[0]
        result['location'] = div.xpath('./div[2]/div[3]/div[2]/text()')[0]
        result_all.append(result)
    print(result_all)
    bookInfo = pd.DataFrame(result_all)
    bookInfo.to_excel('./bookInfo.xlsx')

    return result_all


def main():
    total = search()
    total = int(re.search('(\d+)', total).group(1))
    for i in range(2, total + 10):
        next_page(i)


if __name__ == '__main__':
    main()




