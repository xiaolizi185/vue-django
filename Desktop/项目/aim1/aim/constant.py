# coding: utf-8

HOST='127.0.0.1'
PORT='3306'
USERNAME='asimp'
PASSWORD='Star*2017'
DATABASE='my.db'
# terminal
PASSWORD='123456'

from platform import system

if system()=='Windows':
    PATH = r"C:\aim"
else:
    PATH = r"/opt/aim"
