#!/bin/bash

set -e
set -o xtrace

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

if [ "$SKIP_INSTALLATION" = "False" ]; then
    sudo apt-get update

    sudo apt-get upgrade -y  -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" 2>&1

    sudo apt-get install -qy nginx 2>&1

else
    echo "Skipping installation, using existing Nginx."
fi

curl -o score-nginx-configration.tar.gz ${SCORE_NGINX_CONFIGURATION_URL} 2>&1
if [ "$?" -gt "0" ]; then
    wget -c ${SCORE_NGINX_CONFIGURATION_URL} -O score-nginx-configration.tar.gz 2>&1
fi

if [ -d "score-nginx-configuration" ]; then
    mv score-nginx-configuration score-nginx-configuration-`date +"%m-%d-%y-%H-%m-%S"`
fi

mkdir score-nginx-configuration

tar -xvf score-nginx-configration.tar.gz -C score-nginx-configuration 2>&1

cd score-nginx-configuration/
mv ~/www ~/www-`date +"%m-%d-%y-%H-%m-%S"`
mv www ~/www

sed "s/127.0.0.1/${SCORE_INTERNAL_IP_ADDRESS}/g" -i etc/nginx/vca_io

sudo chmod 600 etc/keys/*
sudo cp etc/keys/* /etc/nginx
sudo rm -fr /etc/nginx/sites-enabled/*
sudo cp etc/nginx/vca_io /etc/nginx/sites-enabled/

sudo service nginx restart
