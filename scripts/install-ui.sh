#!/bin/sh

mkdir www
cd www
wget https://github.com/kostya13/binary-archive/raw/master/walle-ui.tar.gz
tar zxvg walle-ui.tar.gz
sudo apt-get install nginx
sudo service nginx stop
cp vca-io /etc/nginx/sites-enabled/default
sudo service nginx start
