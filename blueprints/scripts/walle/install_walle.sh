#!/bin/bash

set -e
set -o xtrace

cd $HOME

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

rm -f walle-service.tar.gz
curl -o walle-service.tar.gz ${WALLE_PACKAGE_URL}  2>&1
mkdir -p walle-service
tar -xvf walle-service.tar.gz -C walle-service 2>&1
cd walle-service/
sudo pip install -r walle-api-server/requirements.txt
sudo pip install ./walle-api-server
