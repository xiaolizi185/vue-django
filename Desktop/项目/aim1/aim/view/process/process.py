# coding: utf-8
from __future__ import unicode_literals

import os
import json
import urllib
import time
import sys
import socket
import platform
import psutil
import uuid
from platform import system
from datetime import datetime, timedelta

import logging
logger = logging.getLogger(__name__)

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.util import  PY3
from view.base.base import BaseHandler
from util.common import *
       
class ProcessHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, pid, section='overview'):
        data = yield self.asynchronous(pid, section)
        self.render('process/%s.html' % section, **data)

    @run_on_executor
    def asynchronous(self, pid, section):
        pid = int(pid)
        data = {
            'process':get_process(pid),
            'section': section,
            'page': 'processes',
            'os_type': 'windows' if system()=='Windows' else 'linux',
        }

        if section == 'environment':
            data['process_environ'] = get_process_environment(pid)
        elif section == 'threads':
            data['threads'] = get_process_threads(pid)
        elif section == 'files':
            data['files'] = get_process_open_files(pid)
        elif section == 'connections':
            data['connections'] = get_process_connections(pid)
        elif section == 'memory':
            data['memory_maps'] = get_process_memory_maps(pid)
        elif section == 'children':
            data['children'] = get_process_children(pid)
        elif section == 'limits':
            data['limits'] = get_process_limits(pid)
 
        return data
 