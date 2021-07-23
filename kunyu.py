#!/usr/bin/env python
# encoding: utf-8
'''
@author: 风起
@contact: onlyzaliks@gmail.com
@File: kunyu.py
@Time: 2021/7/21 17:19
'''

from config.__version__ import __help__, init
from core.console import KunyuInterpreter
from utils.log import logger_console
from core import cfg

if __name__ == "__main__":
    try:
        if str(cfg.get("zoomeye", "apikey")) == "None" and str(cfg.get("login", "username")) == "None":
            raise Exception
        KunyuInterpreter().main()
    except Exception:
        logger_console.info(__help__.format(datil=init))
