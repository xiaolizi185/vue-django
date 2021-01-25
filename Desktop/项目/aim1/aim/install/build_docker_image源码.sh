cat >  ./Dockerfile << EOF
FROM alpine
MAINTAINER whq <krman@163.com>

RUN apk add --update bash py3-tornado py3-psutil --repository http://mirrors.ustc.edu.cn/alpine/v3.7/main/ --allow-untrusted
RUN rm -rf /var/cache/apk/* 
COPY ./aim  /aim
WORKDIR /aim

RUN pip3 install sqlitedict apscheduler terminado
EXPOSE 12133
CMD python3 aim.py
EOF

rm -rf aim-latest.tar

docker rm -f $(docker ps -a -q)
docker rmi aim  

docker build -t aim   .
docker images
docker run -itd  --restart=always  -p 12133:12133 aim
docker save -o aim-latest.tar aim:latest
