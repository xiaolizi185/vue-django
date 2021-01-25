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
 
class NetworksHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        data = yield self.asynchronous()
        self.render('networks.html' , **data )
         
    @run_on_executor
    def asynchronous(self):
        io_counters = psutil.net_io_counters(pernic=True)
        addrs = psutil.net_if_addrs()

        mydict = SqliteDict(filename=DATABASE, tablename='monitoring', autocommit=True)
        rate_dict = mydict.get('rate_dict', {})
        mydict.close()

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

        form_keys = {
            'pid': '', 
            'family': socket_families[socket.AF_INET],
            'type': socket_types[socket.SOCK_STREAM],
            'state': 'LISTEN'
        }
 
        form_values = dict((k, self.request.arguments.get(k, default_val)) for k, default_val in form_keys.items())

        for k in ('local_addr', 'remote_addr'):
            val = self.request.arguments.get(k, '')
            if ':' in val:
                host, port = val.rsplit(':', 1)
                form_values[k + '_host'] = host
                form_values[k + '_port'] = int(port)
            elif val:
                form_values[k + '_host'] = val
 
        conns = get_connections(form_values)
        conns.sort(key=lambda x: x['state'])
 
        states = [
            'ESTABLISHED', 'SYN_SENT', 'SYN_RECV',
            'FIN_WAIT1', 'FIN_WAIT2', 'TIME_WAIT',
            'CLOSE', 'CLOSE_WAIT', 'LAST_ACK',
            'LISTEN', 'CLOSING', 'NONE'
        ]
 
        data = {
            'net_interfaces': net_list,
            'page': 'networks',
            'connections': conns,
            'socket_families': socket_families,
            'socket_types': socket_types,
            'states': states,
            'num_conns': len(conns),
 
        }
        data.update(form_values)
        # 下面这种写法不支持python2
        # self.render('networks.html', **form_values, **data )
        
        return data
 