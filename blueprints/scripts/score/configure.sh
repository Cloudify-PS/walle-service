#!/bin/bash

set -e
set -o xtrace

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

if [ "$IS_PRODUCTION" = "True" ]; then

# Report about exceeded org-ids

PATHNAME="/opt/score/bin"
FILENAME="daily_exceeded_org-id.sh"

sudo mkdir -p $PATHNAME
cat << END | sudo tee $PATHNAME/$FILENAME
#!/bin/bash

set -e
set -o xtrace

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

TMP_DIR="logrotate-\$RANDOM"
DATE=\$(date +%Y%m%d)
EMAIL_HEADER="To: vladimir_antonovich@gigaspaces.com; yoramw@gigaspaces.com
From: score.alerts@gigaspaces.com
Subject: Deployment quota exceeded.

Deployment quota exceeded for:"

mkdir /tmp/\$TMP_DIR
cd /tmp/\$TMP_DIR
cp /var/log/score-api.log /tmp/\$TMP_DIR

cat score-api.log |
grep "Deployment quota exceeded for Org-ID:" |
awk 'BEGIN { pattern="Org-ID:"}{if (match(\$21,pattern)) {str=substr(\$21,RSTART+RLENGTH);print substr(str, 0, length(str))}}' > exceeded_orgs.txt

if [ \`wc -l < exceeded_orgs.txt\` > 0 ]; then
        while IFS='' read -r line || [[ -n "\$line" ]]; do
                INFO=\$(sudo -u ubuntu -i -- bash -c "source ~/score.rc;score-manage org-ids list" | grep \$line | awk -F '|' '{print \$4}')
                awk -v info="\$INFO" '{print \$0 " - " info}' exceeded_orgs.txt >> exceeded_orgs_1.txt
        done  < "exceeded_orgs.txt"
        if [ -f exceeded_orgs_1.txt ]; then
                awk -v header="\$EMAIL_HEADER" 'NR==1{ print header}1' exceeded_orgs_1.txt > exceeded_orgs_email.txt
                msmtp -t < exceeded_orgs_email.txt
        fi
fi

cd ..
rm -fr \$TMP_DIR
END
sudo chmod 770 $PATHNAME/$FILENAME

# Send email, ~/.msmtprc - config file
cat << BODY | sudo tee /root/.msmtprc
defaults
tls on
tls_starttls on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile ~/.msmtp.log

account score.alerts@gigaspaces.com
host smtp.gmail.com
port 587
protocol smtp
auth on
from score.alerts@gigaspaces.com
user score.alerts@gigaspaces.com
passwordeval "cat ~/.msmtp.pass"
account default: score.alerts@gigaspaces.com
BODY

sudo chmod 600 /root/.msmtprc

# Save email password
sudo touch /root/.msmtp.pass
sudo chown root:root /root/.msmtp.pass
sudo chmod 600 /root/.msmtp.pass
sudo echo "LLMtSs.3t" > /root/.msmtp.pass

# Logrotate file
echo "/var/log/score-api.log {
        daily
        size 10M
        rotate 10
        missingok
        compress
        dateext
        create 644 root root
        prerotate
                /opt/score/bin/daily_exceeded_org-id.sh
        endscript
        postrotate
                sudo initctl reload score_api_server
        endscript

}" | sudo tee /etc/logrotate.d/score-api
else
	echo "Skipping reports configuration, due on staging installation."
fi

mkdir -p ~/score_logs

# Creating score.rc file with necessary options
echo -e "export SCORE_HOST=localhost
export SCORE_PORT=8001
export SCORE_WORKERS=4
export SCORE_DB=${SCORE_EXISTING_DB:=postgresql://${DB_USER}:${DB_PASS}@${DB_IP}/${DB_NAME}}
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
	export SCORE_DB=${SCORE_EXISTING_DB:=postgresql://${DB_USER}:${DB_PASS}@${DB_IP}/${DB_NAME}}
	exec /usr/bin/gunicorn -w 4 -b localhost:8001 score_api_server.cli.app:app --log-level=error --error-logfile=/var/log/gunicorn_score.log
end script
" >> ~/score_api_server.conf

sudo cp ~/score_api_server.conf /etc/init/score_api_server.conf
sudo chown root:root /etc/init/score_api_server.conf

source ~/score.rc; score-manage db upgrade head -d score-service/score-api-server/migrations/
source ~/score.rc; score-manage approved-plugins add --from-file score-service/approved_plugins/approved_plugins_description.yaml

curl -o score-nginx-configration.tar.gz ${SCORE_NGINX_CONFIGURATION_URL} 2>&1

wget -c ${SCORE_NGINX_CONFIGURATION_URL} -O score-nginx-configration.tar.gz 2>&1

mkdir score-nginx-configuration
tar -xvf score-nginx-configration.tar.gz -C score-nginx-configuration 2>&1
cd score-nginx-configuration/

mv www ~/www
sudo cp etc/keys/* /etc/nginx
sudo rm -fr /etc/nginx/sites-enabled/*
sudo cp etc/nginx/vca_io /etc/nginx/sites-enabled/

sudo service nginx restart
sudo initctl start score_api_server
