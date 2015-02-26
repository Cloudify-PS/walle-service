#!/bin/bash

#as root
#sudo -i

PRJ=/home/ubuntu/score-service

service nginx stop
rm /etc/nginx/sites-enabled/*
ln -s $PRJ/conf/nginx/vca_io /etc/nginx/sites-enabled
service nginx start

