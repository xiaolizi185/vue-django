#coding=utf-8
from __future__ import unicode_literals

from multiprocessing import freeze_support
import threading
import os, sys
import posixpath # 不加的话调用路由时，报错
from platform import system
PY2 = sys.version_info <= (3,)

# for pyinstaller 
if hasattr(sys, "_MEIPASS"):
    # print(sys.executable)
    # print(sys._MEIPASS)
    os.chdir(sys._MEIPASS)
 
#################### 服务 ################### 
if system()=='Windows':
    import win32serviceutil   
    import win32service   
    import win32event  
    import win32timezone # 必须要有， 否则 install 服务会报错
    import servicemanager
    import winerror 
    class AIMService(win32serviceutil.ServiceFramework):   
        # 这个服务必须放在主文件， 否则无法启动服务，原因未知
        # 显示名称采用中文， python2 打包会是乱码，python3是正常的
        # install的exe路径， 必须采用绝对路径才行
        _svc_name_ = "AIM"  #服务名
        if PY2:
            _svc_display_name_ = "AIM monitoring system"  #服务在windows系统中显示的名称 Automation infrastructure management
            _svc_description_ = "AIM monitoring system" #服务的描述
        else:
            _svc_display_name_ = "AIM 监控服务"  #服务在windows系统中显示的名称 Automation infrastructure management
            _svc_description_ = "此服务为自动化基础设施管理(AIM)系统监控" #服务的描述
      
        def __init__(self, args):   
            win32serviceutil.ServiceFramework.__init__(self, args)   
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
     
        def SvcDoRun(self):  
            ''' 采用 子进程的方式'''
            t1 = threading.Thread(target=server.start )
            t1.setDaemon(True)   # 主线程结束， 子线程也会结束。 否则主线程结束后， 会一直等待子线程
            t1.start() 
      
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE) #只有停止的时候才会执行 
     
        def SvcStop(self):   
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)   
            win32event.SetEvent(self.hWaitStop)  
# else:
    # centos6 还需要这个代码， 需要研究
    # centos7 采用daemon 是可以的
    # 或者 centos6 采用 《daemon /usr/bin/aim &》 这种方式也可以
    # from utils import daemonize
#################### web服务 ################### 

import logging
logger = logging.getLogger(__name__)
from util import log_config
log_config.init( )  # 必须放在app初始化的前面， 否则别的模块识别不到

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from application import Application
# from task_crontab.time_task import TimeTask # 初始化定时任务
import task_crontab.time_task2                # apscheduler
 
from tornado.options import define, options
define("port", default=12133, help="run on the given port", type=int)

from task_crontab.task import get_task_cpu_name
    
 
if __name__=='__main__':  
    freeze_support()
    tornado.options.parse_command_line()

    tornado_app = Application()     
    http_server = tornado.httpserver.HTTPServer(
        request_callback=tornado_app,
        xheaders=True,# 采用反向代理时，获取正确的ip，nginx里面也需要设置。此功能暂未验证。
        max_buffer_size=6 * 1024 * 1024 * 1024,   #6G Size file upload, default 100M
        # ssl_options={
           # "certfile": '/etc/letsencrypt/archive/haiqing.wang/cert1.pem'),
           # "keyfile": '/etc/letsencrypt/archive/haiqing.wang/privkey1.pem'),
        # },
    )
    http_server.listen(options.port)  
 
    get_task_cpu_name()
 
    server = tornado.ioloop.IOLoop.instance()
    print('service start running on 0.0.0.0:{0}'.format(options.port))
    
    try:
        import webbrowser
        url = "http://127.0.0.1:12133/"
        server.add_callback(webbrowser.open, url)
    except:
        pass
        
    # task_instance = TimeTask()
    # task_instance.run_test()
 
    if hasattr(sys, "frozen"):
        if system()=='Windows':
            if len(sys.argv) == 1:
                try:
                    evtsrc_dll = os.path.abspath(servicemanager.__file__)
                    servicemanager.PrepareToHostSingle(AIMService)
                    servicemanager.Initialize('AIMService', evtsrc_dll)
                    servicemanager.StartServiceCtrlDispatcher()
                    # 执行服务， 貌似会走这里
                except win32service.error as details:
                    server.start()# 双击exe，会执行这里
            else:
                win32serviceutil.HandleCommandLine(AIMService) # 注册服务，操作服务，会执行这里
        else:
            # if len(sys.argv) != 1:
                # daemonize( )
            server.start()
    else:
        server.start()# Linux和Python源代码，执行这里
 