#!/bin/bash

set -e
set -o xtrace

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

sudo apt-get update

sudo apt-get upgrade -y  -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" 2>&1

sudo apt-get install -qy nginx 2>&1


curl -o score-nginx-configration.tar.gz ${SCORE_NGINX_CONFIGURATION_URL} 2>&1

wget -c ${SCORE_NGINX_CONFIGURATION_URL} -O score-nginx-configration.tar.gz 2>&1

mkdir score-nginx-configuration
tar -xvf score-nginx-configration.tar.gz -C score-nginx-configuration 2>&1
cd score-nginx-configuration/

mv www ~/www

sed "s/127.0.0.1/${SCORE_INTERNAL_IP_ADDRESS}/g" -i etc/nginx/vca_io

sudo chmod 600 etc/keys/*
sudo cp etc/keys/* /etc/nginx
sudo rm -fr /etc/nginx/sites-enabled/*
sudo cp etc/nginx/vca_io /etc/nginx/sites-enabled/

sudo service nginx restart
