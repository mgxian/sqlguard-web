#!/bin/bash

# build
docker build -t sqlguard-web .

# delete exist container
docker rm -f sqlguard-web-test && echo 'delete' || echo 'not exist'

# run
docker run --name sqlguard-web-test -d -p 5000:5000 -p 5506:5506 sqlguard-web

# log
docker logs -f sqlguard-web-test
