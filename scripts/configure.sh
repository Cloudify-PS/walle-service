#!/bin/sh
export WALLE_HOST="0.0.0.0"
export WALLE_PORT="5000"
export WALLE_WORKERS="4"
export WALLE_DB="sqlite:////tmp/walle-service.db"
export WALLE_LOGGING_LEVEL=INFO
export WALLE_LOGGING_FILE="/tmp/walle.api"
