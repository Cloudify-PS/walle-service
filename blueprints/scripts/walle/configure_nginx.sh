#!/bin/bash

set -e
set -o xtrace

cd $HOME

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

if [ x"$SKIP_INSTALLATION" != x"true" ]; then

    ctx logger info "Installing Nginx."

    sudo apt-get update

    sudo apt-get upgrade -y  -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" 2>&1

    sudo apt-get install -qy nginx 2>&1

else
    ctx logger info "Skipping installation, using existing Nginx."
fi

rm -f walle-nginx-configration.tar.gz
curl -o walle-nginx-configration.tar.gz ${WALLE_NGINX_CONFIGURATION_URL} 2>&1
if [ "$?" -gt "0" ]; then
    ctx logger info "Download configuration."
    wget -c ${WALLE_NGINX_CONFIGURATION_URL} -O walle-nginx-configration.tar.gz 2>&1
fi

if [ -d "walle-nginx-configuration" ]; then
    mv walle-nginx-configuration walle-nginx-configuration-`date +"%m-%d-%y-%H-%m-%S"`
fi

mkdir -p walle-nginx-configuration

tar -xvf walle-nginx-configration.tar.gz -C walle-nginx-configuration 2>&1

cd walle-nginx-configuration/
if [ -d "$HOME/www" ]; then
    mv $HOME/www $HOME/www-`date +"%m-%d-%y-%H-%m-%S"`
fi
mv www $HOME/www

sed "s/walle_ip_gunicorn/${WALLE_INTERNAL_IP_ADDRESS}/g" -i etc/nginx/vca_io

sudo chmod 600 etc/keys/*
sudo cp etc/keys/* /etc/nginx
sudo rm -fr /etc/nginx/sites-enabled/*
sudo cp etc/nginx/vca_io /etc/nginx/sites-enabled/

sudo service nginx restart
