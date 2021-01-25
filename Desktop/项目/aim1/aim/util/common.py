#coding=utf-8

import socket
import uuid
import os
import psutil
from platform import system
from sqlitedict import SqliteDict

if system() == 'Windows':
    import wmi
    import pythoncom

from constant import *

import logging
logger = logging.getLogger(__name__)

def get_cpu_name():
    cpu_name = '---'
    if system() == 'Windows':
        pythoncom.CoInitialize()
        c = wmi.WMI ()
        for processor in c.Win32_Processor():
            cpu_name = processor.Name.strip()
            break
    elif system() == 'Linux':
        cmd = "grep 'model name' /proc/cpuinfo |uniq |awk -F : '{print $2}' "
        cpu_name = os.popen(cmd).read().strip()
    elif system() == 'Darwin':
        cmd = "sysctl -n machdep.cpu.brand_string"
        cpu_name = os.popen(cmd).read().strip()
    
    return cpu_name
 
def bytes2human(n): 
    value = ''
    if 1024>n:
        value = '%.2f B' %n
    elif 1024>n/1024:
        value = '%.2f KB' %(n/1024) 
    elif 1024>n/1024/1024:
        value = '%.2f MB' %(n/1024/1024) 
    elif 1024>n/1024/1024/1024:
        value = '%.2f GB' %(n/1024/1024/1024) 
    elif 1024>n/1024/1024/1024/1024:
        value = '%.2f TB' %(n/1024/1024/1024/1024) 
    elif 1024>n/1024/1024/1024/1024/1024:
        value = '%.2f PB' %(n/1024/1024/1024/1024/1024) 
    return value.replace('.00','')
 
def get_process_list():
    process_list = []
    for p in psutil.process_iter():
        mem = p.memory_info()
        
        # psutil throws a KeyError when the uid of a process is not associated with an user.
        try:
            username = p.username()
        except Exception as e:
            username = ''
            
        try:
            cmdline = ' '.join(p.cmdline())
        except Exception as e:
            cmdline = ''
            
        proc = {
            'pid': p.pid,
            'name': p.name(),
            'cmdline': cmdline,#'' '.join(p.cmdline()),
            'user': username,
            'status': p.status(),
            'created': p.create_time(),
            'mem_rss': mem.rss,
            'mem_vms': mem.vms,
            'mem_percent': p.memory_percent(),
            'cpu_percent': p.cpu_percent(0)
        }
        process_list.append(proc)

    return process_list
    
def get_disks(all_partitions=True):
    disks = []
    for dp in psutil.disk_partitions(all_partitions):
        usage = psutil.disk_usage(dp.mountpoint)
        disk = {
            'device': dp.device,
            'mountpoint': dp.mountpoint,
            'type': dp.fstype,
            'options': dp.opts,
            'space_total': usage.total,
            'space_used': usage.used,
            'space_used_percent': usage.percent,
            'space_free': usage.free
        }
        disks.append(disk)

    return disks
    
def get_disks_counters(perdisk=True):
    # return dict((dev, c._asdict()) for dev, c in psutil.disk_io_counters(perdisk=perdisk).iteritems())
    return dict((dev, c._asdict()) for dev, c in psutil.disk_io_counters(perdisk=perdisk).items())
    
def get_net_ip_and_netmask(addrs, name):
    all_ip = []
    all_netmask = []
    for addr in addrs:
        if addr==name:
            for i in addrs[addr]:
                if i[1] and '.' in i[1]:
                    all_ip.append(i[1])
                if i[2] and '.' in i[2]:
                    all_netmask.append(i[2])
            break
    return ' '.join(all_ip), ' '.join(all_netmask)
 
def socket_constants(prefix):
    return dict((getattr(socket, n), n) for n in dir(socket) if n.startswith(prefix))


socket_families = socket_constants('AF_')
socket_types = socket_constants('SOCK_')

def get_process_name(process_list, pid):
    for process in process_list:
        if process['pid'] == pid:
            return process['name']
    return '检测中 '
    
def get_connections(filters=None):
    filters = filters or {}
    connections = []

    all =  psutil.net_connections('all')
    for c in all:
        try:
            p = psutil.Process(c.pid)
        except:
            continue
        conn = {
            'fd': c.fd,
            'pid': c.pid,
            'family': socket_families[c.family],
            'type': socket_types[c.type],
            'local_addr_host': c.laddr[0] if c.laddr else None,
            'local_addr_port': c.laddr[1] if c.laddr else None,
            'remote_addr_host': c.raddr[0] if c.raddr else None,
            'remote_addr_port': c.raddr[1] if c.raddr else None,
            'state': c.status,
            'process_name':  p.name(),
        }

        for k, v in filters.items():
            if v and conn.get(k) != v:
                break
        else:
            connections.append(conn)
    return connections
    
