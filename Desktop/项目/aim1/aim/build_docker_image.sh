cat >  ./Dockerfile << EOF
FROM frolvlad/alpine-glibc
MAINTAINER whq <krman@163.com>

RUN apk add --update bash --repository http://mirrors.ustc.edu.cn/alpine/v3.7/main/ --allow-untrusted
RUN rm -rf /var/cache/apk/* 
COPY ./dist/aim  /aim
COPY ./static/  /aim/static
COPY ./templates/  /aim/templates
WORKDIR /aim
 
EXPOSE 12133
CMD /aim/aim
EOF

rm -rf build/
rm -rf dist/
pyinstaller3  --clean aim.py  --additional-hooks-dir=. 
rm -rf build/

rm -rf aim-latest.tar
 
systemctl stop aim  
systemctl disable aim 
docker stop aim
docker rm -f aim
docker rmi aim:latest
 
docker build -t aim   .
docker images
docker save -o aim-latest.tar aim:latest

docker tag aim:latest index.tenxcloud.com/krman/aim:latest
docker push index.tenxcloud.com/krman/aim:latest
if [ $? -eq 0 ]; then
    echo -e "\033[42;37;5m镜像推送成功\033[0m"
else
    echo -e "\033[41;37;5m镜像推送失败\033[0m"
fi

docker run -itd  --restart=always --name aim --net=host index.tenxcloud.com/krman/aim:latest
 