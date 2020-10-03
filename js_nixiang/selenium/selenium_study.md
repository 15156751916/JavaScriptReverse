```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
```

## 添加启动参数
- 完整的启动参数可以到此网页查看：
https://peter.sh/experiments/chromium-command-line-switches/
- 实例化一个启动参数对象
```python
chrome_options = Options()
```
- 设置代理
```python
option.add_argument('--proxy-server=http://127.0.0.1:12345')
```

- 解决DevToolsActivePort文件不存在的报错
```python
chrome_options.add_argument('--no-sandbox')
```

- 设置浏览器窗口大小
```python
chrome_options.add_argument('--window-size=1366,768')
```
- 设置请求头的User-Agent
```python
chrome_options.add_argument('--user-agent=""')
```

- 无界面运行（无窗口）
```python
chrome_options.add_argument('--user-agent=""')
```

- 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
```python
chrome_options.add_argument('--headless')
```

- 最大化运行（全屏窗口）
```python
chrome_options.add_argument('--start-maximized')
```

- 隐身模式（无痕模式）
```python
chrome_options.add_argument('--incognito')
```

- 做使用selenium控制chrome时，默认会开启gpu加速功能，但GPU加速可能导致在虚拟机Chrome的CPU占用率非常高。谷歌文档提到需要加上这个属性来规避bug
```python
chrome_options.add_argument('--disable-gpu') 
```

- 隐藏滚动条, 应对一些特殊页面
```python
chrome_options.add_argument('--hide-scrollbars') 
```

- 不加载图片, 提升速度
```python
chrome_options.add_argument('blink-settings=imagesEnabled=false')
```

- 禁用javascript
```python
chrome_options.add_argument('--disable-javascript')
```

- 禁用浏览器正在被自动化程序控制的提示
```python
chrome_options.add_argument('--disable-infobars')
```

- 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
```python
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
```

- 不加载图片,加快访问速度 方法一
```python
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
```

- 禁用图片加载 方法二
```python
prefs = {
    'profile.default_content_setting_values' : {
        'images' : 2
    }
}
chrome_options.add_experimental_option('prefs',prefs)
```

- 禁用浏览器弹窗
```python
prefs = {  
    'profile.default_content_setting_values' :  {  
        'notifications' : 2  
     }  
}  
options.add_experimental_option('prefs',prefs)
```
- 启动浏览器
```python
browser = webdriver.Chrome(chrome_options=chrome_options)
```

- 请求百度首页
```python
browser.get('https://blog.csdn.net/')
```

- 生成当前页面快照并保存
```python
driver.save_screenshot("csdn.png")
```
- 关闭浏览器
```python
driver.quit()
```

## 使用了WebDriverWait以后仍然无法找到元素
- 由于分辨率设置的原因，查找的元素当前是不可见的。

- 某些页面的元素是需要向下滚动页面才会加载的。
需要滚动页面
有些页面为了性能的考虑，页面下方不在当前屏幕中的元素是不会加载的，只有当页面向下滚动时才会继续加载。
而selenium本身不提供向下滚动的方法，所以我们需要去用JS去滚动页面：
```python
for i in range(3):  # 嵌入JavaScript代码
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    time.sleep(3)
# 滚动的位置：
# 
# 网页可见区域宽： document.body.clientWidth;
# 网页可见区域高： document.body.clientHeight;
# 网页可见区域宽： document.body.offsetWidth   (包括边线的宽);
# 网页可见区域高： document.body.offsetHeight  (包括边线的宽);
# 网页正文全文宽： document.body.scrollWidth;
# 网页正文全文高： document.body.scrollHeight;
# 网页被卷去的高： document.body.scrollTop;
# 网页被卷去的左： document.body.scrollLeft;
# 网页正文部分上： window.screenTop;
# 网页正文部分左： window.screenLeft;
# 屏幕分辨率的高： window.screen.height;
# 屏幕分辨率的宽： window.screen.width;
# 屏幕可用工作区高度： window.screen.availHeight;
# 屏幕可用工作区宽度：window.screen.availWidth;
```