def get_process(pid):
    p = psutil.Process(pid)
    mem = p.memory_info_ex()
    cpu_times = p.cpu_times()

    # psutil throws a KeyError when the uid of a process is not associated with an user.
    try:
        username = p.username()
    except Exception as e:
        username = ''

    attr = dir(p)
    
    try:
        cmdline = ' '.join(p.cmdline())
    except Exception as e:
        cmdline = ''
        
    try:
        cwd = p.cwd()
    except Exception as e:
        cwd = '' 

    try:
        nice = ' '.join(p.nice())
    except Exception as e:
        nice = '' 

    try:
        io_nice_class = p.ionice()[0]
        io_nice_value = p.ionice()[1]
    except Exception as e:
        io_nice_class = ''
        io_nice_value = ''
    
    try:
        open_files = p.open_files()
    except Exception as e:
        open_files = []
    
    try:
        cpu_affinity = p.cpu_affinity()
    except Exception as e:
        cpu_affinity = []
    
    return {
        'pid': p.pid,
        'ppid': p.ppid(),
        'parent_name': p.parent().name() if p.parent() else '',
        'name': p.name(),
        'cmdline': cmdline,
        'user': username,

        'uid_real': p.uids().real if 'uids' in attr else 0,
        'uid_effective': p.uids().effective if 'uids' in attr else 0,
        'uid_saved': p.uids().saved if 'uids' in attr else 0,

        'gid_real': p.gids().real if 'gids' in attr else 0,
        'gid_effective': p.gids().effective if 'gids' in attr else 0,
        'gid_saved': p.gids().saved if 'gids' in attr else 0,
        'status': p.status(),
        'created': p.create_time(),
        'terminal': p.terminal() if 'terminal' in attr else '',
        'mem_rss': mem.rss,
        'mem_vms': mem.vms,
        'mem_shared': p.shared if 'shared' in attr else 0,
        'mem_text': p.text if 'text' in attr else 0,
        'mem_lib': p.lib if 'lib' in attr else 0,
        'mem_data': p.data if 'data' in attr else 0,
        'mem_dirty': p.dirty if 'dirty' in attr else 0,
        'mem_percent': p.memory_percent(),
        'cwd': cwd,
        'nice': nice,
        'io_nice_class': io_nice_class,
        'io_nice_value': io_nice_value,
        'cpu_percent': p.cpu_percent(0),
        'num_threads': p.num_threads(),
        'num_files': len(open_files),
        'num_children': len(p.children()),
        'num_ctx_switches_invol': p.num_ctx_switches().involuntary,
        'num_ctx_switches_vol': p.num_ctx_switches().voluntary,
        'cpu_times_user': cpu_times.user,
        'cpu_times_system': cpu_times.system,
        'cpu_affinity': cpu_affinity
    }
    
def get_process_environment(pid):
    with open('/proc/%d/environ' % pid) as f:
        contents = f.read()
        env_vars = dict(row.split('=', 1) for row in contents.split('\0') if '=' in row)
    return env_vars
    
def get_process_threads(pid):
    threads = []
    proc = psutil.Process(pid)
    for t in proc.threads():
        thread = {
            'id': t.id,
            'cpu_time_user': t.user_time,
            'cpu_time_system': t.system_time,
        }
        threads.append(thread)
 
    return threads
    
def get_process_open_files(pid):
    proc = psutil.Process(pid)
    try:
        return [f._asdict() for f in proc.open_files()]
    except:
        return []
    
def get_process_connections(pid):
    proc = psutil.Process(pid)
    connections = []
    for c in proc.connections(kind='all'):
        conn = {
            'fd': c.fd,
            'family': socket_families[c.family],
            'type': socket_types[c.type],
            'local_addr_host': c.laddr[0] if c.laddr else None,
            'local_addr_port': c.laddr[1] if c.laddr else None,
            'remote_addr_host': c.raddr[0] if c.raddr else None,
            'remote_addr_port': c.raddr[1] if c.raddr else None,
            'state': c.status
        }
        connections.append(conn)

    return connections
    
def get_process_memory_maps(pid):
    return [m._asdict() for m in psutil.Process(pid).memory_maps()]

def get_process_children(pid):
    proc = psutil.Process(pid)
    children = []
    for c in proc.children():
        child = {
            'pid': c.pid,
            'name': c.name(),
            'cmdline': ' '.join(c.cmdline()),
            'status': c.status()
        }
        children.append(child)

    return children
    
def get_process_limits(pid):
    p = psutil.Process(pid)
    return {
        'RLIMIT_AS': p.rlimit(psutil.RLIMIT_AS),
        'RLIMIT_CORE': p.rlimit(psutil.RLIMIT_CORE),
        'RLIMIT_CPU': p.rlimit(psutil.RLIMIT_CPU),
        'RLIMIT_DATA': p.rlimit(psutil.RLIMIT_DATA),
        'RLIMIT_FSIZE': p.rlimit(psutil.RLIMIT_FSIZE),
        'RLIMIT_LOCKS': p.rlimit(psutil.RLIMIT_LOCKS),
        'RLIMIT_MEMLOCK': p.rlimit(psutil.RLIMIT_MEMLOCK),
        'RLIMIT_MSGQUEUE': p.rlimit(psutil.RLIMIT_MSGQUEUE),
        'RLIMIT_NICE': p.rlimit(psutil.RLIMIT_NICE),
        'RLIMIT_NOFILE': p.rlimit(psutil.RLIMIT_NOFILE),
        'RLIMIT_NPROC': p.rlimit(psutil.RLIMIT_NPROC),
        'RLIMIT_RSS': p.rlimit(psutil.RLIMIT_RSS),
        'RLIMIT_RTPRIO': p.rlimit(psutil.RLIMIT_RTPRIO),
        'RLIMIT_RTTIME': p.rlimit(psutil.RLIMIT_RTTIME),
        'RLIMIT_SIGPENDING': p.rlimit(psutil.RLIMIT_SIGPENDING),
        'RLIMIT_STACK': p.rlimit(psutil.RLIMIT_STACK)
    }