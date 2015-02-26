#!/bin/bash

PRJ=/home/ubuntu/score-service

cd $PRJ
source $PRJ/venv/bin/activate
cd $PRJ/score-api-server
$PRJ/venv/bin/gunicorn -w 1 -b 127.0.0.1:8001 score_api_server.app:app