- 由于某些其他元素的短暂遮挡，所以无法定位到。

## 将selenium 集成到scrapy 中

## 破解selenium封禁问题

谷歌浏览器的设置中有一个参数名为excludeSwitches，它的值是一个数组，向里面添加chrome的命令就可以在selenium打开chrome后自动执行数组内的指令

检测基本原理是检测当前浏览器窗口下的 window.navigator 对象是否包含 webdriver 这个属性。因为在正常使用浏览器的情况下，这个属性是 undefined，然而一旦我们使用了 Selenium，Selenium 会给 window.navigator 设置 webdriver 属性。很多网站就通过 JavaScript 判断如果 webdriver 属性存在，那就直接屏蔽

这时候我们可能想到直接使用 JavaScript 直接把这个 webdriver 属性置空，比如通过调用 execute_script 方法来执行如下代码：

```text
Object.defineProperty(navigator, "webdriver", {get: () => undefined})
```

这行 JavaScript 的确是可以把 webdriver 属性置空，但是 execute_script 调用这行 JavaScript 语句实际上是在页面加载完毕之后才执行的，执行太晚了，网站早在最初页面渲染之前就已经对 webdriver 属性进行了检测，所以用上述方法并不能达到效果。

在 Selenium 中，我们可以使用 CDP（即 Chrome Devtools-Protocol，Chrome 开发工具协议）来解决这个问题，通过 CDP 我们可以实现在每个页面刚加载的时候执行 JavaScript 代码，执行的 CDP 方法叫作 Page.addScriptToEvaluateOnNewDocument，然后传入上文的 JavaScript 代码即可，这样我们就可以在每次页面加载之前将 webdriver 属性置空了。另外我们还可以加入几个选项来隐藏 WebDriver 提示条和自动化扩展信息，代码实现如下：

```python3
from selenium import webdriver
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(options=option)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
   'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})
browser.get('https://antispider1.scrape.cuiqingcai.com/')
```

- 除此之外，还有一些其它的标志性字符串（不同的浏览器可能会有所不同），常见的特征串如下所示：
  1. webdriver 
  2. __driver_evaluate 
  3. __webdriver_evaluate 
  4. __selenium_evaluate 
  5. __fxdriver_evaluate 
  6. __driver_unwrapped 
  7. __webdriver_unwrapped 
  8. __selenium_unwrapped 
  9. __fxdriver_unwrapped 
  10. _Selenium_IDE_Recorder 
  11. _selenium 
  12. calledSelenium 
  13. _WEBDRIVER_ELEM_CACHE 
  14. ChromeDriverw 
  15. driver-evaluate 
  16. webdriver-evaluate 
  17. selenium-evaluate 
  18. webdriverCommand 
  19. webdriver-evaluate-response 
  20. __webdriverFunc 
  21. __webdriver_script_fn 
  22. __$webdriverAsyncExecutor 
  23. __lastWatirAlert 
  24. __lastWatirConfirm 
  25. __lastWatirPrompt 
  26. $chrome_asyncScriptInfo 
  27. $cdc_asdjflasutopfhvcZLmcfl_ 
- 这些网站如果直接通过selenium打开网站,selenium会携带一些指纹信息,如:window.navigator.webdriver
- 网站js通过检测类似的指纹信息,可以检测到你在使用自动化工具,就不让你登录
### 方法一
- 执行命令 ,打开chrome的远程调试模式
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"
- user-data-dir:指定配置文件目录
```python
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('debuggerAddress','127.0.0.1:9222')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml')
```
### 方法二
- 通过 mitmproxy 屏蔽掉识别 webdriver 标识符的 js 文件
- 下载
    - pip install mitmproy
    - https://mitmproxy.org/
