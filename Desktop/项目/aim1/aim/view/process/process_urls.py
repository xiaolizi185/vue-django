# coding: utf-8

from tornado.web import url
from view.process.process import *
 
process_urls=[
        url(r"/process/(?P<pid>.+)/(?P<section>.+)/", ProcessHandler,name="process"),
    ]