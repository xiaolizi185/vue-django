# coding: utf-8
import os
import random
import string
import datetime

import tornado.web
import util.uimethods
import util.uimodules
from url_mapping import handlers
 
# 继承tornado.web.Application类，可以在构造函数里做站点初始化（初始数据库连接池，初始站点配置，初始异步线程池，加载站点缓存等）
class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            handlers=handlers,
            debug=False,
            autoreload=True,  # 应用程序将会观察它的源文件是否改变，并且当任何文件改变的时候便重载它自己。验证失败！
            compiled_template_cache=False,  # html修改， 立即生效
            static_hash_cache=False, # 静态文件哈希 (被 static_url 函数使用) 将不会被缓存。
            template_path="templates",
            static_path="static",
            cookie_secret=os.urandom(64),# 注释掉后， get_secure_cookie 不能用了
            # xsrf_cookies=True, # 目前开启后， api POST 调用失败，报错：'_xsrf' argument missing from POST
            ui_methods=util.uimethods,
            ui_modules=util.uimodules,
            # ui_modules={'Hello': HelloModule},
            test='whq',
            login_url='/login',
            session = {# torndsession->memory
                'driver':'memory',
                'driver_settings':{'host': self},
                'force_persistence':True,
                'sid_name':''.join(random.sample(string.ascii_lowercase, 10)), 
                # 'session_lifetime':60*60*24*5,# 单纯设置这一个， 不设置cookie_config 不会生效， 这个貌似没作用
                'cookie_config': {
                    'expires_days': 30,  # 优先级其次
                    # 'expires': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600), # 优先级最高
                },
            },
        )
        tornado.web.Application.__init__(self, **settings)