- mitmdump -p 8001 # windows启动  
- 在此没有找到《专利检索及分析》网站的相关js文件
- 还要在研究中
## selenium 操作cookie
```python
def get_browser():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    return browser, WebDriverWait(browser, 10)

def make_cookie(usr,pwd):
    try:
        browser, wait = get_browser()
        browser.get('http://hcc.haier.net/login')
        input_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginName')))
        input_paw = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#password')))
        login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div._3dqA1 > div > div.qdTck > button')))
        input_name.send_keys(usr)
        input_paw.send_keys(pwd)
        login_btn.click()
    except:
        return make_cookie(usr, pwd)
    try:     # 登录成功的提示页面
        confirm_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div:nth-child(10) > div > div.ant-modal-wrap > div > div.ant-modal-content > div.ant-modal-footer > button.ant-btn.ant-btn-primary.ant-btn-lg')))
        confirm_btn.click()
        cookie = browser.get_cookies()
        with open('./cookie.json', 'w') as f:  # 写入cookie
            f.write(json.dumps(cookie))`

def get_cookie(): # 获取cookie
    with open('cookie.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    return '; '.join(item for item in [item["name"] + "=" + item["value"] for item in listCookies])
if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/83.0.4103.116Safari/537.36',
        'cookie': get_cookie()
    }
    
```

## Selenium Driver操作

- get(url) :在当前浏览器会话中访问传入的url地址
- close():关闭浏览器当前窗口
- quit():退出webdriver并关闭所有窗口
- refresh():刷新当前页面
- title:获取当前页的标题
- page_source：获取当前页渲染后的源代码
- current_url：获取当前页面的url
- window_handles:获取当前会话中所有窗口的句柄

## Driver查找单个元素

- find_element_by_xpath():通过xpath查找

- find_element_by_class_name():通过class属性查找

- find_element_by_css_selector():通过css选择器查找

- find_element_by_id():通过id查找

- find_element_by_name():通过name属性进行查找

- find_element_by_partial_link_text():通过链接文本的部分匹配查找

- find_element_by_tag_name():通过标签名查找

  查找返回的是一个webelement对象

  查找多个元素：将其中的element加上一个s，则是对应的多个查找方法

## Driver获取截屏

  - get_screenshot_as_base64():获取当前窗口的截图保存为一个base64编码的字符串
  - get_screenshot_as_file(filename):获取当前窗口的截图保存为一个png格式的图片，filename参数为图片的保存地址，最后应该以.png结尾
  - get_screenshot_as_png():获取当前窗口的截图保存为一个png格式的二进制字符串

## Driver获取窗口信息

  - get_window_position(windowHandle='current') :获取当前窗口的x，y坐标
  - get_window_rect():获取当前窗口的x,y坐标和当前窗口的高度和宽度
  - get_window_size(windowHandle='current'):获取当前窗口的高度和宽度

## Driver切换操作

- switch_to_frame(frame_reference):将焦点切换到指定的子框架中

```python
#切换到新的iframe
login_frame = browser.find_element_by_xpath('//iframe[@id="tcaptcha_iframe"]')
browser.switch_to.frame(login_frame)#移动到iframe
```

  - switch_to_window(window_name):切换窗口

## Driver执行js代码

  - execute_async_script(script,*args):在当前的window/frame中异步执行js代码
  - script：是你要执行的js代码
  - *args:是你的js代码执行要传入的参数

### execute_script()是同步方法，用它执行js代码会阻塞主线程执行，直到js代码执行完毕；

### execute_async_script()方法是异步方法，它不会阻塞主线程执行。

```text
script = """
var callback = arguments[arguments.length - 1]; 
window.setTimeout(function(){ callback('timeout') }, 3000);
"""
driver.execute_async_script(script)

