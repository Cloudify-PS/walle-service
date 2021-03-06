#!/bin/bash

#as root
#sudo -i

apt-get update
apt-get install -y nginx git build-essential \
libssl-dev libffi-dev libxml2-dev libxslt-dev \
python-dev python-pip


pip install virtualenv

PRJ=/home/ubuntu/walle-service

service nginx stop

rm /etc/nginx/sites-enabled/*
ln -s $PRJ/conf/nginx/vca_io /etc/nginx/sites-enabled

service nginx start
