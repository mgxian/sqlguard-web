#!/bin/bash

# build
docker build -t sqlguard-web .

# delete exist container
docker rm -f sqlguard-web-test && echo 'delete' || echo 'not exist'

# run
docker run --name sqlguard-web-test \
-p 5000:5000 \
-p 5506:5506 \
-e DEV_DATABASE_URL='mysql+pymysql://root:mgx123@11.11.11.111:3306/sqlguard?charset=utf8' \
-e SQL_GUARD_ADMIN='will@will.com' \
-e INCEPTION_HOST='127.0.0.1' \
-e INCEPTION_PORT=5506 \
-e MAIL_USERNAME=niupu_monitor@163.com \
-e MAIL_PASSWORD=yrtlkepdanarzaql \
-d sqlguard-web

# log
sleep 1
docker exec -ti sqlguard-web-test tail -f /code/gunicorn.log