# 首先来看js中第一行代码 var callback = arguments[arguments.length - 1]; 
# 这里是将arguments中的最后一个参数获取出来，那么最后一个参数是什么呢？源码中看不到，这边跟大家解释一下，
# callback接受到的是一个返回数据的函数，当我们通过execute_async_script执行js语句之后，可以通过这个方法来返回内容。
# 然后再来分析一下js中第二行代码，设置了一个一秒钟之后异步执行的函数，函数的内部是执行了callback来返回一个数据。
```

```python
js = """
const callback = arguments[arguments.length - 1]
var s_ele = arguments[0];
var e_ele = arguments[1];
s_ele.readonly = false;
s_ele.value ='2020-05-15';
setTimeout(function() {
    e_ele.value ='2020-06-15';
    callback('修改成功')
}, 3000);
e_ele.readonly=false;
e_ele.value ='2020-07-15';
"""
# 输入起始时间和终止时间
res = driver.execute_async_script(js,start_date,end_date)
print(res)
```



### execute_script() 方法如果有返回值，有以下几种情况：

- 如果返回一个页面元素（document element), 这个方法就会返回一个WebElement

- 如果返回浮点数字，这个方法就返回一个double类型的数字

- 返回非浮点数字，方法返回Long类型数字

- 返回boolean类型，方法返回Boolean类型

- 如果返回一个数组，方法会返回一个List<Object>

- 其他情况，返回一个字符串

- 如果没有返回值，此方法就会返回null

  ```
  js = """
  var s_ele = arguments[0];
  var e_ele = arguments[1];
  s_ele.readonly = false;
  s_ele.value ='2020-05-15';
  e_ele.readonly=false;
  e_ele.value ='2020-06-15';
  return [s_ele.value,e_ele.value]
  """
  # js中的arguments[0]接收的是args中的第1个参数，就是下面传入的start_date
  # js中的arguments[1]接收的是args中的第2个参数，就是下面传入的end_date
  # js代码中可以通过return来返回js代码执行之后的结果
  # 执行js代码
  res = driver.execute_script(js,start_date,end_date)
  driver.quit()
  ```

## Selenium Webelement操作

- clear() ：清空对象中的内容
- click():单击对象
- get_attribute(name):优先返回完全匹配属性名的值，如果不存在则返回属性名中包含name的值
- screenshot(filename):获取当前元素的截图，保存为png，最好用绝对路径
- send_keys(value):给对象元素输入数据
- submit():提交表单

## webelement常用属性

- text:获取当前元素的文本内容
- tag_name:获取当前元素的标签名
- size：获取当前元素的大小~
- screenshot_as_png:将当前元素截屏并保存为png格式的二进制数据
- screenshot_as_base64：将当前元素截屏并保存为base64编码的字符串
- rect：获取一个包含当前元素大小和位置的字典
- parent：获取当前元素的父节点
- location：当前元素的位置
- id:当前元素的id值

## Action-Chains方法

动作链：调用动作链类可以得到一个对象，对象中有方法可以帮你做拖拽图片等操作

- click：左键单击
- context_click:右键单击
- double_click：双击
- click_and_hold:点击并抓起
```python
element = browser.find_element_by_xpath('//div[@id="tcaptcha_drag_thumb"]')
ActionChains(browser).click_and_hold(on_element=element).perform()
```
- drag_and_drop(source,target)：在source元素上点击抓起，移动到target元素上松开放下
- drag_and_drop_by_offset(source,xoffset,yoffset):在source元素上点击抓起，移动到相对source元素偏移xoffset和yoffset的坐标位置放下
- send_keys(*keys_to_send):将键发送到当前聚焦的元素
- send_keys_to_element(element.*keys_to_send):将键发送到指定的元素
- reset_actions():清除已经存储的动作

## Selenium Wait

- 显示等待

  ```python
  from selenium import wdbdriver
  from selenium.wedbriver.common.by import By
  from selenium.webdriver.support.ui import WebDriverWait
  from selenium.wedbriver.support import expected_conditions as ES
  
  driver = webdriver.Chrome()
  driver.get(网址)
  try:
      element =WebDriverWait(driver,10).until(
      EC.presence_of_element_located((By.ID,"myDynamicElement")))
  finally:
      driver.quit()
  ```

- 隐式等待：在webdriver中进行find_element这类查找操作时，如果找不到元素，则会默认的轮询等待一段时间

  ```python
  from selenium import wedbriver
  
  driver =webdriver.Chrome()
  driver.implicitly_wait(10)
  driver.get('网址')
  ```