# coding: utf-8
 
import time
import logging
logger = logging.getLogger(__name__)
 
from util.common import *
from sqlitedict import SqliteDict
from constant import *

 
def get_task_cpu_name():
    cpu_name = get_cpu_name()
 
    mydict = SqliteDict(filename=DATABASE, tablename='monitoring', autocommit=True)
    mydict['cpu_name'] = cpu_name
    mydict.commit()
    mydict.close()
 
def get_task_percent():
    # cpu_percent = psutil.cpu_percent(interval=1)    # blocking
    cpu_percent = psutil.cpu_percent()              # non-blocking (percentage since last call)

    io_counters1 = psutil.net_io_counters(pernic=True)
    time.sleep(2)
    io_counters2 = psutil.net_io_counters(pernic=True)

    rate_dict = {}
    for index, io in enumerate(io_counters1):
        rate_dict[str(index) + '_send_rate'] = (io_counters2[io].bytes_sent -io_counters1[io].bytes_sent)/2
        rate_dict[str(index) + '_recv_rate'] = (io_counters2[io].bytes_recv -io_counters1[io].bytes_recv)/2

    mydict = SqliteDict(filename=DATABASE, tablename='monitoring', autocommit=True)
    mydict['cpu_percent'] = cpu_percent
    mydict['rate_dict'] = rate_dict
    mydict.commit()
    mydict.close()
    
def get_task_process_list():
    mydict = SqliteDict(filename=DATABASE, tablename='monitoring', autocommit=True)
    mydict.commit()
    mydict.close()
