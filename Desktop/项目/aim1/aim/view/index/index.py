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
 
from view.base.base import BaseHandler
from util.common import *
from constant import *

class IndexHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        data = yield self.asynchronous()
        self.render('index.html', **data)
        
        # tornado.ioloop.IOLoop.instance().add_callback(self.asynchronous)  # 这样将在下一轮事件循环执行self.sleep
        # self.write("发送任务成功， 稍后请查询！" )
        # self.finish()

    @run_on_executor
    def asynchronous(self):
        mydict = SqliteDict(filename=DATABASE, tablename='monitoring', autocommit=True)
        cpu_name = mydict.get('cpu_name', None)
        cpu_percent = mydict.get('cpu_percent', None)
        rate_dict = mydict.get('rate_dict', {})
        mydict.close()

        io_counters = psutil.net_io_counters(pernic=True)
        addrs = psutil.net_if_addrs()
        net_list = []
        for index, io in enumerate(io_counters):
            index = str(index)
            temp_dict = {}
            temp_dict['name'] = io
            temp_dict['bytes_sent'] = io_counters[io].bytes_sent
            temp_dict['bytes_recv'] = io_counters[io].bytes_recv

            temp_dict['send_rate'] = rate_dict.get(index+'_send_rate',0)
            temp_dict['recv_rate'] = rate_dict.get(index+'_recv_rate',0)

            all_ip,all_netmask = get_net_ip_and_netmask(addrs, io)
            temp_dict['ip'] = all_ip
            temp_dict['netmask'] = all_netmask
            net_list.append(temp_dict)

        data = {
            'cpu_percent':cpu_percent,
            'num_cpus': psutil.cpu_count(),
            'cpu_name': cpu_name,#get_cpu_name(),
            'memory': psutil.virtual_memory(),
            'disks': get_disks(all_partitions=False),
            'cpu': psutil.cpu_times_percent(),
            'users': [u._asdict() for u in psutil.users()],
            'net_interfaces': net_list,
            'page': 'overview',
        }
        return data