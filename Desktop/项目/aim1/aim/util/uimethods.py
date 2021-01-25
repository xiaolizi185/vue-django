# coding: utf-8
import os
import json
import time
import sys
import socket
import platform
import requests
import psutil
from platform import system
from datetime import datetime, timedelta
import datetime 
from util.common import *
from util.temperature_reader import *
 
def hostname(self):
    my_hostname = socket.gethostname()
    return my_hostname
    
def os(self):
    if system() == 'Windows':
        my_os = platform.platform() 
    elif system() == 'Linux':
        my_os = '-'.join(platform.linux_distribution())
    elif system() == 'Darwin':
        mac_ver = platform.mac_ver()[0]
        if mac_ver.startswith('10.14'):
            my_os = 'Mojave-'+platform.mac_ver()[0]
        elif mac_ver.startswith('10.13'):
            my_os = 'High Sierra-'+platform.mac_ver()[0]
        elif mac_ver.startswith('10.12'):
            my_os = 'Sierra-'+platform.mac_ver()[0]
        elif mac_ver.startswith('10.11'):
            my_os = 'El Capitan-'+platform.mac_ver()[0]
    return my_os
    
def uptime(self):
    delta = int(time.time() - psutil.boot_time())
    uptime = timedelta(seconds=delta)
    my_uptime = str(uptime).split('.')[0]
    return my_uptime

def filesizeformat(self, size):
    return bytes2human(size)
    
def fromtimestamp(self, timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
  
def truncate(self, str, length):
    if len(str) > length:
        return str[0:length]+' ...'
    else:
        return str[0:length]
        
def show_float(self, data, length):
    return round(data, length)
    
def get_cpu_temperature(self):
    if system() == 'Windows':
        temperature = WindowsCpuTemperatureReader.get_reader()
    else:
        temperature = LinuxCpuTemperatureReader.get_reader()
        
    if temperature:
        return temperature()

 