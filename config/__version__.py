#!/usr/bin/env python
# encoding: utf-8
'''
@author: 风起
@contact: onlyzaliks@gmail.com
@File: __version__.py
@Time: 2021/6/15 21:11
'''

import sys
import platform

__title__ = 'Kunyu'
__license__ = 'Kunyu 1.1'
__python_version__ = sys.version.split()[0]
__platform__ = platform.platform()
__url__ = "https://github.com/wikiZ/Kunyu"
__version__ = '1.1'
__author__ = '风起'
__Team__ = 'WgpSec狼组安全团队'
__author_email__ = 'onlyzaliks@gmail.com'
__copyright__ = 'Copyright (C) 2021 风起. All Rights Reserved'
__introduction__ = """
          ___           ___           ___           ___           ___     
         /\__\         /\__\         /\__\         |\__\         /\__\    
        /:/  /        /:/  /        /::|  |        |:|  |       /:/  /    
       /:/__/        /:/  /        /:|:|  |        |:|  |      /:/  /     
      /::\__\____   /:/  /  ___   /:/|:|  |__      |:|__|__   /:/  /  ___ 
     /:/\:::::\__\ /:/__/  /\__\ /:/ |:| /\__\     /::::\__\ /:/__/  /\__\\
     \/_|:|~~|~    \:\  \ /:/  / \/__|:|/:/  /    /:/~~/~    \:\  \ /:/  /
        |:|  |      \:\  /:/  /      |:/:/  /    /:/  /       \:\  /:/  / 
        |:|  |       \:\/:/  /       |::/  /     \/__/         \:\/:/  /  
        |:|  |        \::/  /        /:/  /                     \::/  /    -V {version} Alpha
         \|__|         \/__/         \/__/                       \/__/    


GitHub:{url}

Kunyu is Cyberspace Resources Surveying and Mapping auxiliary tools

{{datil}}

""".format(version=__version__, url=__url__)

__help__ = """
 _  __                       
| |/ /   _ _ __  _   _ _   _ 
| ' / | | | '_ \| | | | | | |
| . \ |_| | | | | |_| | |_| |
|_|\_\__,_|_| |_|\__, |\__,_| -v{version}
                 |___/         
GitHub: https://github.com/
Kunyu is Cyberspace Resources Surveying and Mapping auxiliary tools
{{datil}}
""".format(version=__version__)

usage = """
Usage:
    python3 Kunyu.py -h
    python3 Kunyu.py console
""".format(module="ZoomEye")

init = """
Usage:
    python3 Kunyu.py -h
    python3 Kunyu.py init -h
    python3 Kunyu.py init --apikey "01234567-acbd-00000-1111-22222222222"
    python3 Kunyu.py init --username "404@knownsec.com" -password "P@ssword"
    python3 Kunyu.py init --seebug "a73503200157abcdef981bcc89a1452c34d62b8c"
    python3 Kunyu.py init --apikey "01234567-acbd-0000" --seebug "a73503200157"(推荐)
"""
