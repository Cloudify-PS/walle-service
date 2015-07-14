#!/bin/bash

set -e
set -o xtrace

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

wget -c ${SCORE_PACKAGE_URL} -O score-service.tar.gz 2>&1
mkdir score-service
tar -xvf score-service.tar.gz -C score-service 2>&1
cd score-service/
git init
cd score-api-server/
sudo pip install -r requirements.txt && sudo python setup.py install 2>&1
