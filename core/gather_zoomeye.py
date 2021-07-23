#!/usr/bin/env python
# encoding: utf-8
'''
@author: 风起
@contact: onlyzaliks@gmail.com
@File: gather_zoomeye.py
@Time: 2021/6/24 22:18
'''

import json
import random
import requests
from core import cfg
from rich.table import Table
from config.setting import UA
import lib.FileEncode as encode
from rich.console import Console
from lib.export import export_xls
from utils.log import logger, logger_console


console = Console(color_system="auto", record=True)

# ZoomEye API
login_api = "https://api.zoomeye.org/user/login"
user_info_api = "https://api.zoomeye.org/resources-info"
host_search_api = "https://api.zoomeye.org/host/search"
web_search_api = "https://api.zoomeye.org/web/search"
both_search_api = "https://api.zoomeye.org/both/search"
domain_search_api = "https://api.zoomeye.org/domain/search"

ZOOMEYE_KEY = cfg.get("zoomeye", "apikey")
ZOOMEYE_EMAIL = cfg.get("login", "username")
ZOOMEYE_PASS = cfg.get("login", "password")

params = {}


class zoomeye_search(object):
    def __init__(self, method="POST"):
        self.auth = None
        self.search = None
        self.page = 1
        self.method = method
        self.headers = {
            "User-Agent": random.choice(UA)
        }

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            nonlocal func
            req_list = []
            login_url = func(self, *args, **kwargs)
            for num in range(int(self.page)):
                params['query'], params['page'] = self.search, (num + 1)
                req_list.append(self.__request(login_url, data=params, headers=self.headers))
            return req_list

        return wrapper

    def __request(self, login_url, data=None, headers=None):
        self.__get_login()
        # The API is not available for tourist users.
        try:
            if self.method == "GET":
                resp = requests.get(
                    login_url,
                    data=data,
                    headers=headers,
                    timeout=10
                )
            else:
                resp = requests.post(
                    login_url,
                    data=data,
                    headers=headers,
                    timeout=10
                )
            # check http status code 500 or 503
            if resp.status_code in [500, 503]:
                raise requests.HTTPError(f"ZoomEye Server Error, Status: {resp.status_code}")
            self.check_error(resp)
            return json.loads(resp.text)

        except requests.HTTPError as err:
            return logger.warning(err)
        except requests.exceptions.ConnectionError:
            return logger.error("Network timeout")

    # Check return error info
    def check_error(self, resp):
        if json.loads(resp.text).get("error"):
            raise requests.HTTPError(json.loads(resp.text).get("message"))

    # Obtain the user login credentials and use them dynamically
    def __get_login(self):
        if ZOOMEYE_KEY is None:
            param = f'{{"username": "{ZOOMEYE_EMAIL}", "password": "{ZOOMEYE_PASS}"}}'
            try:
                resp = requests.post(
                    login_api,
                    data=param
                )
                self.check_error(resp)
            except Exception as err:
                return logger.error(err)
            self.headers["Authorization"] = "JWT %s" % json.loads(resp.text)["access_token"]
        else:
            self.headers["API-KEY"] = ZOOMEYE_KEY


# After the SDK public,The interface to get the data.
@zoomeye_search(method="GET")
def _dork_search(self, url, search, page):
    try:
        if int(page) <= 0 or page is None:
            raise ArithmeticError
        self.page = page
        self.search = search
        return url
    except ArithmeticError:
        return logger.warning("Please enter the correct number of queries!")
    except Exception:
        return logger.warning("Search for parameter exceptions!")
    except requests.exceptions.ConnectionError:
        return logger.error("Network timeout")


@zoomeye_search(method="GET")
# Get ZoomEye User Info
def _user_info(self):
    return user_info_api


