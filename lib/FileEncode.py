#!/usr/bin/env python
# encoding: utf-8
'''
@author: 风起
@contact: onlyzaliks@gmail.com
@File: FileEncode.py
@Time: 2021/6/15 15:40
'''

from config.setting import IP_ADDRESS_REGEX, HTTP_CHECK_REGEX
from utils.log import logger
import requests
import hashlib
import codecs
import mmh3
import re
import os


class encode_hash:
    """"
        According to different search engines,
        Select the appropriate ICO icon encryption method.
        ZoomEye, for example, supports both MMH3 and MD5,But FoFa only supports MMH3.
        Through the ICO icon search Related assets,It's very always efficient.
        Security researchers can also modify code files as needed.
    """

    def __init__(self, func):
        self.filename = None
        self.status = False
        self.func = func

    def __call__(self, *args, **kwargs):
        self.filename, self.status = self.func(*args, **kwargs)
        icohash = encode_hash.HTTP_Encode(self) if self.CheckHTTP() else self.File_Encode()
        return icohash if icohash is not None else logger.warning("The hash was not successfully computed")

    def CheckHTTP(self):
        from tld import get_fld
        # Determine if it is valid URL.
        if re.search(IP_ADDRESS_REGEX, self.filename):
            return True
        if re.findall(HTTP_CHECK_REGEX, self.filename):
            if get_fld(self.filename):
                return True
            return False

    def File_Encode(self):
        # MD5 encrypted files.
        if os.path.isfile(self.filename):
            fp = open(self.filename, 'rb')
            contents = fp.read()
            fp.close()
        else:
            return logger.warning("No Such File or URL!")

        return hashlib.md5(contents).hexdigest() if self.status else mmh3.hash(
            codecs.lookup('base64').encode(contents)[0])

    def HTTP_Encode(self):
        try:
            if self.status:
                return hashlib.md5(requests.get(self.filename, timeout=0.5).content).hexdigest()
            else:
                return mmh3.hash(codecs.lookup('base64').encode(requests.get(self.filename, timeout=0.5).content)[0])
        except:
            return


@encode_hash
def Encode_MD5(filename):
    return filename, True


@encode_hash
def Encode_mmh3(filename):
    return filename, False


def Cert_Encode(hostname, system=16):
    import ssl
    import socket
    try:
        c = ssl.create_default_context()
        host = re.sub(HTTP_CHECK_REGEX, '', hostname)
        s = c.wrap_socket(socket.socket(), server_hostname=host)
        s.connect((host, 443))
        return int(s.getpeercert()["serialNumber"], system)

    except Exception:
        return logger.warning("Please confirm that the domain name provided is HTTPS applicable!")



