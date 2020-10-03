$.fn 自定义jquery函数
btoa('1111111')   // base64编码 只有在浏览器中才有
atob($_) //base64解码
VM 通常是由eval或者是function生成的 是一个虚拟出来的代码
VM文件内的 VM断点只对当前页面有效，如果页面刷新则会重生成一个VM文件
开发者工具搜索技巧：在搜索栏中打开正则匹配\b 表示字符串的边界 比如 只想匹配sign 可以使用\bsign\b
js 分析： sign: dSFHBqxz7Yt1hd3wMbAHQlMwlYcS%2F1LNAhXYj8uL9BU%3D
位数固定可能是一个消息摘要算法
协议头结束的标志，服务器是以空行进行判断的
提交数据的结尾是以content-length:进行判断的
### set-cookie：路径 时间 域名 中httponly是JavaScript获取不到的
cookie key=value; key=value; key=value; key=value; 一定遵循分号加空格，因为网站可能是以;分割或者是空格分割
可能会出现302 就禁止重定向
因为 requets 库自动处理了重定向请求了，默认是allow_redirects=True 是启动重定向
allow_redirects=False
可以使用响应对象的 history 方法来追踪重定向。
- 合并更新步骤
    - 新cookie去除无效cookie
        - a="" or a=deleted
    - 在新cookie里，寻找是否在旧cookie里的名字，存在就用新的，丢掉旧的
    - 两个cookie组合到一个位版本变量中
    
### python3 requests禁用安全请求警告
```python
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 禁用安全请求警告
```
### 代码纠错技巧
- 提交的数据该编码没有编码（有些二次编码）
- 提交的数据不该写死的写死
- 替换数据的时候不够仔细
- 忽略了一些看似没用的关键的请求
- 延迟（有些网站会校验延迟时间，如果时间过快，会判断为一个爬虫，比如有些网站认为从登录到打开这个页面必须要5秒钟，他才认为你不是机器人）
- 关键变量调试输出
- 断点调试
- 对自己的python 程序抓包和fiddler抓取的数据包进行对比


### &amp; 只表示& 符号
- 应用场景
- 在<form></form>提交数据的时候使用&amp;替换为&符号