# The Display class of the tool
class ZoomEye:
    from config.setting import ZOOMEYE_FIELDS_HOST, ZOOMEYE_FIELDS_WEB, ZOOMEYE_FIELDS_INFO, ZOOMEYE_FIELDS_DOMAIN
    from utils.convert_dict import convert

    page = 1
    dtype = 0
    btype = "host"
    help = """Global commands:
        info                                      Print User info
        SearchHost <query>                        Basic Host search
        SearchWeb <query>                         Basic Web search
        SearchIcon <File>/<URL>                   Icon Image Search
        SearchBatch <File>                        Batch search Host
        SearchCert <Domain>                       SSL certificate Search
        SearchDomain <Domain>                     domain name associated/subdomain search
        Seebug <Query>                            Search Seebug vulnerability information
        set <Option>                              SET arguments values (result)
        clear                                     clear the console screen
        help                                      Print Help info
        exit                                      Exit KunYu & """

    Command_Info = ["help", "info", "set", "Seebug", "SearchWeb", "SearchHost", "SearchIcon", "SearchBatch", "SearchCert", "SearchDomain", "clear", "exit"]

    def __init__(self):
        self.fields_tables = None

    def __command_search(self, search, types="host"):
        table = Table(show_header=True, style="bold")
        global total, api_url, result, FIELDS, export_host
        total, num = 0, 0
        result_type = "matches"
        export_list = []

        # Gets the API for the call
        api_url, FIELDS = host_search_api, self.ZOOMEYE_FIELDS_HOST
        if types == "web":
            api_url, FIELDS = web_search_api, self.ZOOMEYE_FIELDS_WEB
        elif types == "domain":
            result_type = "list"
            params['q'], params['type'] = search, self.dtype
            api_url, FIELDS = domain_search_api, self.ZOOMEYE_FIELDS_DOMAIN

        try:
            for cloumn in FIELDS:
                table.add_column(cloumn, justify="center", overflow="ignore")
        except Exception:
            return logger.warning("Please enter the correct field")

        # Get data information
        for result in _dork_search(api_url, search, self.page):
            # Check return data Whether it is empty
            if not result:
                return logger.error("No data returned")

            try:
                total = result['total']
                webapp_name, server_name, db_name, system_os, language = "", "", "", "", ""
                for i in range(len(result[result_type])):
                    num += 1
                    title = ""
                    data = self.convert(result[result_type][i])
                    if api_url == host_search_api:
                        if data.portinfo.title:
                            title = data.portinfo.title[0]
                        # Set the output field
                        table.add_row(str(num), data.ip, str(data.portinfo.port), str(data.portinfo.service),
                                      str(data.portinfo.app), str(data.geoinfo.isp), str(data.geoinfo.city.names.en),
                                      str(title), str(data.geoinfo.location.lat),
                                      str(data.geoinfo.location.lon))

                        # Set the exported fields
                        export_host = [str(num), data.ip, str(data.portinfo.port), str(data.portinfo.service),
                                       str(data.portinfo.app), str(data.geoinfo.isp), str(data.geoinfo.city.names.en),
                                       str(title), str(data.geoinfo.location.lat),
                                       str(data.geoinfo.location.lon)]

                    elif api_url == web_search_api:
                        # Because of the problem of returning the default value of the field
                        if data.webapp:
                            webapp = self.convert(data.webapp[0])
                            webapp_name = webapp.name
                        if data.server:
                            server = self.convert(data.server[0])
                            server_name = server.name
                        if data.db:
                            db = self.convert(data.db[0])
                            db_name = db.name
                        if data.language:
                            language = data.language[0]
                        if data.system:
                            system = self.convert(data.system[0])
                            system_os = system.name
                        # Set the output field
                        table.add_row(str(num), data.ip[0], str(data.site), str(data.title),
                                      str(system_os), str(webapp_name), str(db_name),
                                      str(language), str(server_name))

                        # Set the exported fields
                        export_host = [str(num), data.ip[0], str(data.site), str(data.title),
                                       str(system_os), str(webapp_name), str(db_name),
                                       str(language), str(server_name)]

                    elif types == "domain":
                        # Set the output field
                        table.add_row(str(num), str(data.name), str(data.ip), str(data.timestamp))

                        # Set the exported fields
                        export_host = [str(num), str(data.name), str(data.ip), str(data.timestamp)]
                    export_list.append(export_host)

                if export_list:
                    export_xls(export_list, FIELDS)
            except Exception as e:
                print(e)
                continue
        console.log("search result amount:", total, style="green")
        console.print(table)
        logger.info("Search information retrieval is completed\n")
        return console

    @classmethod
    def command_info(cls, *args):
        table = Table(show_header=True, style="bold")
        info = cls.convert(_user_info()[0])
        for column in cls.ZOOMEYE_FIELDS_INFO:
            table.add_column(column, justify="center", overflow="ignore")
        console.log("User Information:", style="green")
        table.add_row(str(info.plan), str(info.resources.search), str(info.resources.stats),
                      str(info.resources.interval))
        console.print(table)
        logger.info("User information retrieval is completed\n")

    @classmethod
    def command_searchhost(cls, search):
        return cls.__command_search(cls, search)

    @classmethod
    def command_searchweb(cls, search):
        return cls.__command_search(cls, search, types="web")

    @classmethod
    # domain name associated / subdomain Search
    def command_searchdomain(cls, search):
        return cls.__command_search(cls, search, types="domain")

    @classmethod
    # ZoomEye batch search IP method
    def command_searchbatch(cls, filename):
        from lib.getfile_Ip import get_file
        search = ""
        # Use ZooEye batch query mode,Search: "ip:1.1.1.1 ip:2.2.2.2 ip:3.3.3.3"
        for ip in get_file(filename):
            search += f"ip:{ip} "
        if cls.btype == "host":
            return cls.command_searchhost(search)
        return cls.command_searchweb(search)

    @classmethod
    # ZoomEye SSL Cert Search
    def command_searchcert(cls, hostname):
        if encode.Cert_Encode(hostname) is not None:
            return cls.__command_search(cls, "ssl:" + str(encode.Cert_Encode(hostname)))

    @classmethod
    # ZoomEye Icon Image Search
    def command_searchicon(cls, filename):
        if encode.Encode_mmh3(filename) is not None:
            return cls.__command_search(cls, "iconhash:" + str(encode.Encode_MD5(filename)))

    @classmethod
    # Get SeeBug vulnerability information
    def command_seebug(cls, search):
        from core.gather_seebug import seebug
        total = seebug.search(search).get("total")
        data = seebug.search(search)
        logger.info(f"Number of relevant vulnerabilities: {total}")
        for vuln in data["results"]:
            vuln = cls.convert(vuln)
            logger_console.info(f'[{vuln.name}] - [{vuln.id}]')
        logger.info("Seebug Search retrieval is completed\n")


