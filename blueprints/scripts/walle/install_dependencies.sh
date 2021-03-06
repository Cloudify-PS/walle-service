#!/bin/bash

sudo apt-get update

sudo apt-get upgrade -y  -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" 2>&1

sudo apt-get install -qy build-essential libssl-dev unzip \
 libffi-dev libxml2-dev postgresql-client \
 gunicorn nginx libxslt-dev python-dev \
 python-pip git libpq-dev curl msmtp 2>&1
