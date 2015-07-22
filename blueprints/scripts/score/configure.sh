#!/bin/bash

set -e
set -o xtrace

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

mkdir -p ~/score_logs

# Creating score.rc file with necessary options
echo -e "export SCORE_HOST=localhost
export SCORE_PORT=8001
export SCORE_WORKERS=4
export SCORE_DB=postgresql://${DB_USER}:${DB_PASS}@${DB_IP}/${DB_NAME}
export SCORE_LOGGING_FILE=~/score_logs/score-api.log
export SCORE_GUNICORN_LOGGING_FILE=~/score_logs/score_gunicorn.log
export SCORE_LOGGING_LEVEL=DEBUG
" >> ~/score.rc

rm -f ~/score_api_server.conf

echo -e "description 'score service'
# used to be: start on startup
# until we found some mounts were not ready yet while booting:
start on started mountall
stop on shutdown
# Automatically Respawn:
respawn
respawn limit 99 5
script
	export SCORE_HOST=localhost
	export SCORE_PORT=8001
	export SCORE_WORKERS=4
	export SCORE_DB=postgresql://${DB_USER}:${DB_PASS}@${DB_IP}/${DB_NAME}
	export SCORE_LOGGING_FILE=~/score_logs/score-api.log
	export SCORE_GUNICORN_LOGGING_FILE=~/score_logs/score_gunicorn.log
	export SCORE_LOGGING_LEVEL=DEBUG
	exec /usr/bin/gunicorn -w ${SCORE_WORKERS} -b ${SCORE_HOST}:${SCORE_PORT} score_api_server.cli.app:app 2>&1
end script
" >> ~/score_api_server.conf

sudo cp ~/score_api_server.conf /etc/init/score_api_server.conf
sudo chown root:root /etc/init/score_api_server.conf

source ~/score.rc; score-manage db upgrade -d score-service/score-api-server/migrations/

sudo initctl start score_api_server

# TODO(denismakogon): avoid hardcoding by downloading nginx configuration from external source

wget -c ${SCORE_NGINX_CONFIGURATION_URL} -O score-nginx-configration.tar.gz 2>&1
mkdir score-nginx-configuration
tar -xvf score-nginx-configration.tar.gz --strip 1 -C score-nginx-configration 2>&1
cd score-nginx-configuration

sudo service nginx restart
