#!/bin/bash

if [ -z "$PRJ" ]; then
    export PRJ=~/walle-service/walle-api-server
fi

source $PRJ/.venv/bin/activate

if [ -z "$WALLE_HOST" ]; then
    export WALLE_HOST=127.0.0.1
fi

if [ -z "$WALLE_PORT" ]; then
    export WALLE_PORT=8001
fi

if [ -z "$WALLE_WORKERS" ]; then
    export WALLE_WORKERS=4
fi

if [ -z "$CFY_MANAGER_HOST" ]; then
    export CFY_MANAGER_HOST=192.168.240.5
fi

if [ -z "$CFY_MANAGER_PORT" ]; then
    export CFY_MANAGER_PORT=80
fi

gunicorn -w ${WALLE_WORKERS} -b ${WALLE_HOST}:${WALLE_PORT} walle_api_server.cli.app:app
