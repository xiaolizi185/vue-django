# coding=utf-8

import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.triggers.interval import IntervalTrigger
 
from task_crontab.task import get_task_percent

logger = logging.getLogger(__name__)


class TimeTask(object):
    def __init__(self):
        self.scheduler = TornadoScheduler()
        self.scheduler.add_jobstore(MemoryJobStore(), 'default')

    def add_time_task(self, id, func,seconds, *args, **kwargs):
        self.scheduler.add_job(
                            func=func,
                            id=id,
                            trigger=IntervalTrigger(
                                                    weeks=0,
                                                    days=0,
                                                    hours=0,
                                                    minutes=0,
                                                    seconds=seconds,
                                                    start_date=datetime.now()+timedelta(seconds=0),
                                                    end_date=datetime.now()+timedelta(seconds=31536000),
                                                    ),
                            replace_existing=True,
                            args=args, 
                            kwargs=kwargs,
                            max_instances=1,
                     )                         
        return self

    def start_tasks(self):
        self.scheduler.start()

    def get_jobs(self):
        return self.scheduler.get_jobs()

        
timetask = TimeTask()
timetask.add_time_task(id='get_task_percent',
                      func=get_task_percent,
                      seconds=30,
                      )
timetask.start_tasks()

