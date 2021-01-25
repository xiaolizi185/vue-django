#!/bin/bash

rm -rf build/
rm -rf dist/
pyinstaller3  --clean aim.py --add-data static:static --add-data templates:templates  --additional-hooks-dir=. 
rm -rf build/


rm -rf packages.tar.gz
 
tar zcvf packages.tar.gz aim aim.service dist/aim/ 

cat linux_install.sh packages.tar.gz > aim-tool.sh

chmod +x aim-tool.sh

rm -rf packages.tar.gz

bash aim-tool.sh
