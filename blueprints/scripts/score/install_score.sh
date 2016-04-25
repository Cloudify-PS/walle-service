#!/bin/bash

set -e
set -o xtrace

cd ~

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

rm -f score-service.tar.gz
curl -o score-service.tar.gz ${SCORE_PACKAGE_URL}  2>&1
mkdir -p score-service
tar -xvf score-service.tar.gz -C score-service 2>&1
cd score-service/
git init
cd score-api-server/
sudo pip install -r requirements.txt && sudo python setup.py install 2>&1
