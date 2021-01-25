@echo off

echo *******************����Է�������ĵ�ַ*********************
echo http://127.0.0.1:8000/
echo ************************************************************
 
start  http://127.0.0.1:8000/

C:\Python36\python.exe manage.py runserver 0.0.0.0:8000
 
pause
 
windows ��Ҫע�͵�uwsgi�����ٽ��а�װ��
C:\Python36\Scripts\pip.exe install -r requirements.txt

http://127.0.0.1:8000/api/show_books
http://127.0.0.1:8000/api/add_book?book_name=test

����node.js
https://nodejs.org/zh-cn/
https://nodejs.org/zh-cn/download/releases/
https://nodejs.org/dist/latest-v8.x/