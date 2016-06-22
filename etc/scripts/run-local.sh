#!/bin/bash

if [ -z "$PRJ" ]; then
    export PRJ=~/vca/walle-service/walle-api-server
fi

cd $PRJ
source $PRJ/.venv/bin/activate
cd $PRJ

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
    export CFY_MANAGER_HOST=127.0.0.1
fi

if [ -z "$CFY_MANAGER_PORT" ]; then
    export CFY_MANAGER_PORT=8080
fi

echo 'run: ssh -i ~/.ssh/id_rsa_manager ubuntu@23.92.225.159 -L 8080:localhost:80 -N'
gunicorn -w ${WALLE_WORKERS} -b ${WALLE_HOST}:${WALLE_PORT} walle_api_server.cli.app:app
