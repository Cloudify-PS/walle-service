#!/bin/bash

if [ -z "$PRJ" ]; then
    export PRJ=~/score-service
fi

cd $PRJ
source $PRJ/venv/bin/activate
cd $PRJ/score-api-server
if [ -z "$CFY_HOST" ]; then
    export CFY_HOST=192.168.240.2
fi    
if [ -z "$CFY_PORT" ]; then
    export CFY_PORT=80
fi
$PRJ/venv/bin/gunicorn -w 4 -b 127.0.0.1:8001 score_api_server.app:app
