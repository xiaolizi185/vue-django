#!/bin/bash
set -x
 
sed -n -e '1,/^exit 0$/!p' $0 > "packages.tar.gz" 2>/dev/null

rm -rf packages
mkdir packages
tar xzf packages.tar.gz -C packages/

if grep -q "6\." /etc/redhat-release;then
    service aim stop 
    chkconfig aim off
elif grep -q "7\." /etc/redhat-release;then
    systemctl stop aim  
    systemctl disable aim 
    # docker stop aim
fi
rm -rf /opt/aim-tool/
 
cp -r packages/dist/aim    /opt/aim-tool
 
if grep -q "6\." /etc/redhat-release;then
    cp -rf packages/aim    /etc/rc.d/init.d/
    chmod 755 -R /etc/rc.d/init.d/aim
    
    chkconfig aim on
    service aim start 
    service aim status 
elif grep -q "7\." /etc/redhat-release;then
    cp -rf packages/aim.service /usr/lib/systemd/system/
    chmod 755 -R /usr/lib/systemd/system/aim.service
    
    systemctl daemon-reload
    systemctl enable aim
    systemctl start  aim    
    systemctl status aim  
fi
 
rm -rf packages.tar.gz
rm -rf packages/
 
# exit 0 下面必须有一个空行， 而且不能有任何内容
exit 0
