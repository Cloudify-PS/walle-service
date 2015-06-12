#!/bin/bash

if [ -z "$PRJ" ]; then
    export PRJ=~/score-service/score-api-server
fi

source $PRJ/.venv/bin/activate

if [ -z "$SCORE_HOST" ]; then
    export SCORE_HOST=127.0.0.1
fi

if [ -z "$SCORE_PORT" ]; then
    export SCORE_PORT=8001
fi

if [ -z "$SCORE_WORKERS" ]; then
    export SCORE_WORKERS=4
fi

if [ -z "$CFY_MANAGER_HOST" ]; then
    export CFY_MANAGER_HOST=192.168.240.5
fi

if [ -z "$CFY_MANAGER_PORT" ]; then
    export CFY_MANAGER_PORT=80
fi

gunicorn -w ${SCORE_WORKERS} -b ${SCORE_HOST}:${SCORE_PORT} score_api_server.cli.app:app
