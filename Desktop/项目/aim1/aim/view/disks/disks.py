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
     
class DisksHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        data = yield self.asynchronous()
        self.render('disks.html', **data)

    @run_on_executor
    def asynchronous(self):
        disks = get_disks(all_partitions=True)
        io_counters = get_disks_counters().items()
        io_counters = list(io_counters)
 
        io_counters.sort(key=lambda x: x[1]['read_count'], reverse=True)
    
        data = {
            'disks': disks,
            'io_counters': io_counters,
            'page': 'disks',
        }
        return data