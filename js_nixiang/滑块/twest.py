import time

from selenium.webdriver.chrome import options
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
try:
    opt = options.Options()
    opt.add_argument('--disable-infobars')
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver.maximize_window()
    driver.get('https://account.dianping.com/login?redir=http://www.dianping.com')
    # driver.implicitly_wait(3)  # 使用隐式等待
    # 切换到  id为iframeResult 的 iframe标签页面中
    wait = WebDriverWait(driver, 20)
    # 切换到新的iframe
    login_frame = driver.find_element_by_xpath('//*[@id="tab-page-account"]')
    driver.switch_to.frame(login_frame)  # 移动到iframe
    input_name = wait.until(EC.presence_of_element_located((By.ID, '#account-textbox')))
    input_paw = wait.until(EC.presence_of_element_located((By.ID, '#password-textbox')))
    login_btn = wait.until(
        EC.element_to_be_clickable((By.ID, '#login-button-account')))
    input_name.send_keys("15156751916")
    input_paw.send_keys("a123456")
    login_btn.click()
    driver.switch_to.frame('tab-page-account')
    # 需要拖动图片块的 源位置
    source = driver.find_element_by_id('yodaBox')
    print(source.location)
    # 根据id为droppable 属性查找目标快 标签对象
    target = driver.find_element_by_id('droppable')
 # 滑块的距离
    distance = target.location.get('x') - source.location.get('x')
    # 注意: 只要是 ActionChains(driver)调用的方法，都需要调用 perform方法来执行
    # 先点击鼠标，按住拖拽的标签
    ActionChains(driver).click_and_hold(source).perform()
    number = 0
    while number < distance:

     # 循环滑动，每次滑动3 每次移动3格
        ActionChains(driver).move_by_offset(xoffset=3,yoffset=0).perform()
        number += 3
        # 移动完毕后，必须释放
        ActionChains(driver).release().perform()
        time.sleep(100)
finally:
    driver.close()
