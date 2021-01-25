# coding: utf-8
from tornado.web import url
from view.index.index import *
 
index_urls=[
        url(r"/", IndexHandler, name="index"),
]