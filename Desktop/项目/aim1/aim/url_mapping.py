# coding: utf8
import re

from tornado.web import url, StaticFileHandler
 
from view.index.index_urls import index_urls
from view.processes.processes_urls import processes_urls
from view.process.process_urls import process_urls
from view.disks.disks_urls import disks_urls
from view.networks.networks_urls import networks_urls
# from view.api.api_urls import api_urls
# from view.terminal.terminal_urls import terminal_urls
# from view.user.user_urls import user_urls
# from view.docker.docker_urls import docker_urls

from constant import *

handlers=[
        
        # (r"/user/(?P<name>.+)", UserHandler),
         
        # (r"/share/(.*)", StaticFileHandler, {"path": r"C:/Users/root/Desktop/www/"}), #这种方式只能实现单个目录
        (re.escape('/share/') + r"(.*)", StaticFileHandler, {"path": PATH}),
        # http://127.0.0.1:8000/share/abc/2.txt  也可以访问
        # tornado实现文件服务器  C:\Python27\Lib\site-packages\tornado\web.py
    ]
    
handlers += index_urls
handlers += processes_urls
handlers += process_urls
handlers += disks_urls
handlers += networks_urls
# handlers += api_urls
# handlers += terminal_urls
# handlers += user_urls
# handlers += docker_urls
