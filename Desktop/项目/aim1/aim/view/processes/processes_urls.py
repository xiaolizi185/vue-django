# coding: utf-8

from tornado.web import url
from view.processes.processes import *
 
processes_urls=[
        url(r"/processes/", ProcessesHandler, name="main-processes"),
        url(r"/processes/(?P<sort>.+)/(?P<order>.+)/", ProcessesHandler,name="processes"),
 
    ]