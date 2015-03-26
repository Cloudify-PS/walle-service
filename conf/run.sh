#!/bin/bash

PRJ=/home/ubuntu/score-service

cd $PRJ
source $PRJ/venv/bin/activate
cd $PRJ/score-api-server
export CFY_HOST=192.168.240.2 
export CFY_PORT=80
$PRJ/venv/bin/gunicorn -w 4 -b 127.0.0.1:8001 score_api_server.app:app
