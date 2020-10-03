import js2py


print(js2py.translate_js("console.log('hello world')"))

# 将js文件翻译成Python脚本
# js2py.translate_file('test.js', 'test.py') 	# 第一个参数为需翻译的js文件，第二个为翻译后的文件

import js2py

# 在js代码中导入Python模块并使用
# 使用pyimport语法
js_code = """
pyimport requests
console.log('导入成功');
var response = requests.get('http://www.baidu.com');
console.log(response.url);
console.log(response.content);
"""
js2py.eval_js(js_code)

