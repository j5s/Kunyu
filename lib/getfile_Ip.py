#!/usr/bin/env python
# encoding: utf-8
'''
@author: 风起
@contact: onlyzaliks@gmail.com
@File: getfile_Ip.py
@Time: 2021/6/16 21:05
'''

import sys
import re
from utils.log import logger
from functools import wraps

def GetIp(func):
    __ip_list = []

    @wraps(func)
    def Getfile(file):
        try:
            if file.endswith(".txt"):
                logger.info("File load successful")
            else:
                logger.warning("Only input TXT type files are allowed")
                raise Exception
            nonlocal __ip_list
            with open(file, "r", encoding='utf-8') as ip_text:
                for line in ip_text:
                    __ip_list.append(line.strip())
            return filter(func, __ip_list)
        except Exception:
            # ([LRE])Hidden garbled code appearing before the file path can also cause an error.
            # Copy from right to left will lead to appear [LRE] tabs,Whereas not.
            return logger.error("please check the file name is correct")
    return Getfile


@GetIp
def Check_fileip(ip):
    from config.setting import IP_ADDRESS_REGEX
    return True if re.search(IP_ADDRESS_REGEX, ip) \
        else logger.warning(ip + ":It's an illegal IP address")


# Get the contents of the IP list.
def get_file(*args, **kwargs):
    _ip_list = []
    try:
        for i in Check_fileip(*args, **kwargs):
            _ip_list.append(i)
        return _ip_list
    except Exception:
        logger.error("Failed to get IP list content! Please check if the IP file name is abnormal")
        sys.exit(0)



