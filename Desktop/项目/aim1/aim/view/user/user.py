# coding: utf-8
import tornado

from view.base.base import BaseHandler 
from util.function import login_required
from constant import *
     
class LoginHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render("login.html" )
 
    @tornado.gen.coroutine
    def post(self):
        password = self.get_argument('password')
        
        if password == PASSWORD:
            self.session["_terminal_"] = "_terminal_"
            self.redirect(self.reverse_url('index'))
        else:
            self.render("login.html", message="终端密码错误！")
 
class LogoutHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required
    def get(self):
        self.session["_terminal_"] = None
        self.redirect('/')
        
 