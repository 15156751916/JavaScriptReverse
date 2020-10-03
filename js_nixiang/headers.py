headers= """
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8
cache-control: no-cache
cookie: kg_mid=fa123fe2c3e1ef211f8f36f8c9939e55; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1600565207; kg_dfid=2B4WfR1KbldX0sulfx0ayWXT; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1600565822
pragma: no-cache
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: none
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36
"""
header = ''
for i in headers:
    if i == ':':
        i = "':'"
    if i == '\n':
        i = "',\n'"
    header += i
print(header[2:].replace(' ', '')+'\'')

# (.*?):(.*)
# '$1':'$2',


import json
json.dumps('长盈精密')
# \u957f\u76c8\u7cbe\u5bc6
# ArqMaOP6sNozEzw2I61gh23OC-vfazINsPuy9cS1YgsYblRdrPuOVYB_AtCX