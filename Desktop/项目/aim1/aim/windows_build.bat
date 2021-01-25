rd /s /q dist                       2> nul 1> nul
rd /s /q build                      2> nul 1> nul
 
REM C:\miniconda3\Scripts\pyinstaller.exe --clean -F  --add-data static;static --add-data templates;templates    -i k_window.ico aim.py  --additional-hooks-dir=.
D:\workspace\Python36\Scripts\pyinstaller.exe --clean -F  --add-data static;static --add-data templates;templates    -i k_window.ico aim.py  --additional-hooks-dir=.
REM C:\miniconda3\Scripts\pyinstaller.exe  aim.spec
REM C:\miniconda3\Scripts\pyinstaller.exe  aimu.spec
 
REM rd /s /q dist                       2> nul 1> nul
rd /s /q build                      2> nul 1> nul
 
pause
exit
 