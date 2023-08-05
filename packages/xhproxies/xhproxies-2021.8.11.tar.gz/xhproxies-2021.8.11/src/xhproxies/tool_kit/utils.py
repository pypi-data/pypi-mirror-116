# -*- coding:utf-8 -*-
# @Author  : Creat by Han
import requests
from requests.exceptions import ConnectionError

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

def get_page(url, options={}):

    headers = dict(base_headers, **options)
    # print('正在抓取', url)
    try:
        response = requests.get(url, headers=headers)
        # print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        # print('抓取失败', url)
        return None
