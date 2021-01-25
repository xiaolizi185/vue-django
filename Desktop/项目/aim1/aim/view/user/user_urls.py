# coding: utf-8
from __future__ import unicode_literals
from tornado.web import url
from view.user.user import *
 
user_urls=[
        url(r"/login/", LoginHandler, name="login"),
        url(r"/logout/", LogoutHandler, name="logout"),
    ]