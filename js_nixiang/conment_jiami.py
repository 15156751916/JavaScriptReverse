
# 我们所说的加密方式，都是对二进制编码的格式进行加密的，对应到Python中，则是我们的Bytes。
# 所以当我们在Python中进行加密操作的时候，要确保我们操作的是Bytes，否则就会报错

# binascii模块包含很多在二进制和ASCII编码的二进制表示转换的方法。
import binascii
a = b'hello world'
# 先把hello world转换成二进制数据然后在用十六进制表示
b = binascii.b2a_hex(a)
# print(b)
# 与b2a_hex相反
binascii.a2b_hex(b)
# 这个功能和b2a_hex()一样
c = binascii.hexlify(a)
# print(c)
# 这个功能和a2b_hex()一样
binascii.unhexlify(c)

# 把10进制转整形换成16进制
hex(15)

# 把浮点型转换成16进制
3.1415926.hex()
# 内置函数hex和binascii.hexlify()的区别就在于，hex只能接受整形不能接受字符串

# bin():把十进制整形转换成二进制字符
bin(1024)

# oct():把十进制转换成八进制字符
oct(10)

# chr():把一个整形转换成ASCII码表中对应的单个字符 ,该参数必须是在范围[0..255]。
chr(97)

# ord():和chr相反，把ASCII码表中的字符转换成对应的整形
ord("A")

# Hexlify的优势在于可以同时处理多个字符。下面2个操作有一定类似性，返回值都是字符串，不过hexlify去掉了’0x’。
hex(ord('a')) # 只能处理一个字符串
binascii.hexlify(b'a')
##################################################################################

#  URL编码
# 正常的URL中是只能包含ASCII字符的，也就是字符、数字和一些符号。而URL编码就是一种浏览器用来避免url中出现特殊字符（如汉字）的编码方式。
# 其实就是将超出ASCII范围的字符转换成带%的十六进制格式。
# urllib.parse模块使用
# parse模块：url的解析，合并，编码，解码

# urlparse()实现URL的识别和分段
from urllib import parse
url = 'https://www.baidu.com/s?wd=from%20urllib%20import%20parse&rsv_spt=1&rsv_iqid=0x832745f7000076c0&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&oq=python%2520URL%25E7%25BC%2596%25E7%25A0%2581&rsv_btype=t&inputT=844&rsv_t=39b8lC8MqqGjzJbde9Q0jogpdQdl2SCin8Hd8SMc94xh3GQ7PN%2B7cTDiVK4XENXweNx7&rsv_pq=9bd97d480003883f&rsv_n=2&rsv_sug3=17&rsv_sug2=0&prefixsug=from%2520urllib%2520import%2520parse&rsp=2&rsv_sug4=844'
"""
url：待解析的url
scheme=''：假如解析的url没有协议,可以设置默认的协议,如果url有协议，设置此参数无效
allow_fragments=True：是否忽略锚点,默认为True表示不忽略,为False表示忽略
"""
result = parse.urlparse(url=url,scheme='http',allow_fragments=True)
# print(result)
"""
scheme:表示协议
netloc:域名
path:路径
params:参数
query:查询条件，一般都是get请求的url
fragment:锚点，用于直接定位页
面的下拉位置，跳转到网页的指定位置
"""
# urlencode()将字典构形式的参数序列化为url编码后的字符串（常用来构造get请求和post请求的参数
from urllib import parse
from urllib import request

url = 'http://www.baidu.com/s?'
dict1 ={'wd': '你好世界！'}
url_data = parse.urlencode(dict1) #unlencode()将字典{k1:v1,k2:v2}转化为k1=v1&k2=v2
# print(url_data)             #url_data：wd=%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C%EF%BC%81
data = request.urlopen((url+url_data)).read() #读取url响应结果
data = data.decode('utf-8') #将响应结果用utf8编码

# parse_qs()将url编码格式的参数反序列化为字典类型
str4 = parse.parse_qs(url_data)     # {'wd': ['你好世界！']}
# print(str4)
# print(data)

# 解码url
url_org = parse.unquote(url_data) #解码url
# print(url_org)              #url_org：wd=百度翻译
str1 = '你好世界！'
str2 = parse.quote(str1)    #将字符串进行编码
print(str2)                 #%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C%EF%BC%81
str3 = parse.unquote(str2)  #解码字符串

# urljoin()传递一个基础链接,根据基础链接可以将某一个不完整的链接拼接为一个完整链接
base_url = 'https://blog.csdn.net'
sub_url = '/qq_21531681'
full_url = parse.urljoin(base_url,sub_url)
print(full_url)


# ascii  ##########################################################################
def get_ascii():
    for x in 'adbdA':
        print(f'{x} is : ',ord(x))

# md5  ##########################################################################
import hashlib

def get_string_md5():
    info = b'111'
    m = hashlib.md5()
    # m.update(info.encode('utf-8'))
    m.update(info)
    print(m.hexdigest())
get_string_md5()
def get_file_md5(fname:str) -> str:
    hash_md5 = hashlib.md5()

    with open(fname, 'rb') as f:
        for chunk in iter(lambda :f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# base64  ##########################################################################
import base64
def set_base64():
    str = b'hello world'
    # t = base64.b64encode(str.encode('utf-8'))
    t = base64.b64encode(str)
    print(t)
def get_base64():
    str = b'dSFHBqxz7Yt1hd3wMbAHQlMwlYcS%2F1LNAhXYj8uL9BU%3D'
    t = base64.b64decode(str)
    print(t)

# AES  ##########################################################################
# pip install pycryptodome -i https://pypi.tuna.tsinghua.edu.cn/simple
# PyCrypto 已死,请替换为 PyCryptodome
# 需要在python目录里面把Python36\Lib\site-packages下的crypto文件改名，没错，就是直接改成Crypto。结果就能用了...


# 时间戳 ########################################################################
import time
time_1 = time.time()  # 十六位
time_1 = str(format(time.time(), '.3f'))
time_1 = str(format(time.time(), '.3f')).replace('.', '')  # 十三位
str(int(time_1))  # 十位

# requests禁止重定向
# 在requests.get 中添加属性 allow_redirects=False

if __name__ == '__main__':
    # pass
    # get_ascii()
    get_string_md5()
    # set_base64()
    # get_base64()
##################################################################################

