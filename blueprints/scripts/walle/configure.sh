#!/bin/bash
set -e
set -o xtrace

cd $HOME

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

if [ x"$IS_PRODUCTION" != x"false" ]; then

ctx logger info "Prodaction mode."
# Report about exceeded org-ids

PATHNAME="/opt/walle/bin"
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
From: walle.alerts@gigaspaces.com
Subject: Deployment quota exceeded.

Deployment quota exceeded for:"

mkdir -p /tmp/\$TMP_DIR
cd /tmp/\$TMP_DIR
cp /var/log/walle-api.log /tmp/\$TMP_DIR

cat walle-api.log |
grep "Deployment quota exceeded for Org-ID:" |
awk 'BEGIN { pattern="Org-ID:"}{if (match(\$21,pattern)) {str=substr(\$21,RSTART+RLENGTH);print substr(str, 0, length(str))}}' > exceeded_orgs.txt

if [ \`wc -l < exceeded_orgs.txt\` > 0 ]; then
        while IFS='' read -r line || [[ -n "\$line" ]]; do
                INFO=\$(sudo -u ubuntu -i -- bash -c "source $HOME/walle.rc;walle-manage org-ids list" | grep \$line | awk -F '|' '{print \$4}')
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

# Send email, $HOME/.msmtprc - config file
cat << BODY | sudo tee /root/.msmtprc
defaults
tls on
tls_starttls on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile $HOME/.msmtp.log

account walle.alerts@gigaspaces.com
host smtp.gmail.com
port 587
protocol smtp
auth on
from walle.alerts@gigaspaces.com
user walle.alerts@gigaspaces.com
passwordeval "cat $HOME/.msmtp.pass"
account default: walle.alerts@gigaspaces.com
BODY

sudo chmod 600 /root/.msmtprc

# Save email password
sudo touch /root/.msmtp.pass
sudo chown root:root /root/.msmtp.pass
sudo chmod 600 /root/.msmtp.pass
echo "LLMtSs.3t" | sudo tee /root/.msmtp.pass

# Logrotate file
echo "/var/log/walle-api.log {
        daily
        size 10M
        rotate 10
        missingok
        compress
        dateext
        su root root
        create 644 ubuntu adm
        prerotate
                /opt/walle/bin/daily_exceeded_org-id.sh
        endscript
        postrotate
                sudo initctl reload walle_api_server
        endscript

}" | sudo tee /etc/logrotate.d/walle-api
else
    ctx logger info "Skipping reports configuration, due on staging installation."
fi

mkdir -p $HOME/walle_logs

rm -f $HOME/walle.rc

# Creating walle.rc file with necessary options
echo -e "export WALLE_HOST=127.0.0.1
export WALLE_PORT=8001
export WALLE_WORKERS=4
export WALLE_DB=${WALLE_EXISTING_DB:=postgresql://${DB_USER}:${DB_PASS}@${DB_IP}/${DB_NAME}}
export WALLE_LOGGING_FILE=$HOME/walle_logs/walle-api.log
export WALLE_GUNICORN_LOGGING_FILE=$HOME/walle_logs/walle_gunicorn.log
export WALLE_LOGGING_LEVEL=DEBUG
" >> $HOME/walle.rc

rm -f $HOME/walle_api_server.conf

sudo touch /var/log/gunicorn_walle.log
sudo touch /var/log/walle-api.log
sudo chown ubuntu:ubuntu /var/log/gunicorn_walle.log /var/log/walle-api.log
sudo chmod 660 /var/log/gunicorn_walle.log /var/log/walle-api.log

# gunicorn
echo -e "description 'walle service'
# used to be: start on startup
# until we found some mounts were not ready yet while booting:
start on started mountall
stop on shutdown
# Automatically Respawn:
respawn
respawn limit 99 5
setuid ubuntu
setgid ubuntu
script
    export WALLE_DB=${WALLE_EXISTING_DB:=postgresql://${DB_USER}:${DB_PASS}@${DB_IP}/${DB_NAME}}
    exec /usr/bin/gunicorn -w 4 -b 0.0.0.0:8001 walle_api_server.cli.app:app --log-level=error --error-logfile=/var/log/gunicorn_walle.log
end script
" >> $HOME/walle_api_server.conf

sudo cp $HOME/walle_api_server.conf /etc/init/walle_api_server.conf
sudo chown root:root /etc/init/walle_api_server.conf

source $HOME/walle.rc; walle-manage db upgrade head -d walle-service/walle-api-server/migrations/
source $HOME/walle.rc; walle-manage approved-plugins add --from-file walle-service/approved_plugins/approved_plugins_description.yaml

sudo initctl start walle_api_server
