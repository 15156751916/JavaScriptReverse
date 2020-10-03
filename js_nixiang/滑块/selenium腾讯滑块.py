import cv2 as cv
import requests
from selenium import webdriver
# 导入鼠标事件类
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.chrome import options
"""
pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install selenium -i https://pypi.tuna.tsinghua.edu.cn/simple
"""

class TencentSlider():
    # 计算到缺口的位置
    @staticmethod
    def get_pos(image):
        """
        缺口轮廓检测
        对付腾讯滑块够用
        该方法识别率 95% 左右
        """
        blurred = cv.GaussianBlur(image, (5, 5), 0)
        canny = cv.Canny(blurred, 200, 400)
        contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for i, contour in enumerate(contours):
            m = cv.moments(contour)
            if m['m00'] == 0:
                cx = cy = 0
            else:
                cx, cy = m['m10'] / m['m00'], m['m01'] / m['m00']
            if 6000 < cv.contourArea(contour) < 8000 and 370 < cv.arcLength(contour, True) < 390:
                if cx < 400:
                    continue
                x, y, w, h = cv.boundingRect(contour)  # 外接矩形
                cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # cv.imshow('image', image)   # 展示滑块的图片
                return x, y, w, h
        return 0

    # 加速度函数
    @staticmethod
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

    # 初始化webdriver
    @property
    def get_browser(self):
        opt=options.Options()
        #opt.add_argument('--headless')
        #opt.add_argument('--incognito')
        opt.add_argument('--disable-infobars')
        #opt.add_argument('--user-agent="Mozilla/5.0 (Linux; Android 4.2.1; M040 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36"')
        opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        browser = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options=opt)
        return browser

    def parse_tencent(self):
        browser = self.get_browser
        browser.maximize_window()
        browser.get('https://007.qq.com/online.html')

        browser.find_elements_by_xpath('//div[@class="wp-onb-tit"]/a')[1].click()

        browser.find_element_by_xpath('//button[@id="code"]').click()
        time.sleep(5)

        #切换到新的iframe
        login_frame = browser.find_element_by_xpath('//iframe[@id="tcaptcha_iframe"]')
        browser.switch_to.frame(login_frame)#移动到iframe

        #下载图片
        src=browser.find_element_by_id('slideBg').get_attribute('src')
        print('图片链接：',src)
        img=requests.get(src).content
        with open('../test.jpg', 'wb')as f:
            f.write(img)

        img0 = cv.imread('../test.jpg')

        res=TencentSlider.get_pos(img0)
        distance=res[0]
        print('距离：',distance)
        cv.waitKey(0)
        cv.destroyAllWindows()

        element = browser.find_element_by_xpath('//div[@id="tcaptcha_drag_thumb"]')
        ActionChains(browser).click_and_hold(on_element=element).perform()
        #move_to_element_with_offset():移动到距离某个元素左上角多少距离的位置 distance[0]/2 - 25
        ActionChains(browser).move_to_element_with_offset(to_element=element,xoffset=220,yoffset=0).perform()

        # 6、使用加速度函数移动剩下的距离
        tracks = TencentSlider.get_tracks(25)
        for track in tracks:
            #开始移动 move_by_offset() 鼠标从当前位置移动多少距离
            ActionChains(browser).move_by_offset(xoffset=track,yoffset=0).perform()

        # 7、延迟释放鼠标: release()
        time.sleep(0.5)
        ActionChains(browser).release().perform()
        print('ok')

if __name__ == '__main__':
    slider = TencentSlider()
    slider.parse_tencent()
