#!/usr/bin/env python
# encoding: utf-8
'''
@author: 风起
@contact: onlyzaliks@gmail.com
@File: console.py
@Time: 2021/7/19 22:35
'''

import sys
import platform
import subprocess
from core import args
from utils.log import logger
from rich.console import Console
from lib.export import Createdir
from core.gather_zoomeye import ZoomEye
from utils import readlineng as readline
from config.__version__ import __introduction__
PLATFORM = platform.system()
cmd = "cls" if PLATFORM == "Windows" else "clear"

console = Console(color_system="auto")


def readline_available():
    """
    Check if the readline is available. By default
    it is not in Python default installation on Windows
    """
    return readline._readline is not None


def auto_completion(completion=None, console=None):
    if not readline_available():
        return
    readline.set_completer_delims(" ")
    readline.set_completer(console)
    readline.parse_and_bind("tab: complete")


class BaseInterpreter(object):
    global_help = ""
    OUTPUT_PATH = None

    def __init__(self):
        self.module = "ZoomEye"
        self.complet = eval(self.module).Command_Info
        self.setup()
        Createdir()

    def setup(self):
        """ Initialization of third-party libraries
        Setting appropriate completer function.
        """
        auto_completion(completion=4, console=self.complete)

    def parse_line(self, line):
        command, _, args = line.strip().partition(" ")
        return command, args.strip()

    def setter(self, line):
        args, _, number = line.strip().partition("=")
        args, number = args.strip(), number.strip()
        if hasattr(eval(self.module), args):
            setattr(eval(self.module), args, number)
        return True

    @property
    def prompt(self):
        """ Returns prompt string """
        return f"Kunyu\033[31;1m ({self.module})\033[0m > "

    def get_command_handler(self, command):
        """ Parsing command and returning appropriate handler.
        :param command: command
        :return: command_handler
        """
        try:
            command_handler = getattr(eval(self.module), "command_{}".format(command))

        except AttributeError:
            logger.error("Unknown command: '{}'".format(command))
            return False

        return command_handler

    def complete(self, text, state):
        """Return the next possible completion for 'text'.
        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """
        if state == 0:
            start_index = readline.get_begidx()
            if start_index != 0:
                complete_function = self.default_completer
            else:
                complete_function = self.raw_command_completer

            self.completion_matches = complete_function(text)
        try:
            return self.completion_matches[state]
        except IndexError:
            return None

    def raw_command_completer(self, text):
        """ Complete command w/o any argument """
        return [command for command in self.complet if command.startswith(text)]

    def default_completer(self, *ignored):
        return []

    def auxiliary(self, command, line=None):
        if command == "clear":
            subprocess.call(cmd, shell=True)
            return True
        elif command == "exit":
            raise KeyboardInterrupt
        elif command == "help":
            console.print(eval(self.module).help)
            return True
        elif command == "set":
            return self.setter(line)
        return False

    def start(self):
        # logger_console(self.global_help)
        while True:
            try:
                command, args = self.parse_line(input(self.prompt))
                command = command.lower()
                if self.auxiliary(command, args) or not command:
                    continue
                command_handler = self.get_command_handler(command)
                command_handler(args)
            except EOFError:
                logger.info("Kunyu Console mode stopped")
                break
            except KeyboardInterrupt:
                logger.info("Console Exit")
                sys.exit(0)
            except Exception:
                continue


class KunyuInterpreter(BaseInterpreter):

    def __init__(self):
        super().__init__()
        self.global_help = __introduction__.format(datil=eval(self.module).help)
        console.print(self.global_help)

    def main(self):
        super().start()
