打包：
    pyinstaller.exe -F -c PythonService.py

服务：    
    #1.安装服务
        PythonService.exe install
    #2.让服务自动启动        
        PythonService.exe --startup auto install 
    #3.启动服务
        PythonService.exe start
    #4.重启服务
        PythonService.exe restart
    #5.停止服务
        PythonService.exe stop
    #6.删除/卸载服务
        PythonService.exe remove
 