# coding=utf-8

import logging
logger = logging.getLogger(__name__)

from datetime import datetime, timedelta
from tornado import ioloop

from task_crontab.task import get_task_cpu_name

class TimeTask():
    def __init__(self):
        pass
    def run_test(self):
        logger.info('timing task start ....')
        ioloop.PeriodicCallback(get_task_cpu_name, 60*1000).start()  # start scheduler 每隔60s执行一次 test1

