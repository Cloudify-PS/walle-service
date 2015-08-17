#!/bin/bash

set -e
set -o xtrace

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

# Logrotate file
cat > /etc/logrotate.d/score-api <<DELIM
/var/log/score-api.log {
        daily
        size 10M
        rotate 10
        missingok
        notifempty
        compress
}
DELIM

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
	export SCORE_DB=postgresql://${DB_USER}:${DB_PASS}@${DB_IP}/${DB_NAME}
	exec /usr/bin/gunicorn -w 4 -b localhost:8001 score_api_server.cli.app:app --log-level=error --error-logfile=/var/log/gunicorn_score.log
end script
" >> ~/score_api_server.conf

sudo cp ~/score_api_server.conf /etc/init/score_api_server.conf
sudo chown root:root /etc/init/score_api_server.conf

source ~/score.rc; score-manage db upgrade head -d score-service/score-api-server/migrations/
source ~/score.rc; score-manage approved-plugins add --from-file score-service/approved_plugins/approved_plugins_description.yaml

sudo initctl start score_api_server

# TODO(denismakogon): avoid hardcoding by downloading nginx configuration from external source

curl -o score-nginx-configration.tar.gz ${SCORE_NGINX_CONFIGURATION_URL} 2>&1
mkdir score-nginx-configuration
tar -xvf score-nginx-configration.tar.gz -C score-nginx-configuration 2>&1
cd score-nginx-configuration/

mv www ~/www
sudo cp etc/keys/* /etc/nginx
sudo rm -fr /etc/nginx/sites-enabled/*
sudo cp etc/nginx/vca_io /etc/nginx/sites-enabled/

sudo service nginx restart
