#!/usr/bin/env python
# encoding: utf-8
'''
@author: 风起
@contact: onlyzaliks@gmail.com
@File: readlineng.py
@Time: 2021/7/19 11:18
'''

import os
_readline = None
PLATFORM = os.name


try:
    from readline import *
    import readline as _readline
except ImportError:
    try:
        from pyreadline import *
        import pyreadline as _readline
    except ImportError:
        # raise PocsuiteSystemException("Import pyreadline faild,try pip3 install pyreadline")
        pass

if PLATFORM == 'windows' and _readline:
    try:
        _outputfile = _readline.GetOutputFile()
    except AttributeError:
        _readline = None

# Test to see if libedit is being used instead of GNU readline.
# Thanks to Boyd Waters for this patch.
uses_libedit = False

if PLATFORM == 'mac' and _readline:
    import subprocess

    (status, result) = subprocess.getstatusoutput("otool -L %s | grep libedit" % _readline.__file__)

    if status == 0 and len(result) > 0:
        # We are bound to libedit - new in Leopard
        _readline.parse_and_bind("bind ^I rl_complete")
        uses_libedit = True

if _readline:
    try:
        _readline.clear_history()
    except AttributeError:
        def clear_history():
            pass


        _readline.clear_history = clear_history