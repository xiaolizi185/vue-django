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
       
class ProcessesHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, sort='pid', order='desc', filter='user', ):
        data = yield self.asynchronous(sort, order, filter)
        self.render('processes.html', **data)
        
    @run_on_executor
    def asynchronous(self, sort, order, filter):
        procs = get_process_list()
 
        procs.sort(
            key=lambda x: x.get(sort),
            reverse=True if order != 'asc' else False
        )

        data = {
            'processes': procs,
            'sort': sort,
            'order': order,
            'filter': filter,
            'num_procs': len(procs),
            'page': 'processes',
            'urllib':urllib,
            'PY3':PY3,

        }
        return data

 