import json

import tornado


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Welcome.")

    def post(self):
        self.write("Welcome.")


class ActionHandler(tornado.web.RequestHandler):
    """ index目录
    """

    def initialize(self, chrome_fetch):
        # 用户任务
        self.chrome_fetch: ChromeFetch = chrome_fetch

    def get(self):
        self.write("Welcome.")

    def post(self):
        """ start 开始任务命令
        """
        try:
            json_body = json.loads(self.request.body.decode())
            # print(json_body)

            if json_body['code'] == 0:

                data_json = json_body['data']
                shop_id = data_json['mtWmPoiId']
                data_list = [shop_id]
                # data_list.append(data_json['shopStar'])
                data_list.append(data_json['isBrand'])
                data_list.append(','.join(data_json['shopPhone']))
                data_list.append(','.join(data_json['licencePics']))
                data_list.append(data_json['poiQualificationInfo']['url'])
                # data_list.append(data_json['tip'])
                data_list.append('')
                data_list.append(str(data_json['shopLat']))
                data_list.append(str(data_json['shopLng']))

                city_address_list = [shop_basic[9], shop_basic[10]]

                new_list = self.chrome_fetch.shop_id_now[1:7] + data_list + city_address_list + [get_date_str()]
                print('---', new_list)

            else:
                self.chrome_fetch.shop_id_now = json_body['msg']

        except Exception as err:
            print('ActionHandler:', err)

        self.write('哈哈')


def tornado_start(chrome_fetch, http_listen_port=8888):
    """ 启动web服务器 """

    app = tornado.web.Application([
        (r"/", MainHandler),  # 空类
        (r"/action", ActionHandler, dict(chrome_fetch=chrome_fetch))  # 接收信息
    ])
    app.listen(http_listen_port)
    tornado.ioloop.IOLoop.current().start()
