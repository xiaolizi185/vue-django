# coding: utf-8
from tornado.web import url
 
from view.docker.docker import *
 
docker_urls=[
        url(r"/docker/", DockerHandler, name="docker"),
        (r'/ws', WebSocketHandler)  
]