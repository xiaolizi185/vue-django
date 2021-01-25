# coding: utf-8

from tornado.web import url
from view.disks.disks import *
 
disks_urls=[
        url(r"/disks/", DisksHandler, name="disks"),
    ]