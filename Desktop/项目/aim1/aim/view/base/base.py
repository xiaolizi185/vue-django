# coding: utf-8
import logging
logger = logging.getLogger(__name__)

import tornado.web
import tornado.websocket
from tornado import gen
from tornado.web import RequestHandler, Finish 
from concurrent.futures import ThreadPoolExecutor

import torndsession 
from torndsession.sessionhandler import SessionBaseHandler
from torndsession import memorysession
# from torndsession import redissession  
 
class BaseHandler(SessionBaseHandler):
    # 这个并发库在python3自带;在python2需要安装sudo pip install futures
    executor = ThreadPoolExecutor(max_workers=10)

    def get_current_user(self):
        current_user = self.session.get("_terminal_", None)
        return current_user

    def initialize(self):
        self.request.headers['X-Xsrftoken'] = tornado.escape.to_unicode(self.xsrf_token)
 
    @gen.coroutine
    def prepare(self):
        pass
 
    @gen.coroutine
    def on_finish(self):
        pass
            
    def write_error(self, status_code, **kwargs):
        if status_code == 403:
            self.render("403.html")
        elif status_code == 404 or 405:
            self.render("404.html")
        elif status_code == 500:
            self.render("500.html")
            
    def write_json(self, data, status_code=200, message='success.'):
        data = json.dumps(
            {
                'code': status_code,
                'message': message,
                'data': data
            }
        )
        self.finish(data)

    def write_success(self, data={}, message=''):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write({"status": True, "data": data, "message": message})
        raise Finish  # 确保后面的代码不会执行

    def write_fail(self, data={}, message=''):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write({"status": False, "data": data, "message": message})
        raise Finish  # 确保后面的代码不会执行
            
class JsonHandler(BaseHandler):
    def initialize(self):
        # print(self.xsrf_token)  # 添加了 token POST 也不行， 需要再研究一下
        # self.set_header('X-XSRFTOKEN',self.xsrf_token)
        # self.set_header('_xsrf',self.xsrf_token)

        # 采用下面的方法， python2可以， python3不可以， 一样的版本  '_xsrf' argument has invalid format
        # 不加的话， 报错：'_xsrf' argument missing from POST
        self.request.headers['X-Xsrftoken'] = self.xsrf_token
 
    def write_json(self, object):
        object = tornado.escape.json_encode(object)
        # object = tornado.escape.json_encode(object).decode('unicode_escape')
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(object)
        raise Finish  # 确保后面的代码不会执行

    def write_success(self, data={}, message=''):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write({"status": True, "data": data, "message": message})
        raise Finish  # 确保后面的代码不会执行

    def write_fail(self, data={}, message=''):
        """ 抛出结束异常来确保代码不会继续执行 """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write({"status": False, "data": data, "message": message})
        raise Finish  # 确保后面的代码不会执行
 