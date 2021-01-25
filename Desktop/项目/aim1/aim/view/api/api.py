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
 
from view.base.base import BaseHandler, JsonHandler
from util.common import *
from constant import *

class GetDiskInfoHandler(JsonHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        object = yield self.asynchronous()

        self.write_json(object)
        self.write_success( data=object )
        self.write_fail( message='调用接口失败' )

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        object = yield self.asynchronous()
        self.write_json(object)
 
    @run_on_executor
    def asynchronous(self):
        object = {'list': [1, 2, 3],'name':'王海庆'}
        return object