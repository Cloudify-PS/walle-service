#!/bin/bash

if [ -z "$PRJ" ]; then
    export PRJ=~/score-service/score-api-server
fi

cd $PRJ
source $PRJ/.venv/bin/activate
cd $PRJ/score-api-server

if [ -z "$SCORE_HOST" ]; them
    export SCORE_HOST=0.0.0.0
fi

if [ -z "$SCORE_PORT" ]; them
    export SCORE_PORT=5000
fi

if [ -z "$SCORE_WORKERS" ]; them
    export SCORE_WORKERS=4
fi

if [ -z "$CFY_MANAGER_HOST" ]; them
    export CFY_MANAGER_HOST=127.0.0.1
fi

if [ -z "$CFY_MANAGER_PORT" ]; them
    export CFY_MANAGER_PORT=80
fi

gunicorn -w ${SCORE_WORKERS} -b ${SCORE_HOST}:${SCORE_PORT} score_api_server.cli.app:app
