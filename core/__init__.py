#!/usr/bin/env python
# encoding: utf-8
'''
@author: 风起
@contact: onlyzaliks@gmail.com
@File: __init__.py
@Time: 2021/6/21 16:26
'''

import os
import sys
import argparse
import configparser
from utils import *
import configparser

from utils.log import logger
import config.setting as config

from config.__version__ import __title__, __help__
from config.__version__ import usage, init




parser = argparse.ArgumentParser(prog=__title__)

# console pattern subcommand
subparsers = parser.add_subparsers()
parser_group_console = subparsers.add_parser('console', help='enter console mode',
                                             description=__help__.format(datil=usage),
                                             formatter_class=argparse.RawDescriptionHelpFormatter,
                                             usage=argparse.SUPPRESS, add_help=True)

# Initial Configuration
parser_init_console = subparsers.add_parser('init', help='enter console mode',
                                            description=__help__.format(datil=init),
                                            formatter_class=argparse.RawDescriptionHelpFormatter,
                                            usage=argparse.SUPPRESS, add_help=True)

parser_init_console.add_argument("--apikey", help='ZoomEye API Key')
parser_init_console.add_argument("--username", help='ZoomEye Username')
parser_init_console.add_argument("--password", help='ZoomEye Password')
parser_init_console.add_argument("--seebug", help='ZoomEye Password')

args = parser.parse_args()

# Gets the absolute path of the project
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

cfg = configparser.ConfigParser()
__path = os.path.join(path, "config", "user.ini")

# Read config.user.ini
cfg.read(__path)

try:
    if args.apikey:
        cfg.set("zoomeye", "apikey", args.apikey)

    elif args.username and args.password:
        cfg.set("login", "username", args.username)
        cfg.set("login", "password", args.password)

    if args.seebug:
        cfg.set("seebug", "apikey", args.seebug)

except Exception:
    pass

with open(__path, "w+") as f:
    cfg.write(f)
