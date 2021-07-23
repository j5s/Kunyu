#!/usr/bin/env python
# encoding: utf-8
'''
@author: 风起
@contact: onlyzaliks@gmail.com
@File: gather_seebug.py
@Time: 2021/7/20 16:42
'''
import json
import requests
from utils.log import logger
from urllib.parse import urlencode
from core import cfg
from utils.convert_dict import convert

search_api = "https://www.seebug.org/api/get_open_vuls_by_component"
search_vul_api = "https://www.seebug.org/api/get_vul_detail_by_id"

SEEBUG_KEY = cfg


class seebug():
    headers = {
        "Content-Type": "application/json"
    }

    def __init__(self):
        self.__get_login()
        self.param = {}

    def __get_login(self):
        if SEEBUG_KEY is not None:
            self.headers["Authorization"] = f"Token {SEEBUG_KEY}"

    @classmethod
    def search(cls, search):
        try:
            cls.param = {
                "app_name": search
            }
            login_url = "%s?%s" % (search_api, urlencode(cls.param))
            resp = requests.get(
                login_url,
                headers=cls.headers
            )
            return json.loads(resp.text)
        except Exception:
            return logger.error("Failed to get SeeBug vulnerability information")










