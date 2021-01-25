#!/bin/bash

rm -rf /opt/python3

# 没有会报错 zipimport.ZipImportError: can't decompress data; zlib not available
yum -y install zlib* 
yum -y install sqlite-devel  # 解决 sqlachemy sqlite 报错的问题：ModuleNotFoundError: No module named 'pysqlite2'
# yum -y install python-devel  # 暂时无用
yum -y install openssl-devel # 不安装的话， https加密会报错 AssertionError: Python 2.6+ and OpenSSL required for SSL
# yum -y install bzip2-devel   # 不安装的话， matplotlib 报错 ModuleNotFoundError: No module named '_bz2'
# yum -y install tk-devel      # 不安装的话， matplotlib 报错 ModuleNotFoundError: No module named '_tkinter'
# yum -y install tkinter       # 安装完tk之后， 尽管不调用这个库， 打包之后的文件也会大3M   
yum -y install gcc           # 以前不会，不知道什么情况出现报错 configure: error: no acceptable C compiler found in $PATH  

rm -rf Python-3.6.6.tgz
wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz
# wget http://172.19.105.177:2133/job/aim/Python-3.6.6.tgz

tar -xzf Python-3.6.6.tgz 

cd Python-3.6.6
# --prefix选项是配置安装的路径，如果不配置该选项，安装后可执行文件默认放在/usr/local/bin，
# 库文件默认放在/usr/local/lib，配置文件默认放在/usr/local/etc，其它的资源文件放在/usr/local/share，比较凌乱.

# 不加 --enable-shared ， 编译不会报错。ldd里面还没有libpython3.6m.so.1.0关联信息。但是打包会报错。
# 安装多个python27的版本，如果不开启enable-shared，指定不同路径即可。
# 当开启enable-shared时，默认只有一个版本的python

# --enable-optimizations 是优化选项（LTO,PGO 等）加上这个 flag 编译后，性能有 10% 左右的优化,但是这会明显的增加编译时间,老久了. 
./configure --prefix=/opt/python3  --enable-shared  

make && make install
cd ..

# 不加下面变量的话，打包会失败 libpython3.6m.so.1.0 => not found
# /opt/python3/bin/python3.6: error while loading shared libraries: libpython3.6m.so.1.0: cannot open shared object

# echo export LD_LIBRARY_PATH=/opt/python3/lib >> /root/.bashrc
# source /root/.bashrc

echo /opt/python3/lib > /etc/ld.so.conf.d/python3.conf
ldconfig

# ldd查看关联的库
ldd /opt/python3/bin/python3  

# 安装常用的库
# export LD_LIBRARY_PATH=/opt/python3/lib 
/opt/python3/bin/pip3 install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple/
/opt/python3/bin/pip3 install -r ../requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 删除软连接
rm -rf /usr/bin/python3 
rm -rf /usr/bin/pip3
rm -rf /usr/bin/pyinstaller3
# 创建软连接
ln -s /opt/python3/bin/python3 /usr/bin/python3
ln -s /opt/python3/bin/pip3 /usr/bin/pip3
ln -s /opt/python3/bin/pyinstaller /usr/bin/pyinstaller3

 









