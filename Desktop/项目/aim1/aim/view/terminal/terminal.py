# coding: utf-8
from __future__ import unicode_literals

import os
import json
import time
import sys
import socket
import platform
import psutil
import uuid
from platform import system
from datetime import datetime, timedelta
from sqlitedict import SqliteDict

import logging
logger = logging.getLogger(__name__)
 
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import terminado

from view.base.base import BaseHandler, JsonHandler
from util.common import *
from constant import *
from util.function import login_required
 
shell_command = 'cmd.exe' if system()=="Windows" else "bash" # powershell.exe

# NamedTermManager：One shared terminal per URL endpoint.
#                   Plus a /new URL which will create a new terminal and redirect to it.
# UniqueTermManager：A separate terminal for every websocket opened.
# SingleTermManager：A single common terminal for all websockets.
term_manager = terminado.UniqueTermManager(shell_command=[shell_command],
                                           max_terminals=100,
                                           )
                                           

class TerminalPageHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required
    def get(self):
        return self.render("terminal.html", 
                            ws_url_path="/websocket",
                            )