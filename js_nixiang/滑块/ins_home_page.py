# -*- coding: utf-8 -*-
import re
import json
import asyncio
import aiohttp
import jsonpath
from loguru import logger

# 安装 aiohttp 首先安装依赖aiodns，
# pip install aiodns  -i https://pypi.tuna.tsinghua.edu.cn/simple
# pip install cchardet  -i https://pypi.tuna.tsinghua.edu.cn/simple
#
# pip install aiohttp  -i https://pypi.tuna.tsinghua.edu.cn/simple
#
# 安装jsonpath
# pip install jsonpath  -i https://pypi.tuna.tsinghua.edu.cn/simple



logger.add("".join([__file__.split(".")[0], ".log"]),
           level='DEBUG',
           encoding="utf-8",
           format='{time:YYYY-MM-DD HH:mm:ss} {level} {file}[line:{line}] {message}',
           rotation="10 MB")


class InsHomePage:

    def __init__(self,
                 user_id: str,
                 file_name: str,
                 first: int,
                 proxy: str,
                 page_url: str,
                 headers: dict,
                 first_query_hash: str,
                 next_query_hash: str
                 ):
        self.session = None
        self.file_name = file_name
        self.first = first
        self.proxy = proxy
        self.page_url = page_url
        self.headers = headers
        self.first_query_hash = first_query_hash
        self.next_query_hash = next_query_hash
        self.user_id = user_id
        self.user_info = {}
        self.edges_node = []

    async def home(self, start_url: str):
        """
        :param start_url: 个人主页的url
        :return: 服务端加密的pageNumber，用于下一次请求传参
        """
        async with self.session.get(
                url=start_url,
                proxy=self.proxy,
                headers=self.headers,
                verify_ssl=False
        ) as result:
            if result.status != 200:
                logger.error(f"个人主页响应状态码异常: {start_url}")
                return

            result_text = await result.text()

            text_content = re.findall(r"\d+.*子", result_text)[0].split("、")
            self.user_info["followers"] = text_content[0]
            self.user_info["following"] = text_content[1]
            self.user_info["posts"] = text_content[2]

            logger.info(f"用户ID: {self.user_id} 信息: {self.user_info}")

            shared_data = re.findall(r"_sharedData\s=\s\{.*\}", result_text)[0].replace("_sharedData = ", "")
            json_content = json.loads(shared_data)
            end_cursor = jsonpath.jsonpath(json_content, "$..end_cursor")[1]
            return end_cursor

    async def first_page(self, params: dict):
        """
        :param params: 默认值 query_hash=ad99dd9d3646cc3c0dda65debcd266a7&variables=%7B%22user_id%22%3A%2225025320%22%2C%22include_chaining%22%3Afalse%2C%22include_reel%22%3Afalse%2C%22include_suggested_users%22%3Afalse%2C%22include_logged_out_extras%22%3Atrue%2C%22include_highlight_reels%22%3Atrue%2C%22include_related_profiles%22%3Atrue%2C%22include_live_status%22%3Afalse%7D
        :return:
        """
        logger.info(f"用户ID: {self.user_id} 主页信息开始采集")
        async with self.session.get(
                url=self.page_url,
                proxy=self.proxy,
                headers=self.headers,
                params=params,
                verify_ssl=False
        ) as result:
            if result.status != 200:
                logger.error(f"首次翻页响应状态码异常: {await result.text()}")
                return

            result_json = await result.json()

            self.edges_node_extend(
                result_json=result_json,
                expr="$.data.user.edge_highlight_reels.edges[*].node"
            )

    def edges_node_extend(self, result_json: dict, expr: str):
        """
        :param result_json: dict对象, 原始数据
        :param expr: jsonpath匹配规则
        :return:
        """
        edges_node = jsonpath.jsonpath(result_json, expr)
        if edges_node:
            self.edges_node.extend(edges_node)
            edges_node_count = len(self.edges_node)
            logger.info(f"edges_node计数: {edges_node_count}")
        else:
            logger.error(json.dumps(result_json, ensure_ascii=False, indent=2))

    async def next_page(self, params: dict):
        """
        :param params: after值为上一个请求响应文本中的end_cursor
        :return:
        """
        await asyncio.sleep(3)  # 代理原因需要设置延时
        async with self.session.get(
                url=self.page_url,
                proxy=self.proxy,
                headers=self.headers,
                params=params,
                verify_ssl=False
        ) as result:
            if result.status != 200:
                logger.error(f"翻页响应状态码异常: {await result.text()}")
                self.save_data_to_json_file()
                return

            result_json = await result.json()

            self.edges_node_extend(
                result_json=result_json,
                expr="$.data.user.edge_owner_to_timeline_media.edges[*].node"
            )

            has_next_page = jsonpath.jsonpath(
                result_json, "$.data.user.edge_owner_to_timeline_media.page_info.has_next_page")
            if has_next_page[0]:
                end_cursor = jsonpath.jsonpath(
                    result_json, "$.data.user.edge_owner_to_timeline_media.page_info.end_cursor")
                next_page_params = {
                    "query_hash": self.next_query_hash,
                    "variables": json.dumps(
                        {
                            "id": "25025320",
                            "first": self.first,
                            "after": end_cursor[0]
                        }
                    ),
                }
                return await self.next_page(next_page_params)
            else:
                self.save_data_to_json_file()
                logger.info(f"用户ID: {self.user_id} 主页信息结束采集")

    def save_data_to_json_file(self):
        with open(self.file_name, "w+", encoding="utf-8") as fp:
            fp.write(
                json.dumps(
                    {
                        "user_info": self.user_info,
                        "edges_node": self.edges_node
                    },
                    ensure_ascii=False,
                    indent=2
                )
            )

    async def main(self):
        async with aiohttp.ClientSession() as self.session:
            first_page_params = {
                "query_hash": self.first_query_hash,
                "variables": json.dumps(
                    {
                        "user_id": "25025320",
                        "include_chaining": False,
                        "include_reel": False,
                        "include_suggested_users": False,
                        "include_logged_out_extras": True,
                        "include_highlight_reels": True,
                        "include_related_profiles": True,
                        "include_live_status": False
                    }
                )
            }

            # 获取第一页的帖子数据
            await self.first_page(first_page_params)

            # 获取下一页的pageNumber(即end_cursor, 服务端加密)
            end_cursor = await self.home(
                start_url=f"https://www.instagram.com/{user_id}/",
            )

            # 递归获取所有帖子数据, 并写入文件
            next_page_params = {
                "query_hash": self.next_query_hash,
                "variables": json.dumps(
                    {
                        "id": "25025320",
                        "first": self.first,
                        "after": end_cursor
                    }
                )
            }
            await self.next_page(next_page_params)


if __name__ == '__main__':
    user_id = "instagram"  # 用户ID
    file_name = "home_page.json"  # 采集数据存入文件
    first = 50  # 一次请求获取50条数据, 参数可改
    proxy = "http://127.0.0.1:1080"  # 墙外代理
    page_url = "https://www.instagram.com/graphql/query/"  # 翻页API
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    # query_hash写死在https://www.instagram.com/static/bundles/es6/ProfilePageContainer.js/c764fdbac4ca.js
    first_query_hash = "ad99dd9d3646cc3c0dda65debcd266a7"
    next_query_hash = "44efc15d3c13342d02df0b5a9fa3d33f"

    home_page = InsHomePage(
        user_id=user_id,
        file_name=file_name,
        first=first,
        proxy=proxy,
        page_url=page_url,
        headers=headers,
        first_query_hash=first_query_hash,
        next_query_hash=next_query_hash,
    )
    asyncio.run(home_page.main())
