from selenium import webdriver
# 导入鼠标事件类
from selenium.webdriver import ActionChains
import time

from selenium.webdriver.chrome import options
opt=options.Options()
#opt.add_argument('--headless')
opt.add_argument('--incognito')
opt.add_argument('--disable-infobars')
#opt.add_argument('--user-agent="Mozilla/5.0 (Linux; Android 4.2.1; M040 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36"')
opt.add_experimental_option('excludeSwitches', ['enable-automation'])
# prefs = {
#     'profile.default_content_setting_values' : {
#         'images' : 2,
#         'notifications': 2
#     },
# }
# opt.add_experimental_option('prefs',prefs)

# 加速度函数
def get_tracks(distance):
    """
    拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
    匀变速运动基本公式：
    ①v=v0+at
    ②s=v0t+½at²
    """
    # 初速度
    v = 0
    # 单位时间为0.3s来统计轨迹，轨迹即0.3内的位移
    t = 0.3
    # 位置/轨迹列表,列表内的一个元素代表0.3s的位移
    tracks = []
    # 当前的位移
    current = 0
    # 到达mid值开始减速
    mid = distance*4/5
    while current < distance:
        if current < mid:
            # 加速度越小,单位时间内的位移越小,模拟的轨迹就越多越详细
            a = 2
        else:
            a = -3

        # 初速度
        v0 = v
        # 0.3秒内的位移
        s = v0*t+0.5*a*(t**2)
        # 当前的位置
        current += s
        # 添加到轨迹列表
        tracks.append(round(s))
        # 速度已经达到v，该速度作为下次的初速度
        v = v0 + a*t
    return tracks
    # tracks: [第一个0.3秒的移动距离,第二个0.3秒的移动距离,...]


# 1、打开豆瓣官网 - 并将窗口最大化
browser = webdriver.Chrome(options=opt)
browser.maximize_window()
browser.get('https://www.douban.com/')

# 2、切换到iframe子页面
login_frame = browser.find_element_by_xpath('//*[@id="anony-reg-new"]/div/div[1]/iframe')
browser.switch_to.frame(login_frame)#移动到iframe

# 3、密码登录 + 用户名 + 密码 + 登录豆瓣
browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]').click()
browser.find_element_by_xpath('//*[@id="username"]').send_keys('13520791099')
browser.find_element_by_xpath('//*[@id="password"]').send_keys('zygx8666')
browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]/a').click()
time.sleep(4)

# 4、切换到新的iframe子页面 - 滑块验证
auth_frame = browser.find_element_by_xpath('//*[@id="TCaptcha"]/iframe')
browser.switch_to.frame(auth_frame)

# 5、按住开始滑动位置按钮 - 先移动180个像素
element = browser.find_element_by_xpath('//*[@id="tcaptcha_drag_button"]')
ActionChains(browser).click_and_hold(on_element=element).perform()
#move_to_element_with_offset():移动到距离某个元素左上角多少距离的位置
ActionChains(browser).move_to_element_with_offset(to_element=element,xoffset=180,yoffset=0).perform()

# 6、使用加速度函数移动剩下的距离
tracks = get_tracks(25)
for track in tracks:
    #开始移动 move_by_offset() 鼠标从当前位置移动多少距离
    ActionChains(browser).move_by_offset(xoffset=track,yoffset=0).perform()

# 7、延迟释放鼠标: release()
time.sleep(0.5)
ActionChains(browser).release().perform()
print('ok')