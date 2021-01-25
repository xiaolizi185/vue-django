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
import tornado.websocket
import threading
import logging
import requests
import traceback
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

class MyThread(threading.Thread):  
    def __init__(self,id,channel):  
        threading.Thread.__init__(self)  
        self.channel=channel
        self._running = True
        
    def terminate(self):
        self._running = False
        
    def run(self):  
        while self._running:    
            try:
                data = self.channel.sock.recv(512)
                if not data:
                    break
 
                data_json={"data":data.decode()}
                self.channel.write_message(json.dumps(data_json))
            except Exception as ex:
                break
        self.channel.sock.close()
        return False

##获取容器执行ID
def connect_containers(host,port,containers_id):
    headers={
        "Content-Type":"application/json"
    }
    data=json.dumps({
      "AttachStdin": True,
      "AttachStdout": True,
      "AttachStderr": True,
      "Cmd": ["/bin/bash"],
      "Privileged": True,
      "Tty": True
    })
    status={"status":True,"response":""}
    try:
        url='http://%s:%s/containers/%s/exec'%(host,str(port),containers_id)
        result=requests.post(url, data=data,headers=headers)
        result_obj=result.text.replace("\n","")
        result_json=json.loads(result_obj)
        id=result_json["Id"]
        status.update({"response":id})
    except Exception as ex:
        response=u'%s 获取容器任务ID失败,请检查主机/端口/容器ID是否正确...'%(str(ex))
        status.update({"status":False,"response":response})
    return status
    
##重置容器窗口大小
def resize_containers(host,port,containers_id,width,height):
    headers={
        "Content-Type":"text/plain",
    }
    try:
        url='http://%s:%s/exec/%s/resize?h=%s&w=%s'%(host,str(port),containers_id,width,height)
        result=requests.post(url,data={},headers=headers)
    except Exception as ex:
        print(ex)
    
class DockerHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required
    def get(self):
        data = {
            'page': 'docker',
            'containers': self.get_containers(),
        }
        return self.render("docker.html", **data)
        
    def get_containers(self):
        if system() == "Windows":
            return []
        try:
            r = requests.get('http://127.0.0.1:2375/containers/json', timeout=1)
            containers = r.json()
        except Exception as e:
            containers = []
        return containers
        
class WebSocketHandler(tornado.websocket.WebSocketHandler):  
    def check_origin(self, origin):  
        return True  

    def open(self):
        status={"status":True,"response":""}
        try:
            ##获取参数
            args=self.request.arguments
            host=args["h"][0].decode()
            port=int(args["p"][0])
            containers_id=args["containers_id"][0].decode()
            rows=args["rows"][0]
            cols=args["cols"][0]
            ##获取容器ID
            connect_json=connect_containers(host,port,containers_id)
            id=connect_json["response"]

            if connect_json["status"]:
                ##成功
                response=connect_json["response"]
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((host, port))
                param_data = '{"Tty":true}'
                # param_data = '{"Detach":false, "Tty":false}'
                param_lenth = len(param_data)
                str="""POST /exec/{id}/start HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {param_lenth}\r\n\r\n{param_data}""".format(
                    id=response,
                    host=host,
                    port=port,
                    param_lenth=param_lenth,
                    param_data=param_data,
                )
 
                self.sock.send(str.encode())
 
                resize_containers(host,port,id,rows,cols)
                self.t=MyThread(999,self)
                self.t.setDaemon(True)
                self.t.start() 
            else:
                ##失败
                response=connect_json["response"]
                status.update({"status":False,"data":response})
                self.write_message(status)
        except Exception as ex:
            exstr = traceback.format_exc()
            response="%s 联接容器失败..."%(exstr)
            status.update({"status":False,"data":response})
            self.write_message(status)

    def on_message(self, message):  
        try:
            self.sock.send(message.encode("utf8"))
        except Exception as ex:
            print(ex)  
        
    def on_close(self):  
        try:
            # data_json=json.dumps({"data":"connect close , pleace refesh the window..."})         
            # self.write_message(data_json)
            self.sock.close()
            self.t.terminate()
        except:
            exstr = traceback.format_exc()
            print(exstr)