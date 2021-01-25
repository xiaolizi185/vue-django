# -*- mode: python -*-

block_cipher = None
import os

a = Analysis(['aimu.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[
                    (r"static","static"),
                    (r"templates","templates"),
                    
                    #(r"C:\Users\root\Desktop\tornado\static","static"),
                    #(r"C:\Users\root\Desktop\tornado\templates","templates"),
             ],
             hiddenimports=[],
             hookspath=['.'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
 
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='aimu',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='k_window.ico')
